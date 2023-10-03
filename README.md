<h1 align="center"> 
 E-Commerce Admin Dashboard
</h1>


# Features

✅ Well Structured Code Approach. \
✅ Relational Database: Postgres\
✅ Local dockerized db.\
✅ Dockerized PgAdmin to check the db records.\
✅ Migrations, Serializers and ORM configured.\
✅ Logging Mechanism.\
✅ Sanity Checks to enhance the Code Quality \
✅ Poetry dependency management and packaging made easy.


# Technologies

- Alembic: For Database Migrations.
- SQLAlchemy: For ORM.
- Pydantic: For Typing or Serialization.
- Pytest: For test cases.
- Poetry: Python dependency management and packaging made easy.
- Docker & docker-compose : For Virtualization.
- PostgresSQL: Database.
- PgAdmin 4: To interact with the Postgres database sessions.
- Loguru: Easiest logging ever done.

# How to setup this application locally
Make sure you have docker and docker-compose installed [docker installation guide](https://docs.docker.com/compose/install/)
## Step 1
Run this command in root folder:
```
cp template.env .env
```
Copy this content into your .env:
```
DATABASE_URL=postgresql+psycopg://postgres_admin:password@db:5432/ecommerce_db
DB_USER=postgres_admin
DB_PASSWORD=password
DB_NAME=ecommerce_db
PG_ADMIN_EMAIL=admin@xyz.com
PG_ADMIN_PASSWORD=admin
```

## Step 2
```
docker-compose up
```
The e-commerce admin dashboard application is up & running.

# Application URLs

- Application URL on `localhost:8000`
- Swagger docs on `localhost:8000/docs`
- PgAdmin on `localhost:5050`

<img src="https://github.com/hamzaijaz-dev/FastAPI-SQLAlchemy-Docker/blob/main/images/docs.png" alt="FastAPI SQLAlchemy Docker">

# Database Schema
<img src="https://github.com/hamzaijaz-dev/FastAPI-SQLAlchemy-Docker/blob/main/images/DB-Schema.png" alt="FastAPI SQLAlchemy Docker">

