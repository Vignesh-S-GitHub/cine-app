import asyncio
import json
from pathlib import Path

import httpx
from loguru import logger
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from tenacity import retry, stop_after_attempt, wait_exponential

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

METADATA_FILE = DATA_DIR / "metadata.json"

BASE_URL = "https://datasets.imdbws.com"

IMDB_FILES = [
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz",
]


def load_metadata() -> dict:
    if METADATA_FILE.exists():
        return json.loads(METADATA_FILE.read_text())

    return {}


def save_metadata(metadata: dict):
    METADATA_FILE.write_text(
        json.dumps(metadata, indent=2)
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
async def download_file(
    client: httpx.AsyncClient,
    filename: str,
    metadata: dict,
    progress: Progress,
):
    url = f"{BASE_URL}/{filename}"
    output_path = DATA_DIR / filename

    head_response = await client.head(url)
    head_response.raise_for_status()

    etag = head_response.headers.get("etag")

    if (
        filename in metadata
        and metadata[filename].get("etag") == etag
        and output_path.exists()
    ):
        logger.info(f"Skipping {filename} (unchanged)")
        return

    logger.info(f"Downloading {filename}")

    async with client.stream("GET", url) as response:
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))

        task_id = progress.add_task(
            filename,
            total=total,
        )

        with open(output_path, "wb") as file:
            async for chunk in response.aiter_bytes():
                file.write(chunk)
                progress.update(
                    task_id,
                    advance=len(chunk),
                )

    metadata[filename] = {
        "etag": etag
    }

    logger.success(f"Downloaded {filename}")


async def main():
    metadata = load_metadata()

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )

    async with (
        progress,
        httpx.AsyncClient(timeout=120.0) as client,
    ):
        tasks = [
            download_file(
                client,
                filename,
                metadata,
                progress,
            )
            for filename in IMDB_FILES
        ]

        await asyncio.gather(*tasks)

    save_metadata(metadata)


if __name__ == "__main__":
    logger.add(
        "logs/download.log",
        rotation="10 MB",
    )

    asyncio.run(main())