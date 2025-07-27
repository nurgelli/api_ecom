#!/bin/sh

export PGUSER='nurgelli'
export PGPASSWORD="${POSTGRES_PASSWORD}"

psql postgres -c "CREATE DATABASE postgres_db"
psql postgres_db -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"


psql postgres_db -c '
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
'