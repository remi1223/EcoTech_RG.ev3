from complementos.complementos import (
    limpiar_pantalla,
    validar_correo,
    validar_texto_longitud,
    validar_entero_positivo
)
from getpass import getpass
import bcrypt
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from entradas import pedir_dato


def menu_dominio_usuario(dao_or_class):
    """
    Menú interactivo para administrar el Dominio de Usuarios.
    Garantiza salida limpia con la opción 0 y manejo defensivo de atributos.
    """
    if isinstance(dao_or_class, type):
        usuario_dao = dao_or_class()
    else:
        usuario_dao = dao_or_class

    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO USUARIO =====")
        print("1. Crear usuario para un empleado")
        print("2. Autenticar usuario")
        print("3. Cambiar contraseña")
        print("4. Listar usuarios")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            print("Regresando al menú principal...")
            return

        elif opcion == "1":
            try:
                id_empleado = pedir_dato("ID del empleado existente: ", lambda v: validar_entero_positivo(v, "ID Empleado"))
                
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("\nEmpleado no encontrado. Regístrelo primero en el CRUD.")
                    input("\nPresione Enter para continuar...")
                    continue

                nombre = pedir_dato("Nombre de usuario (máx 30 caracteres): ", lambda v: validar_texto_longitud(v, 30, "Usuario"))
                mail = pedir_dato("Correo del usuario: ", lambda v: validar_correo(v, 80))

                contrasenia = getpass(f"Contraseña (mínimo {Usuario.MIN_CLAVE} caracteres): ")
                if len(contrasenia) < Usuario.MIN_CLAVE:
                    print(f"\nLa contraseña debe tener al menos {Usuario.MIN_CLAVE} caracteres.")
                    input("\nPresione Enter para continuar...")
                    continue

                clave_bytes = contrasenia.encode('utf-8')
                sal = bcrypt.gensalt()
                clave_hasheada_bytes = bcrypt.hashpw(clave_bytes, sal)
                clave_hasheada_str = clave_hasheada_bytes.decode('utf-8')

                # Asignación defensiva del ID del empleado
                id_emp_val = getattr(empleado, '_id', getattr(empleado, 'id', getattr(empleado, 'id_empleado', id_empleado)))

                nuevo_usuario = Usuario(
                    nombre_usuario=nombre,
                    mail=mail,
                    contrasenia=clave_hasheada_str,
                    id_empleado=id_emp_val
                )

                todos = usuario_dao.obtener_todos()
                if len(todos) == 0:
                    if hasattr(nuevo_usuario, '_permisos'):
                        nuevo_usuario._permisos.append("administrar_permisos")
                    elif hasattr(nuevo_usuario, 'permisos'):
                        nuevo_usuario.permisos.append("administrar_permisos")
                    print("\nPrimer usuario: asignado como administrador.")

                id_generado = usuario_dao.crear(nuevo_usuario)
                
                if id_generado:
                    print(f"\n¡Usuario guardado con éxito! ID asignado: {id_generado}")
                else:
                    print("\nNo se pudo crear el usuario. Verifique si el usuario o empleado ya está registrado.")

            except Exception as error:
                print("\nError inesperado al crear usuario:", error)

            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            try:
                nombre = input("Nombre de usuario: ").strip()
                contrasenia = getpass("Contraseña: ")
                usuario = usuario_dao.obtener_por_nombre(nombre)

                if usuario:
                    pwd = getattr(usuario, 'contrasenia', getattr(usuario, '_contrasenia', None))
                    if pwd and bcrypt.checkpw(contrasenia.encode('utf-8'), pwd.encode('utf-8')):
                        usr_nombre = getattr(usuario, 'nombre_usuario', getattr(usuario, '_nombre_usuario', nombre))
                        print(f"\n¡Autenticación exitosa! Bienvenido, {usr_nombre}.")
                    else:
                        print("\nCredenciales incorrectas. Verifique el nombre o contraseña.")
                else:
                    print("\nCredenciales incorrectas. Verifique el nombre o contraseña.")
            except Exception as error:
                print("\nError al autenticar:", error)

            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            try:
                nombre = input("Nombre de usuario: ").strip()
                usuario = usuario_dao.obtener_por_nombre(nombre)

                if usuario:
                    clave_actual = getpass("Contraseña actual: ")
                    pwd_actual = getattr(usuario, 'contrasenia', getattr(usuario, '_contrasenia', None))
                    
                    if pwd_actual and bcrypt.checkpw(clave_actual.encode('utf-8'), pwd_actual.encode('utf-8')):
                        nueva_clave = getpass(f"Nueva contraseña (mínimo {Usuario.MIN_CLAVE} caracteres): ")
                        if len(nueva_clave) >= Usuario.MIN_CLAVE:
                            sal = bcrypt.gensalt()
                            nueva_hasheada = bcrypt.hashpw(nueva_clave.encode('utf-8'), sal).decode('utf-8')
                            
                            if hasattr(usuario, 'contrasenia'):
                                usuario.contrasenia = nueva_hasheada
                            elif hasattr(usuario, '_contrasenia'):
                                usuario._contrasenia = nueva_hasheada
                                
                            usuario_dao.actualizar(usuario)
                            print("\n¡Contraseña actualizada exitosamente!")
                        else:
                            print(f"\nLa nueva contraseña debe tener al menos {Usuario.MIN_CLAVE} caracteres.")
                    else:
                        print("\nLa contraseña actual es incorrecta.")
                else:
                    print(f"\nEl usuario '{nombre}' no existe.")
            except Exception as error:
                print("\nError al cambiar contraseña:", error)

            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            try:
                usuarios = usuario_dao.obtener_todos()
                print("--- LISTA DE USUARIOS REGISTRADOS ---")
                if usuarios:
                    for u in usuarios:
                        correo = getattr(u, 'mail', getattr(u, 'email', getattr(u, '_mail', getattr(u, '_email', 'N/A'))))
                        id_usr = getattr(u, 'id_usuario', getattr(u, '_id_usuario', getattr(u, 'id', 'N/A')))
                        nombre_usr = getattr(u, 'nombre_usuario', getattr(u, '_nombre_usuario', getattr(u, 'username', 'N/A')))
                        id_emp = getattr(u, 'id_empleado', getattr(u, '_id_empleado', 'N/A'))
                        
                        print(f"ID: {id_usr} | Usuario: {nombre_usr} | Email: {correo} | Empleado ID: {id_emp}")
                else:
                    print("No hay usuarios registrados en la base de datos.")
            except Exception as error:
                print("\nError al listar usuarios:", error)

            input("\nPresione Enter para continuar...")

        else:
            print("Opción no válida. Por favor elija un número de la lista (0 al 4).")
            input("\nPresione Enter para continuar...")