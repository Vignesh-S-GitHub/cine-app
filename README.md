<div align="center">

# Cine App
### The Encyclopedia of Entertainment

**Cinema discovery · IMDb data pipeline · FastAPI foundation**

</div>

Cine App is an early-stage cinema web-app project. The repository currently contains a Python backend scaffold, an IMDb data-processing pipeline, and tests. It does **not yet contain a finished end-user cinema browsing experience**, so this README describes the work in progress rather than promising production features.

## What is in the repository

- **FastAPI backend structure** for authentication, database access, models, routers, schemas, and services
- **IMDb data pipeline scripts** for downloading, merging, and processing source datasets
- **Test directory** for backend behavior as the project develops
- **Docker Compose configuration** for local service orchestration

## Technology

| Area | Current foundation |
|---|---|
| API | FastAPI, Pydantic |
| Data processing | Polars, pandas, DuckDB, PyArrow |
| Database connectivity | psycopg |
| Project management | Python 3.11+, uv |

## Get started

Install the locked project dependencies:

```bash
uv sync
```

The main module is currently a placeholder, and the API entry point is not yet complete. Check the backend and data-pipeline modules for the current implementation before attempting to run the service. Environment configuration is kept outside the README; copy `.env` settings from your own local configuration and never publish secrets.

## Roadmap direction

The current structure lays groundwork for a cinema information app backed by IMDb datasets. API behavior, persistence, and a user-facing interface will be documented here as those parts become implemented.

---

<p align="center"><sub>A cinema data app in its early build stage.</sub></p>
