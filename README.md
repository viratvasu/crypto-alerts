# Crypto Alerts

**Frontend**: [Live Demo](https://crypto-alerts-one.vercel.app/)

**Backend**: [API Endpoint](https://www.sahitvasu.info/)

**API Documentation**: [API Structure](https://www.sahitvasu.info/docs/)

---

### Architecture Overview

![Architecture Diagram](https://github.com/viratvasu/images/blob/main/websocket-architecture-svg.png)

---

### Technologies Used

- **Backend**: FastAPI
- **Frontend**: ReactJS
- **Database**: SQLite3
- **Deployment**: AWS, Vercel

---

### Local Setup Instructions

#### 1. Clone the repository:
```bash
 git clone <repo_url>
```

#### 2. Navigate to the backend folder:
```bash
 cd backend
```

#### 3. Create and activate a virtual environment:
```bash
 python3.11 -m venv venv
 source venv/bin/activate
```

#### 4. Install dependencies:
```bash
 pip install -r requirements.txt
```

#### 5. Set up a `.env` file:
```env
 DB_URL=sqlite:///./alerts.db
 BINANCE_WS_URL=wss://stream.binance.com:9443/ws
 TOP_CRYPTOS=BTCUSDT,ETHUSDT,BNBUSDT,XRPUSDT,DOGEUSDT
 MAIL_USERNAME=<your_email_username>
 MAIL_PASSWORD=<your_email_password>
 MAIL_SERVER=<your_mail_server>
 MAIL_FROM=<your_email_address>
```

#### 6. Start the server:
```bash
 uvicorn app:app --reload
```

---

### Database Migrations

#### Generate migration files:
```bash
 alembic revision --autogenerate -m "<migration_message>"
```

#### Apply migrations:
```bash
 alembic upgrade head
```

---

### Features Missing (Due to Time Constraints)

1. **Real-time Alert Notifications**: Currently batch alerts run every 5 minutes (configurable).
2. **User Authentication**.
3. **Logging and Unit Testing**.
4. **Denormalized Tables**: For join optimization.
5. **Alert History on Frontend UI**.

---

### Edge Cases Handled

1. **Burst Notifications**: Prevent duplicate alerts by throttling for 10 minutes (configurable).
2. **WebSocket Auto-Reconnection**: Resumes on Binance WebSocket disconnection.

---

### Scalable Architecture for Real-time Updates

![Scalable Architecture](https://github.com/viratvasu/images/blob/main/crypto-alert-system-clean.png)

---

