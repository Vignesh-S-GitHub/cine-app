from pathlib import Path

import duckdb
from loguru import logger

RAW_DIR = Path("data/raw")
PARQUET_DIR = Path("data/parquet")
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path("data/IMDB_DATA.duckdb")


def process_title_basics(con):
    logger.info("Processing title.basics.tsv.gz")

    con.execute("""
    CREATE OR REPLACE TABLE title_basics AS
    SELECT
        tconst,
        titleType,
        primaryTitle,
        originalTitle,
        CAST(NULLIF(startYear, '\\N') AS INTEGER) AS startYear,
        CAST(NULLIF(endYear, '\\N') AS INTEGER) AS endYear,
        CAST(NULLIF(runtimeMinutes, '\\N') AS INTEGER) AS runtimeMinutes,
        genres
    FROM read_csv_auto(
        'data/raw/title.basics.tsv.gz',
        delim='\t'
    )
    """)

    con.execute("""
    COPY title_basics
    TO 'data/parquet/title_basics.parquet'
    (FORMAT PARQUET)
    """)


def process_title_ratings(con):
    logger.info("Processing title.ratings.tsv.gz")

    con.execute("""
    CREATE OR REPLACE TABLE title_ratings AS
    SELECT *
    FROM read_csv_auto(
        'data/raw/title.ratings.tsv.gz',
        delim='\t'
    )
    """)

    con.execute("""
    COPY title_ratings
    TO 'data/parquet/title_ratings.parquet'
    (FORMAT PARQUET)
    """)


def process_name_basics(con):
    logger.info("Processing name.basics.tsv.gz")

    con.execute("""
    CREATE OR REPLACE TABLE name_basics AS
    SELECT *
    FROM read_csv_auto(
        'data/raw/name.basics.tsv.gz',
        delim='\t'
    )
    """)

    con.execute("""
    COPY name_basics
    TO 'data/parquet/name_basics.parquet'
    (FORMAT PARQUET)
    """)


def main():
    logger.info("Connecting to DuckDB")

    con = duckdb.connect(DB_PATH)

    process_title_basics(con)
    process_title_ratings(con)
    process_name_basics(con)

    logger.success("Processing completed")

    con.close()


if __name__ == "__main__":
    logger.add(
        "logs/process.log",
        rotation="10 MB"
    )

    main()