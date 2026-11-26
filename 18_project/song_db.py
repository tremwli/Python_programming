

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "song.db")



def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                search_title TEXT NOT NULL,
                search_artist TEXT NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                lyrics TEXT NOT NULL,
                PRIMARY KEY (
                    search_title,
                    search_artist,
                    title,
                    artist,
                    lyrics
                )
            )
        """)

        conn.commit()

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise

    finally:
        if conn is not None:
            conn.close()



def load_songs(search_title, search_artist):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT title, artist, lyrics
            FROM songs
            WHERE search_title = ? AND search_artist = ?
            """,
            (search_title, search_artist)
        )

        rows = cur.fetchall()

        result = []
        for row in rows:
            song = {
                "제목": row[0],
                "가수": row[1],
                "가사": row[2]
            }
            result.append(song)

        return result

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise

    finally:
        if conn is not None:
            conn.close()



def save_songs(search_title, search_artist, rows):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        values = []

        for song in rows:
            values.append((
                search_title,
                search_artist,
                song["제목"],
                song["가수"],
                song["가사"]
            ))

        cur.executemany(
            """
            INSERT OR REPLACE INTO songs
            VALUES (?, ?, ?, ?, ?)
            """,
            values
        )

        conn.commit()

    except sqlite3.Error as e:
        print("DB 오류:", e)
        if conn is not None:
            conn.rollback()
        raise

    finally:
        if conn is not None:
            conn.close()



def add_song(title, artist, lyrics):
    song = {
        "제목": title,
        "가수": artist,
        "가사": lyrics
    }

    
    save_songs(title, artist, [song])



def get_songs():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT title, artist, lyrics
            FROM songs
           
            """
        )

        rows = cur.fetchall()

        result = []
        for row in rows:
            song = {
                "제목": row[0],
                "가수": row[1],
                "가사": row[2]
            }
            result.append(song)

        return result

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise

    finally:
        if conn is not None:
            conn.close()
