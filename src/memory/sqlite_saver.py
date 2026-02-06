import aiosqlite
from pathlib import Path
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from typing import Optional

path = Path(__file__).resolve().parent.parent.parent
db_file_path = path / "storage" / "agent_memory.db"

# Singleton state - module-level variables
_conn: Optional[aiosqlite.Connection] = None
_sqlite_saver: Optional[AsyncSqliteSaver] = None
_initialized = False

async def get_sqlite_saver() -> AsyncSqliteSaver:
    """
    Get the SQLite saver singleton.
    Creates connection only once, reuses it on subsequent calls.
    """
    global _conn, _sqlite_saver, _initialized
    
    # Singleton check: if already initialized, return existing instance
    if _sqlite_saver is not None and _initialized:
        return _sqlite_saver
    
    # Create connection only if it doesn't exist
    if _conn is None:
        # Ensure storage directory exists
        db_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create async connection (this is the only place it's created)
        _conn = await aiosqlite.connect(str(db_file_path))
        
        # Create async checkpointer with the connection
        _sqlite_saver = AsyncSqliteSaver(_conn)
        _initialized = True
    
    return _sqlite_saver

async def close_sqlite_connection():
    """Close the singleton connection"""
    global _conn, _sqlite_saver, _initialized
    
    if _conn is not None:
        try:
            await _conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
        finally:
            _conn = None
            _sqlite_saver = None
            _initialized = False
