# Crypo alerts

- Run locally
```
-> Go to backend/ then run below command

uvicorn app:app --reload
```

- Migrations
```
To generate migration files
alembic revision --autogenerate -m 'message here'

To migrate file
alembic upgrade head
```