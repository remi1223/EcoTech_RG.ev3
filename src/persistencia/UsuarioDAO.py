from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            id_usuario=fila[0],
            nombre_usuario=fila[1],
            contrasenia=fila[2],
            mail=fila[3],
            rol=fila[4],
            activo=bool(fila[5])
        )
    
    def insertar(usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "INSERT INTO usuario "
                "(username, clave, correo, rol, activo) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca})"
            )
            cursor.execute(sql, (
                usuario._nombre_usuario,
                usuario._contrasenia,
                usuario._mail,
                usuario._rol,
                usuario._activo
            ))
            conexion.commit()
            usuario._id = cursor.lastrowid
            return usuario
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def actualizar(usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "UPDATE usuario SET "
                f"username = {marca}, clave = {marca}, correo = {marca}, "
                f"rol = {marca}, activo = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(sql, (
                usuario._nombre_usuario,
                usuario._contrasenia,
                usuario._correo,
                usuario._rol,
                usuario._activo,
                usuario._id_usuario
            ))
            actualizado = cursor.rowcount > 0
            conexion.commit()
            return actualizado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def eliminar(id_usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM usuario WHERE id = {marca}"
            cursor.execute(sql, (id_usuario,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def buscar_por_id(id_usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, username, clave, correo, rol, activo "
                f"FROM usuario WHERE id = {marca}"
            )
            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return UsuarioDAO._fila_a_usuario(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, username, clave, correo, rol, activo "
                f"FROM usuario WHERE username = {marca}"
            )
            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return UsuarioDAO._fila_a_usuario(fila)
        finally:
            if conexion:
                conexion.close()

    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, username, clave, correo, rol, activo FROM usuario"
            )
            filas = cursor.fetchall()
            usuarios = []
            for fila in filas:
                usuarios.append(UsuarioDAO._fila_a_usuario(fila))
            return usuarios
        finally:
            if conexion:
                conexion.close()