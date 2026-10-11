
import os
import time

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/lost_and_found"
)


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def init_db():
    """Create the items table and retry while PostgreSQL starts."""
    for attempt in range(10):
        try:
            with get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id SERIAL PRIMARY KEY,
                        item_type VARCHAR(10) NOT NULL
                            CHECK (item_type IN ('lost', 'found')),
                        title VARCHAR(200) NOT NULL,
                        description TEXT NOT NULL,
                        category VARCHAR(100) NOT NULL DEFAULT 'other',
                        location VARCHAR(200) NOT NULL,
                        item_date DATE NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                """)
            print("Database initialized successfully.")
            return
        except psycopg.OperationalError:
            if attempt == 9:
                raise
            print("Waiting for PostgreSQL...")
            time.sleep(2)
