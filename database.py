import sqlite3

def create_frames_table(db_name='yolo_data.db'):
    # SQLite connection and cursor setup
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create frames table if it does not exist
    create_table_sql = """
                       CREATE TABLE IF NOT EXISTS frames (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           device_id TEXT NOT NULL,
                           frame_data BLOB NOT NULL,
                           fire INTEGER NOT NULL,
                           x INTEGER,
                           y INTEGER,
                           w INTEGER,
                           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
                       """
    cursor.execute(create_table_sql)
    conn.commit()

    # Close connection
    conn.close()

if __name__ == "__main__":
    create_frames_table()