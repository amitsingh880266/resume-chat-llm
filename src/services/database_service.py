from pathlib import Path
import sqlite3
from src.config import settings


def get_connection()-> sqlite3.Connection:
    settings.database_path.parent.mkdir(
        parents = True,
        exist_ok = True
    )

    return sqlite3.connect(settings.database_path)