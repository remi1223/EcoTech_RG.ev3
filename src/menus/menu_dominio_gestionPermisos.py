from complementos.complementos import limpiar_pantalla
from getpass import getpass
from persistencia.UsuarioDAO import UsuarioDAO


def menu_dominio_gestionPermisos(dao_usuario: UsuarioDAO, gestion_permisos):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO GESTION PERMISOS (DEMOSTRACION) =====")
        print("1. Ver usuarios y permisos")
        print("2. Otorgar permiso")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            usuarios = dao_usuario.obtener_todos()
            if not usuarios:
                print("No hay usuarios registrados en la BD.")
            else:
                for usuario in usuarios:
                    nombre = getattr(usuario, "_nombre_usuario", "Sin nombre")
                    permisos = getattr(usuario, "_permisos", [])
                    print(
                        f"ID: {usuario._id_usuario} | Usuario: {nombre} | Permisos: {', '.join(permisos) or 'Sin permisos'}"
                    )

        elif opcion == "2":
            try:
                id_encargado = int(input("ID del usuario encargado: "))
                encargado = dao_usuario.obtener_por_id(id_encargado)
                if encargado is None:
                    print("Encargado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia = getpass("Contrasena del encargado: ")
                if not encargado.autenticar(contrasenia):
                    print("Autenticacion incorrecta.")
                    input("\nPresione Enter para continuar...")
                    continue

                id_usuario = int(
                    input("ID del usuario que recibira el permiso: ")
                )
                usuario = dao_usuario.obtener_por_id(id_usuario)
                if usuario is None:
                    print("Usuario destinatario no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                permiso = input("Nombre del permiso: ").strip()
                if gestion_permisos.otorgar_permiso(
                    encargado, usuario, permiso
                ):
                    print("Permiso otorgado correctamente.")
                else:
                    print(
                        "No se pudo otorgar: encargado sin autorizacion, permiso vacio o repetido."
                    )

            except ValueError:
                print("Los ID deben ser numericos.")

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")