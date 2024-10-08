from pymongo import MongoClient
from bson.objectid import ObjectId

def conectar_db(uri="mongodb://localhost:27017", db_name="biblioteca"):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        return db
    except Exception as e:
        print("Error al conectar a la base de datos: " + str(e))
        return None

def agregar_libro(db):
    titulo = input("Titulo: ")
    autor = input("Autor: ")
    anio = input("Año: ")
    libro = {
        "titulo": titulo,
        "autor": autor,
        "anio": anio
    }
    try:
        resultado = db.libros.insert_one(libro)
        print("Libro agregado con el ID: " + str(resultado.inserted_id))
    except Exception as e:
        print("Error al agregar el libro: " + str(e))

def listar_libros(db):
    try:
        libros = db.libros.find()
        print("\nListado de Libros: ")
        for libro in libros:
            print(f"ID: {libro['_id']} | Titulo: {libro['titulo']} | Autor: {libro['autor']} | Año: {libro['anio']}")
        print()
    except Exception as e:
        print("Error al listar los libros: " + str(e))

def editar_libro(db):
    listar_libros(db)
    libro_id = input("Ingrese el ID del libro a editar: ")
    try:
        libro = db.libros.find_one({"_id": ObjectId(libro_id)})
        if libro:
            print("Ingrese los nuevos valores (en blanco para mantener):")
            titulo = input(f"Título [{libro['titulo']}]: ") or libro['titulo']
            autor = input(f"Autor [{libro['autor']}]: ") or libro['autor']
            anio = input(f"Año [{libro['anio']}]: ") or libro['anio']
            nuevos_datos = {
                "titulo": titulo,
                "autor": autor,
                "anio": anio
            }
            db.libros.update_one({"_id": ObjectId(libro_id)}, {"$set": nuevos_datos})
            print("Libro actualizado exitosamente!")
        else:
            print("Ese libro no existe...")
    except Exception as e:
        print("Error al editar el libro: " + str(e))

def eliminar_libro(db):
    listar_libros(db)
    libro_id = input("Ingrese el ID del libro a eliminar: ")
    try:
        resultado = db.libros.delete_one({"_id": ObjectId(libro_id)})
        if resultado.deleted_count > 0:
            print("Libro eliminado exitosamente!")
        else:
            print("Libro no encontrado...")
    except Exception as e:
        print("Error al eliminar el libro: " + str(e))

def menu():
    print("=== GESTION DE LIBROS ===")
    print("1. Agregar libro")
    print("2. Editar libro")
    print("3. Eliminar libro")
    print("4. Listar libro")
    print("5. Salir")

def main():
    db = conectar_db()
    if db is None:
        return
    while True:
        menu()
        opcion = input("Opcion: ")
        if opcion == "1":
            agregar_libro(db)
        elif opcion == "2":
            editar_libro(db)
        elif opcion == "3":
            eliminar_libro(db)
        elif opcion == "4":
            listar_libros(db)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opcion invalida. Intente de nuevo.")

if __name__ == "__main__":
    main()