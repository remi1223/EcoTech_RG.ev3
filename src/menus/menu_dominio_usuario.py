from complementos.complementos import limpiar_pantalla
from getpass import getpass

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO


def menu_dominio_usuario(usuario_dao):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO USUARIO =====")
        print("1. Crear usuario para un empleado")
        print("2. Autenticar usuario")
        print("3. Cambiar contrasena")
        print("4. Listar usuarios")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            try:
                id_empleado = int(input("ID del empleado existente: "))
                
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado. Registrelo primero en el CRUD.")
                    input("\nPresione Enter para continuar...")
                    continue

                nombre = input("Nombre de usuario: ").strip()
                mail = input("Correo del usuario: ").strip()
                if nombre == "" or "@" not in mail or "." not in mail:
                    print("Ingrese un nombre y un correo validos.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia = getpass(f"Contrasena (minimo {Usuario.MIN_CLAVE} caracteres): ")
                if len(contrasenia) < Usuario.MIN_CLAVE:
                    print(f"La contrasena debe tener al menos {Usuario.MIN_CLAVE} caracteres.")
                    input("\nPresione Enter para continuar...")
                    continue

                nuevo_usuario = Usuario(
                    nombre_usuario=nombre,
                    mail=mail,
                    contrasenia=contrasenia,
                    id_empleado=empleado._id
                )

                todos = usuario_dao.obtener_todos()
                if len(todos) == 0:
                    nuevo_usuario._permisos.append("administrar_permisos")
                    print("Primer usuario: asignado como administrador.")

                id_generado = usuario_dao.crear(nuevo_usuario)
                
                if id_generado:
                    print(f"Usuario guardado en la base de datos con éxito. ID asignado: {id_generado}")
                else:
                    print("No se pudo crear el usuario. Verifique si el nombre de usuario o el empleado ya están registrados.")

            except ValueError as ve:
                print("Error en los datos ingresados:", ve)
            except Exception as error:
                print("Error inesperado al crear usuario:", error)

        elif opcion in ("2", "3"):
            try:
                id_usuario = int(input("ID del usuario: "))
                usuario = usuario_dao.obtener_por_id(id_usuario)
                
                if usuario is None:
                    print("Usuario no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                contrasenia_actual = getpass("Contrasena actual: ")

                if opcion == "2":
                    if usuario.autenticar(contrasenia_actual):
                        print("Autenticacion correcta.")
                    else:
                        print("Contrasena incorrecta.")

                elif opcion == "3":
                    nueva_clave = getpass("Nueva contrasena: ")
                    
                    if usuario.cambiar_contrasenia(contrasenia_actual, nueva_clave):
                        if usuario_dao.actualizar(usuario):
                            print("Contrasena actualizada correctamente en la base de datos.")
                        else:
                            print("Error al guardar la nueva contrasena en la base de datos.")
                    else:
                        print("No se pudo cambiar la contrasena. Verifique que coincida con la actual y cumpla la longitud minima.")

            except ValueError:
                print("El ID debe ser un entero positivo.")

        elif opcion == "4":
            usuarios = usuario_dao.obtener_todos()
            if not usuarios:
                print("Aun no hay usuarios registrados en la base de datos.")
            else:
                for u in usuarios:
                    permisos_str = ", ".join(u.permisos) if u.permisos else "Sin permisos"
                    print(
                        f"ID: {u.id_usuario} | Usuario: {u.nombre_usuario} | Mail: {u._mail} | ID Empleado: {u._empleado} | Permisos: {permisos_str}"
                    )

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")