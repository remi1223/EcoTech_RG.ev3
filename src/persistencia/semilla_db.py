import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from dominio.departamento import Departamento
from persistencia.UsuarioDAO import UsuarioDAO
from dominio.usuario import Usuario


def cargar_departamentos():
    departamento_ej = [
        (1, 'Recursos Humanos', 1),
        (2, 'Finanzas', 2),
        (3, 'Tecnología', 3),
        (4, 'Marketing', 4),
        (5, 'Ventas', 5),
    ]

    for id_dept, nombre, id_gerente in departamento_ej:
        existente = DepartamentoDAO.buscar_por_id(id_dept)
        if existente is None:
            dept = Departamento(id_dept, nombre, id_gerente)
            DepartamentoDAO.insertar(dept)
            print(f"Creado departamento: {nombre}")
        else:
            print(f"Ya existe departamento: {nombre}")


def cargar_empleados(dept_demo):
    empleados_ej = [
        (1, 'Juan Pérez', 'Av. Providencia 123', '912345678', 'juan.perez@ecotech.cl', '2022-01-10', 850000, 'Desarrollador'),
        (2, 'María González', 'Av. Apoquindo 456', '923456789', 'maria.gonzalez@ecotech.cl', '2021-03-15', 1200000, 'Gerente de Recursos Humanos'),
        (3, 'Pedro Rodríguez', 'Calle Los Leones 789', '934567890', 'pedro.rodriguez@ecotech.cl', '2023-06-01', 950000, 'Analista de Sistemas'),
        (4, 'Ana Martínez', 'Av. Las Condes 321', '945678901', 'ana.martinez@ecotech.cl', '2020-09-20', 1100000, 'Contadora'),
        (5, 'Carlos Muñoz', 'Calle San Diego 654', '956789012', 'carlos.munoz@ecotech.cl', '2022-05-12', 900000, 'Técnico Informático'),
        (6, 'Camila Soto', 'Av. Irarrázaval 987', '967890123', 'camila.soto@ecotech.cl', '2023-02-18', 800000, 'Diseñadora Gráfica'),
        (7, 'Diego Torres', 'Calle Macul 147', '978901234', 'diego.torres@ecotech.cl', '2021-11-08', 1000000, 'Ingeniero de Software'),
        (8, 'Valentina Rojas', 'Av. Grecia 258', '989012345', 'valentina.rojas@ecotech.cl', '2024-01-15', 750000, 'Asistente Administrativa'),
        (9, 'Andrés Silva', 'Calle Ñuble 369', '991234567', 'andres.silva@ecotech.cl', '2020-07-22', 1300000, 'Jefe de Operaciones'),
        (10, 'Francisca López', 'Av. Vicuña Mackenna 741', '912456789', 'francisca.lopez@ecotech.cl', '2022-08-30', 850000, 'Especialista en Marketing')
    ]

    for id_emp, nombre, direccion, numero, correo, fecha, salario, cargo in empleados_ej:
        existente = EmpleadoDAO.buscar_por_id(id_emp)
        if existente is None:
            emp = Empleado(nombre, direccion, str(numero), correo, fecha, salario, cargo, id_emp)
            if hasattr(emp, 'departamento'):
                emp.departamento = dept_demo
            EmpleadoDAO.insertar(emp)
            print(f"Creado empleado: {nombre}")
        else:
            print(f"Ya existe empleado: {nombre}")


def crear_admin_inicial():
    dao_usuario = UsuarioDAO('ecotech.db')
    usuarios = dao_usuario.obtener_todos()
    
    admin_existente = next((u for u in usuarios if u.nombre_usuario == 'admin'), None)
    if admin_existente is not None:
        print("El usuario 'admin' ya existe en la base de datos.")
        return

    if EmpleadoDAO.buscar_por_id(1) is None:
        emp_admin = Empleado('Administrador Sistema', 'Oficina Central', '+56911111111', 'admin@ecotech.cl', '2026-01-01', 1000000.0, 'Gerente General', 1)
        EmpleadoDAO.insertar(emp_admin)

    admin = Usuario(
        nombre_usuario='admin',
        mail='admin@ecotech.cl',
        contrasenia='admin123',
        id_empleado=1
    )
    
    if hasattr(admin, '_permisos') and 'administrar_permisos' not in admin._permisos:
        admin._permisos.append('administrar_permisos')

    dao_usuario.crear(admin)
    print("Usuario 'admin' creado exitosamente con permiso 'administrar_permisos'.")


def poblar_base_datos():
    print("--- INICIANDO POBLAMIENTO DE BASE DE DATOS ---")
    cargar_departamentos()
    dept_demo = DepartamentoDAO.buscar_por_id(1)
    cargar_empleados(dept_demo)
    crear_admin_inicial()
    print("--- BASE DE DATOS POBLADA CON ÉXITO ---")


if __name__ == "__main__":
    poblar_base_datos()