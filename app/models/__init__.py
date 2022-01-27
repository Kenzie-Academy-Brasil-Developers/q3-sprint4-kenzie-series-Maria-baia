import psycopg2

def create_table():
    conn = psycopg2.connect(host="localhost", database="kenzie_series",
    user="maria", password="17122001")

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ka_series(
            id BIGSERIAL PRIMARY KEY,
            serie VARCHAR(100) NOT NULL UNIQUE,
            seasons INTEGER NOT NULL,
            released_date DATE NOT NULL,
            genre VARCHAR(50) NOT NULL,
            imdb_rating FLOAT NOT NULL
        );
        """)
        
    conn.commit()

    cur.close()
    conn.close()