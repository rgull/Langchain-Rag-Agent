import sqlite3
import atexit
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

path = Path(__file__).resolve().parent.parent.parent
db_file_path = path / "storage" / "agent_memory.db"

conn = sqlite3.connect(db_file_path, check_same_thread=False)
sqlite_saver = SqliteSaver(conn)

atexit.register(conn.close) # Ensure the connection is closed on exit

def get_sqlite_saver() -> SqliteSaver:
    return sqlite_saver
