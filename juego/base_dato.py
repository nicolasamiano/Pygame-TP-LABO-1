import sqlite3

def generar_tabla():
    with sqlite3.connect("top_scores.db") as conexion:
        try:
            sentencia = ''' create  table scores
            (
            id integer primary key autoincrement,
            usuario text,
            scores integer
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla scores")
        except sqlite3.OperationalError:
            print("La tabla de scores ya existe")

def subir_tabla(jugador,scores):
    with sqlite3.connect("top_scores.db") as conexion:
        try:
            conexion.execute("INSERT INTO scores(usuario,scores) VALUES (?,?)", (f"{jugador}", scores))
            conexion.commit()
        except:
            print("Error")

def ordenar_scores():
    with sqlite3.connect("top_scores.db") as conexion:
        cursor = conexion.execute("SELECT * FROM scores ORDER BY scores DESC;")
        lista_scores = []
    for fila in cursor:
        #print(fila)
        lista_scores.append(fila)
    return lista_scores