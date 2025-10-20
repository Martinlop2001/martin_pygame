

import db
if __name__ == "__main__":
    conn = db.connect()
db.init_db(conn)

pid = db.get_or_create_jugador(conn, "Silvana")
db.registrar_puntuacion(conn, pid, 123, 1)

for r in db.top_n(conn, 5):
    print(dict(r))

db.set_ajuste(conn, "dificultad", "media")

print("Dificultad:", db.get_ajuste(conn, "dificultad"))
conn.close()