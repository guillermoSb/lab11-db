import psycopg2
from psycopg2 import extensions

conn = psycopg2.connect("dbname=lab11 user=postgres")  # Connect to the Database
cur = conn.cursor()  # Cursor used to perform database queries


# Menu de opciones
def menu():
    print("Opciones: ")
    print("1. Localizar PC utilizando VELOCIDAD y RAM")
    print("2. Eliminar una PC y Producto utilizando un modelo")
    print("3. Descontar el precio de un modelo")
    print("4. Buscar PC")
    print("5. Salir")


def ejercicio1(velocidad, ram):
    cur.execute("SELECT modelo, precio FROM pc WHERE ram = %s AND velocidad = %s;", (ram, velocidad))
    filas = cur.fetchall()
    if len(filas) <= 0:
        print("No hay resultados.")
    else:
        for fila in filas:
            print(fila)

def ejercicio2(modelo):
    cur.execute("SELECT * FROM pc WHERE modelo = %s", (modelo,))
    filas = cur.fetchall()
    if len(filas) <= 0:
        print("No hay productos con ese modelo.")
    else:
        cur.execute("""
            DELETE FROM pc
            WHERE modelo = %s;
            DELETE FROM productos
            WHERE modelo = %s;
        """, (modelo, modelo))
        conn.commit()
        print("Se han eliminado todos los registros para el modelo %s" % modelo)

def ejercicio3(modelo):
    cur.execute("SELECT precio FROM pc WHERE modelo = %s", (modelo,))
    filas = cur.fetchone()
    if len(filas) <= 0:
        print("No hay productos con ese modelo.")
    else:
        cur.execute("""
            UPDATE pc
            SET precio = precio - 100
            WHERE modelo = 'Macbook';
        """)
        print("Se ha descontado en $100 el modelo %s" % modelo)

def ejercicio4(fabricante, modelo, velocidad, ram, disco, precio):
    cur.execute("""
        SELECT * FROM pc 
        WHERE modelo = %s AND precio = %s AND velocidad = %s AND ram = %s AND disco = %s
    """, (modelo, precio, velocidad, ram, disco))
    filas = cur.fetchone()
    if filas is not None:
        print("Ya existe ese equipo.")
    else:
        cur.execute("""
            INSERT INTO productos VALUES
            (%s, %s, 'pc')
        """, (fabricante, modelo))
        cur.execute("""
            INSERT INTO pc VALUES
            (%s, %s, %s, %s, %s)
        """, (modelo, velocidad, ram, disco, precio))
        conn.commit()


while True:

    menu()
    try:
        op = int(input("--> Ingrese la opcion que desea: "))
        if op == 1:
            velocidad = float(input("--> Ingrese la velocidad: "))
            ram = float(input("--> Ingrese la RAM: "))
            ejercicio1(velocidad, ram)
        if op == 2:
            modelo = input("--> Ingrese un modelo: ")
            ejercicio2(modelo)
        if op == 3:
            modelo = input("--> Ingrese un modelo: ")
            ejercicio3(modelo)
        if op == 4:
            modelo = input("--> Ingrese un modelo: ")
            fabricante = input("--> Ingrese un fabricante: ")
            velocidad = float(input("--> Ingrese velocidad: "))
            disco = float(input("--> Ingrese disco: "))
            precio = float(input("--> Ingrese precio: "))
            ram = float(input("--> Ingrese RAM: "))
            ejercicio4(fabricante, modelo, velocidad, ram, disco, precio)
        if op == 5:
            print("--> Saliendo del sistema...")
            cur.close()
            conn.close()
            break
    except Exception as e:
        print(e)
        print("--> Opcion Incorrecta.")
