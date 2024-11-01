import sqlite3

async def establish_conn():
    db = sqlite3.connect('core.db')
    try:
        yield db
    finally:
        db.close()