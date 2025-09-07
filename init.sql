-- Initial database setup for RoomScheduler
-- This file will be executed when PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'Europe/Kiev';

-- Database is already created by POSTGRES_DB environment variable
-- You can add any initial data here if needed
