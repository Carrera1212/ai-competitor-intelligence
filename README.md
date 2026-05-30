AI Competitor Intelligence Engine

A high-performance, asynchronous REST API built with FastAPI designed to aggregate, process, and track competitor intelligence data. This service integrates a relational database backend to store structured market data, allowing businesses to monitor competitor movements, pricing changes, and feature rollouts in real-time.

Features
* **Asynchronous API Endpoints**: Built on FastAPI for lightning-fast request handling and automatic OpenAPI/Swagger documentation generation.
* **Structured Data Persistence:** Integrated relational database layer to cleanly store and query competitor metrics.
* **Modular Architecture:** Clean separation of concerns between API routing, business logic, and database operations.
* **Automated Environment Isolation:** Out-of-the-box configuration minimizing local dependency bloat.

Tech Stack
* **Framework:** FastAPI (Python)
* **ASGI Server:** Uvicorn
* **Database:** SQLite / SQLAlchemy (Relational storage)
* **Data Validation:** Pydantic

 Project Structure
```text
 app_with_db.py       # Core application containing API routes & database initialization
Competitor_data.db    Contains the logs of the company names.
 README.md            Project documentation
