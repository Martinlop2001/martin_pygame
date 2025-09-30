

from pathlib import Path
import sqlite3

DB_NAME = "game.db"
SCHEMA = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS jugadores (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS puntuaciones (
    id INTEGER PRIMARY KEY,
    jugador_id INTEGER NOT NULL,
    puntaje INTEGER NOT NULL CHECK (puntaje >= 0),
    nivel INTEGER NOT NULL CHECK (nivel >= 1),
    creado_en TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (jugador_id) REFERENCES jugadores(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS ajustes (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);
PRAGMA user_version = 1;
"""

def get_db_path(base_dir=None):
    base = Path(base_dir or Path(__file__).parent)
    return base / DB_NAME

def connect(db_path=None):
    """Abre/crea la base y devuelve una conexión lista para usar."""
    path = Path(db_path or get_db_path())
    # check_same_thread=False permite compartir conexión entre hilos si fuera necesario
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row # filas como dict: row["col"]
    return conn

def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()

def get_or_create_jugador(conn, nombre: str) -> int:
    cur = conn.execute("SELECT id FROM jugadores WHERE nombre = ?", (nombre,))
    row = cur.fetchone()
    if row:
        return row["id"]
    cur = conn.execute("INSERT INTO jugadores(nombre) VALUES (?)", (nombre,))
    conn.commit()
    return cur.lastrowid

def registrar_puntuacion(conn, jugador_id: int, puntaje: int, nivel: int) -> None:
    conn.execute(
        "INSERT INTO puntuaciones(jugador_id, puntaje, nivel) VALUES (?,?,?)",
        (jugador_id, puntaje, nivel),
    )
    conn.commit()

def top_n(conn, n: int = 10, nivel: int | None = None):
    if nivel is None:
        sql = (
            """
            SELECT j.nombre, p.puntaje, p.nivel, p.creado_en
            FROM puntuaciones p
            JOIN jugadores j ON j.id = p.jugador_id
            ORDER BY p.puntaje DESC, p.creado_en ASC
            LIMIT ?
            """
        )
        cur = conn.execute(sql, (n,))
        
    else:
        sql = (
            """
            SELECT j.nombre, p.puntaje, p.nivel, p.creado_en
            FROM puntuaciones p
            JOIN jugadores j ON j.id = p.jugador_id
            WHERE p.nivel = ?
            ORDER BY p.puntaje DESC, p.creado_en ASC
            LIMIT ?
            """
        )
        cur = conn.execute(sql, (nivel, n))
    return cur.fetchall()

def set_ajuste(conn, clave: str, valor: str) -> None:
    conn.execute(
        "INSERT INTO ajustes(clave, valor) VALUES (?, ?)\n"
        "ON CONFLICT(clave) DO UPDATE SET valor = excluded.valor",
        (clave, valor),
    )
    conn.commit()

def get_ajuste(conn, clave: str, default: str | None = None) -> str | None:
    cur = conn.execute("SELECT valor FROM ajustes WHERE clave = ?", (clave,))
    row = cur.fetchone()
    return row["valor"] if row else default