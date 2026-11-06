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

def menu_dominio_usuario(UsuarioDAO):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO USUARIO =====")
        print("1. Crear usuario para un empleado")
        print("2. Autenticar usuario")
        print("3. Cambiar contraseña")
        print("4. Listar usuarios")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            try:
                id_empleado = pedir_dato("ID del empleado existente: ", lambda v: validar_entero_positivo(v, "ID Empleado"))
                
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado. Regístrelo primero en el CRUD.")
                    input("\nPresione Enter para continuar...")
                    continue

                nombre = pedir_dato("Nombre de usuario (máx 30 caracteres): ", lambda v: validar_texto_longitud(v, 30, "Usuario"))
                mail = pedir_dato("Correo del usuario: ", lambda v: validar_correo(v, 80))

                contrasenia = getpass(f"Contraseña (mínimo {Usuario.MIN_CLAVE} caracteres): ")
                if len(contrasenia) < Usuario.MIN_CLAVE:
                    print(f"La contraseña debe tener al menos {Usuario.MIN_CLAVE} caracteres.")
                    input("\nPresione Enter para continuar...")
                    continue

                clave_bytes = contrasenia.encode('utf-8')
                sal = bcrypt.gensalt()
                clave_hasheada_bytes = bcrypt.hashpw(clave_bytes, sal)
                clave_hasheada_str = clave_hasheada_bytes.decode('utf-8')

                nuevo_usuario = Usuario(
                    nombre_usuario=nombre,
                    mail=mail,
                    contrasenia=clave_hasheada_str,
                    id_empleado=empleado._id
                )

                todos = UsuarioDAO.obtener_todos()
                if len(todos) == 0:
                    nuevo_usuario._permisos.append("administrar_permisos")
                    print("Primer usuario: asignado como administrador.")

                id_generado = UsuarioDAO.crear(nuevo_usuario)
                
                if id_generado:
                    print(f"\nUsuario guardado con éxito. ID asignado: {id_generado}")
                else:
                    print("\nNo se pudo crear el usuario. Verifique si el usuario o empleado ya está registrado.")

            except Exception as error:
                print("\nError inesperado al crear usuario:", error)