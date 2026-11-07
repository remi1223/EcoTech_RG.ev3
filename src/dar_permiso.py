from persistencia.UsuarioDAO import UsuarioDAO

dao = UsuarioDAO("ecotech.db")
user = dao.obtener_por_nombre("admin")

if user:
    permisos_actuales = user.permisos if hasattr(user, 'permisos') and user.permisos else []
    if "administrar_permisos" not in permisos_actuales:
        permisos_actuales.append("administrar_permisos")
        user._permisos = permisos_actuales
        dao.actualizar(user)
        print("Permiso 'administrar_permisos' asignado con éxito a 'admin'.")
    else:
        print("El usuario 'admin' ya tiene el permiso asignado.")
else:
    print("No se encontró el usuario 'admin' en la base de datos.")