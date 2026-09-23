import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent.parent / "medvision.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            image_format TEXT,
            width INTEGER,
            height INTEGER,
            model TEXT NOT NULL,
            question TEXT,
            analysis TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(
    filename,
    metadata,
    model,
    question,
    analysis,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO analyses (
            filename,
            image_format,
            width,
            height,
            model,
            question,
            analysis,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            metadata["format"],
            metadata["width"],
            metadata["height"],
            model,
            question,
            analysis,
            datetime.now().isoformat(),
        ),
    )

    connection.commit()
    analysis_id = cursor.lastrowid
    connection.close()

    return analysis_id


def get_analyses():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM analyses
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_analysis(analysis_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM analyses
        WHERE id = ?
        """,
        (analysis_id,),
    ).fetchone()

    connection.close()

    return dict(row) if row else None