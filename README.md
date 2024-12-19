# Crypo alerts

architecture

![architecure_image](https://github.com/viratvasu/images/blob/main/websocket-architecture-svg.png)

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