from servicios.api import obtener_datos, mostrar_indicador, DATOS_RESPALDO
from persistencia.UsuarioDAO import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from dominio.usuario import Usuario


class ServicioGestionAdmin:

    def __init__(self, db_path: str = "ecotech.db"):
        self.usuario_dao = UsuarioDAO(db_path)

    def _exigir_admin(self, usuario_sesion: Usuario):
        if usuario_sesion is None:
            raise PermissionError("Acceso denegado: No hay una sesión activa.")
        
        if "administrar_permisos" not in usuario_sesion.permisos:
            raise PermissionError("Acceso denegado: Se requieren permisos de administrador.")

    def listar_cuentas(self, usuario_sesion: Usuario):
        self._exigir_admin(usuario_sesion)
        return self.usuario_dao.obtener_todos()

    def crear_usuario_admin(self, usuario_sesion: Usuario, username: str, mail: str, clave: str, id_empleado: int):
        self._exigir_admin(usuario_sesion)

        if self.usuario_dao.obtener_por_nombre(username) is not None:
            raise ValueError("El nombre de usuario ya está registrado.")

        nuevo_usuario = Usuario(
            nombre_usuario=username,
            mail=mail,
            contrasenia=clave,
            id_empleado=id_empleado
        )

        nuevo_usuario.agregar_permiso("administrar_permisos", usuario_sesion)

        id_creado = self.usuario_dao.crear(nuevo_usuario)
        if not id_creado:
            raise ValueError("No se pudo registrar el usuario en la base de datos.")

        return nuevo_usuario

    def otorgar_permiso(self, usuario_sesion: Usuario, id_usuario_destino: int, permiso: str):
        self._exigir_admin(usuario_sesion)

        usuario_destino = self.usuario_dao.obtener_por_id(id_usuario_destino)
        if usuario_destino is None:
            raise ValueError("El usuario destinatario no existe.")

        exito = usuario_destino.agregar_permiso(permiso, usuario_sesion)
        if not exito:
            raise ValueError("No se pudo otorgar el permiso. Permiso vacío o ya asignado.")

        return True

    def eliminar_usuario(self, usuario_sesion: Usuario, id_usuario_eliminar: int):
        self._exigir_admin(usuario_sesion)

        if usuario_sesion.id_usuario == id_usuario_eliminar:
            raise ValueError("No puedes eliminar tu propio usuario en sesión.")

        return self.usuario_dao.eliminar(id_usuario_eliminar)

    def listar_empleados(self, usuario_sesion: Usuario):
        self._exigir_admin(usuario_sesion)
        return EmpleadoDAO.listar()

    def consultar_indicador_dolar(self, usuario_sesion: Usuario):
        """
        Consulta el indicador económico. Si la API en vivo falla, 
        tarda o entrega datos no válidos, utiliza el respaldo automáticamente.
        """
        self._exigir_admin(usuario_sesion)
        
        try:
            datos, origen = obtener_datos()
            mostrar_indicador(datos, origen)
        except Exception:
            print("\n[AVISO] No se pudo procesar la respuesta en vivo de la API.")
            print("[AVISO] Cargando datos locales de respaldo para la demostración...\n")
            mostrar_indicador(DATOS_RESPALDO, "datos de respaldo (local)")