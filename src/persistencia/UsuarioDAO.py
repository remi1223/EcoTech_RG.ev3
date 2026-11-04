import sqlite3
from typing import Optional, List
from dominio.usuario import Usuario


class UsuarioDAO:

    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Establece conexión con la BD y habilita la verificación de Foreign Keys."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def crear(self, usuario: Usuario) -> Optional[int]:
        """Inserta un objeto Usuario en la BD. Asigna el ID generado al objeto."""
        sql = """
            INSERT INTO usuario (nombre_usuario, password_hash, id_empleado)
            VALUES (?, ?, ?);
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    sql, 
                    (usuario.nombre_usuario, usuario._contrasenia_hash, usuario._empleado)
                )
                conn.commit()
                # Actualizamos el id privado en la instancia cargada
                usuario._id_usuario = cursor.lastrowid
                return usuario.id_usuario
        except sqlite3.IntegrityError as e:
            print(f"Error al registrar usuario (posible duplicado de nombre o empleado): {e}")
            return None

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        """Recupera un registro por ID y reconstruye la instancia de Usuario."""
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado FROM usuario WHERE id = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
        return None

    def obtener_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        """Recupera un usuario por su nombre de usuario normalizado."""
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado FROM usuario WHERE nombre_usuario = ?;"
        
        # Opcional: normalizar la entrada antes de buscar
        try:
            nombre_busqueda = Usuario.normalizar_usuario(nombre_usuario)
        except (TypeError, ValueError):
            return None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (nombre_busqueda,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
        return None

    def obtener_todos(self) -> List[Usuario]:
        """Retorna una lista con todas las instancias de Usuario."""
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado FROM usuario;"
        usuarios = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                usuarios.append(self._mapear_a_objeto(row))
        return usuarios

    def actualizar_contrasenia(self, usuario: Usuario) -> bool:
        """Persiste el cambio de contraseña del objeto Usuario en la BD."""
        if usuario.id_usuario is None:
            raise ValueError("El usuario debe estar registrado en la BD para actualizarse.")

        sql = "UPDATE usuario SET password_hash = ? WHERE id = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (usuario._contrasenia_hash, usuario.id_usuario))
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, id_usuario: int) -> bool:
        """Elimina un usuario por su ID primario."""
        sql = "DELETE FROM usuario WHERE id = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0

    def _mapear_a_objeto(self, row: tuple) -> Usuario:
        """
        Método auxiliar para reconstruir un objeto Usuario desde una tupla de la BD
        sin regenerar/re-hashear la contraseña.
        """
        id_db, nombre, hash_db, id_emp = row

        usuario = Usuario.__new__(Usuario)
        usuario._id_usuario = id_db
        usuario._nombre_usuario = nombre
        usuario._mail = None  # No está en la tabla de BD actual
        usuario._empleado = id_emp
        usuario._permisos = []
        usuario._contrasenia_hash = hash_db
        
        return usuario