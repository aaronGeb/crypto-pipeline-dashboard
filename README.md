# 📊 Crypto Data Pipeline & BI Dashboard

A production-grade data pipeline that ingests real-time cryptocurrency market data from the [CoinGecko API](https://www.coingecko.com/), transforms it into analytics-ready tables using **dbt**, and visualizes market KPIs with **Power BI**.

---

## 🧭 Overview

This project demonstrates how to build a modern data stack using:

- **Apache Airflow** for orchestration
- **PostgreSQL** for data storage
- **dbt** for transformation
- **Power BI** for dashboarding

---

## ⚙️ Architecture

```text
CoinGecko API → Airflow → PostgreSQL (raw) → dbt → Power BI
```

## 🚀 Quickstart
### 1. Setup Environment
Install dependencies with uv:
```
uv venv
uv pip install -r pyproject.toml
```
### 2. Configure PostgreSQL
Run this SQL to create the raw table:
```
CREATE TABLE IF NOT EXISTS raw_market_data (
    id SERIAL PRIMARY KEY,
    coin_id TEXT,
    symbol TEXT,
    price_usd NUMERIC,
    volume_usd NUMERIC,
    market_cap_usd NUMERIC,
    change_1h_pct NUMERIC,
    change_24h_pct NUMERIC,
    change_7d_pct NUMERIC,
    timestamp TIMESTAMP
);
```



### 🗃 Project Structure
bash
Copy
Edit
```
crypto-data-pipeline/
├── dags/
├── dbt_crypto/
│   ├── models/
├── scripts/
├── dashboard/
├── database/schema.sql
├── pyproject.toml
└── README.md
```
