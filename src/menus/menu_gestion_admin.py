from complementos.complementos import limpiar_pantalla
from servicios.gestion_admin import ServicioGestionAdmin


def menu_gestion_admin(usuario_sesion):
    servicio_admin = ServicioGestionAdmin("ecotech.db")

    while True:
        limpiar_pantalla()
        print("\n===== MÓDULO DE GESTIÓN ADMINISTRATIVA =====")
        print("1. Listar todas las cuentas de usuario")
        print("2. Registrar nuevo usuario administrador")
        print("3. Otorgar permiso a un usuario")
        print("4. Eliminar cuenta de usuario")
        print("5. Listar empleados (Vista Administrador)")
        print("6. Consultar Dólar Observado (API)")  # <--- OPCIÓN PARA LA API
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        try:
            if opcion == "1":
                usuarios = servicio_admin.listar_cuentas(usuario_sesion)
                if not usuarios:
                    print("No hay usuarios registrados.")
                else:
                    print("--- LISTA DE USUARIOS REGISTRADOS ---")
                    for u in usuarios:
                        permisos_str = ", ".join(u.permisos) if u.permisos else "Sin permisos"
                        print(f"ID: {u.id_usuario} | Usuario: {u.nombre_usuario} | ID Empleado: {u._empleado} | Permisos: {permisos_str}")

            elif opcion == "2":
                username = input("Nombre de usuario: ").strip()
                mail = input("Correo electrónico: ").strip()
                clave = input("Contraseña: ").strip()
                id_emp = int(input("ID del empleado asociado: "))

                nuevo = servicio_admin.crear_usuario_admin(usuario_sesion, username, mail, clave, id_emp)
                print(f"\nUsuario Admin '{nuevo.nombre_usuario}' creado exitosamente con ID {nuevo.id_usuario}.")

            elif opcion == "3":
                id_dest = int(input("ID del usuario destinatario: "))
                permiso = input("Nombre del permiso a otorgar: ").strip()
                servicio_admin.otorgar_permiso(usuario_sesion, id_dest, permiso)
                print("\nPermiso otorgado correctamente.")

            elif opcion == "4":
                id_elim = int(input("ID del usuario a eliminar: "))
                confirmar = input(f"¿Confirmar eliminación del usuario ID {id_elim}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if servicio_admin.eliminar_usuario(usuario_sesion, id_elim):
                        print("\nUsuario eliminado correctamente.")
                    else:
                        print("\nNo se pudo encontrar el usuario.")
                else:
                    print("\nEliminación cancelada.")

            elif opcion == "5":
                empleados = servicio_admin.listar_empleados(usuario_sesion)
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for emp in empleados:
                        print(emp.mostrar_datos())

            elif opcion == "6":
                print("--- CONSULTA DE INDICADOR ECONÓMICO ---")
                servicio_admin.consultar_indicador_dolar(usuario_sesion)  # <--- LLAMA A LA API

            else:
                print("Opción no válida.")

        except PermissionError as err:
            print(f"\nError de Permisos: {err}")
        except ValueError as err:
            print(f"\nError de Datos: {err}")
        except Exception as err:
            print(f"\nError al consultar API / Servicio: {err}")

        input("\nPresione Enter para continuar...")