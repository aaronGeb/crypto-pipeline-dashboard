-- PostgreSQL schema for a crypto data pipeline using CoinGecko API

-- 1. Table: coins
CREATE TABLE coins (
    id TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    asset_platform_id TEXT,
    image_url TEXT,
    last_updated TIMESTAMPTZ
);

-- 2. Table: coin_market_data
CREATE TABLE coin_market_data (
    id SERIAL PRIMARY KEY,
    coin_id TEXT REFERENCES coins(id),
    current_price NUMERIC,
    market_cap BIGINT,
    market_cap_rank INTEGER,
    total_volume BIGINT,
    high_24h NUMERIC,
    low_24h NUMERIC,
    price_change_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    circulating_supply NUMERIC,
    total_supply NUMERIC,
    max_supply NUMERIC,
    last_updated TIMESTAMPTZ,
    UNIQUE (coin_id, last_updated)
);

-- 3. Table: coin_historical_prices
CREATE TABLE coin_historical_prices (
    id SERIAL PRIMARY KEY,
    coin_id TEXT REFERENCES coins(id),
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    market_cap BIGINT,
    UNIQUE (coin_id, date)
);

-- 4. Table: exchanges
CREATE TABLE exchanges (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    year_established INTEGER,
    country TEXT,
    url TEXT,
    trust_score INTEGER,
    trade_volume_24h_btc NUMERIC
);

-- 5. Table: tickers
CREATE TABLE tickers (
    id SERIAL PRIMARY KEY,
    coin_id TEXT REFERENCES coins(id),
    base TEXT,
    target TEXT,
    market_name TEXT,
    last_price NUMERIC,
    volume NUMERIC,
    trade_url TEXT,
    timestamp TIMESTAMPTZ,
    UNIQUE (coin_id, base, target, market_name, timestamp)
);

-- 6. Table: categories
CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    name TEXT
);

-- 7. Junction table: coin_categories
CREATE TABLE coin_categories (
    coin_id TEXT REFERENCES coins(id),
    category_id TEXT REFERENCES categories(id),
    PRIMARY KEY (coin_id, category_id)
);
