import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='dbflask',
    )

def alta_usuario(email, clave):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios (email, clave) VALUES (%s, %s)", (email, clave))
        conexion.commit()
        conexion.close()
    
def obtener_usuario(email):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT email, clave FROM usuarios WHERE email=%s", (email))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

if __name__ == '__main__':
    alta_usuario('prueba1@mail.com', 'password')
    print(obtener_usuario('prueba1@mail.com')[1])