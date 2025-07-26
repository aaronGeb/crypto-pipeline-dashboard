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
