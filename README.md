<div align="center">

# 🎬 Cine App

**An IMDb data pipeline with a future cinema API scaffold.**

![Python 3.11+](https://img.shields.io/badge/Python%203.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-947800?style=flat-square&logo=duckdb&logoColor=white)
![uv](https://img.shields.io/badge/uv-5C3EE8?style=flat-square&logo=uv&logoColor=white)

[Status](#implementation-status) · [Quick start](#quick-start) · [Data pipeline](#data-pipeline)

</div>

---

An early-stage cinema project. Its working source centers on downloading IMDb datasets and converting selected tables into DuckDB and Parquet. The planned FastAPI routes, database models, tests, and Docker service configuration are currently scaffolding.

<a id="implementation-status"></a>

## 🚧 Implementation status

| Component | Present in source |
|---|---|
| IMDb downloader | Async HTTP downloads for seven datasets, ETag metadata, retries, and progress |
| Dataset processing | DuckDB tables and Parquet exports for title basics, ratings, and person basics |
| Weekly workflow | Scheduled/manual download → process → merge-script invocation |
| Merge script | Empty placeholder; incremental merging is not implemented |
| FastAPI backend and tests | Empty module placeholders; no runnable API or test coverage |
| Docker Compose | Empty placeholder |
| End-user interface | Not implemented |

<a id="quick-start"></a>

## 🚀 Quick start

Requirements: Python **3.11+**, [uv](https://docs.astral.sh/uv/), internet access, and disk/memory capacity for large IMDb datasets.

```bash
git clone https://github.com/Vignesh-S-GitHub/cine-app.git
cd cine-app
uv sync --locked
uv run python data_pipeline/download_imdb.py
uv run python data_pipeline/process_imdb.py
```

Run from the repository root so relative data paths resolve correctly. These are pipeline commands, not a web-server launch.

<a id="data-pipeline"></a>

## 🗃️ Data pipeline

| Output | Location |
|---|---|
| Compressed source files and ETag metadata | `data/raw/` |
| Processed database | `data/IMDB_DATA.duckdb` |
| Selected Parquet tables | `data/parquet/` |
| Download/process logs | `logs/` |

The [workflow](.github/workflows/imdb_update.yml) requests a Sunday **02:30 UTC / 08:00 IST** run and allows manual dispatch. It invokes the empty merge script and does not upload pipeline outputs as artifacts or commit them, so this is not a persistent published dataset service.

Source datasets: [IMDb non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/). Review their use conditions before using or redistributing data.

## 📁 Repository guide

- [download_imdb.py](data_pipeline/download_imdb.py) — dataset acquisition.
- [process_imdb.py](data_pipeline/process_imdb.py) — DuckDB processing and Parquet exports.
- [backend/app/](backend/app/) — intended API layout.
- [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock) — environment definition and lockfile.

## 🛤️ Next implementation steps

Implement incremental merging, complete the API/database layer, add meaningful tests, and build a browsing interface before presenting this as a finished cinema application.

## 🤝 Contributing

Open an issue with a reproducible example or submit a focused pull request. Keep setup instructions and documentation aligned with any behavior changes.

## 📄 License

No repository-level `LICENSE` file is currently included.
