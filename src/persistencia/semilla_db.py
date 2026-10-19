from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from dominio.departamento import Departamento

def cargar_empleados(departamento_demo):

    empleados_ej = [
    (1, 'Juan Pérez', 'Av. Providencia 123', 912345678, 'juan.perez@ecotech.com', '2022-01-10', 850000, 'Desarrollador'),
    (2, 'María González', 'Av. Apoquindo 456', 923456789, 'maria.gonzalez@ecotech.com', '2021-03-15', 1200000, 'Gerente de Recursos Humanos'),
    (3, 'Pedro Rodríguez', 'Calle Los Leones 789', 934567890, 'pedro.rodriguez@ecotech.com', '2023-06-01', 950000, 'Analista de Sistemas'),
    (4, 'Ana Martínez', 'Av. Las Condes 321', 945678901, 'ana.martinez@ecotech.com', '2020-09-20', 1100000, 'Contadora'),
    (5, 'Carlos Muñoz', 'Calle San Diego 654', 956789012, 'carlos.munoz@ecotech.com', '2022-05-12', 900000, 'Técnico Informático'),
    (6, 'Camila Soto', 'Av. Irarrázaval 987', 967890123, 'camila.soto@ecotech.com', '2023-02-18', 800000, 'Diseñadora Gráfica'),
    (7, 'Diego Torres', 'Calle Macul 147', 978901234, 'diego.torres@ecotech.com', '2021-11-08', 1000000, 'Ingeniero de Software'),
    (8, 'Valentina Rojas', 'Av. Grecia 258', 989012345, 'valentina.rojas@ecotech.com', '2024-01-15', 750000, 'Asistente Administrativa'),
    (9, 'Andrés Silva', 'Calle Ñuble 369', 991234567, 'andres.silva@ecotech.com', '2020-07-22', 1300000, 'Jefe de Operaciones'),
    (10, 'Francisca López', 'Av. Vicuña Mackenna 741', 912456789, 'francisca.lopez@ecotech.com', '2022-08-30', 850000, 'Especialista en Marketing'),
    (11, 'Sebastián Díaz', 'Calle La Florida 852', 923567890, 'sebastian.diaz@ecotech.com', '2023-04-05', 950000, 'Analista de Datos'),
    (12, 'Daniela Castro', 'Av. Matta 963', 934678901, 'daniela.castro@ecotech.com', '2021-06-14', 900000, 'Encargada de Compras'),
    (13, 'Felipe Morales', 'Calle Catedral 159', 945789012, 'felipe.morales@ecotech.com', '2024-02-01', 780000, 'Soporte Técnico'),
    (14, 'Paula Herrera', 'Av. Santa Rosa 357', 956890123, 'paula.herrera@ecotech.com', '2020-12-10', 1400000, 'Gerente de Finanzas'),
    (15, 'Nicolás Flores', 'Calle Portugal 468', 967901234, 'nicolas.flores@ecotech.com', '2022-10-03', 1050000, 'Administrador de Redes'),
    (16, 'Javiera Contreras', 'Av. Manuel Montt 579', 978012345, 'javiera.contreras@ecotech.com', '2023-09-11', 820000, 'Ejecutiva de Ventas'),
    (17, 'Matías Vargas', 'Calle Recoleta 681', 989123456, 'matias.vargas@ecotech.com', '2021-02-25', 1150000, 'Ingeniero Ambiental'),
    (18, 'Constanza Reyes', 'Av. Independencia 792', 991345678, 'constanza.reyes@ecotech.com', '2024-05-06', 760000, 'Asistente de Recursos Humanos'),
    (19, 'Tomás Fernández', 'Calle San Pablo 813', 912567890, 'tomas.fernandez@ecotech.com', '2022-04-19', 980000, 'Desarrollador Backend'),
    (20, 'Isidora Ramírez', 'Av. Brasil 924', 923678901, 'isidora.ramirez@ecotech.com', '2023-07-17', 870000, 'Analista de Calidad')
]
    
    for id_empleado, nombre in empleados_ej:
        existente = EmpleadoDAO.buscar_por_id(id_empleado)
        if existente is not None:
            print(f"Ya existe: {id_empleado}")
        continue
    
    empleado = Empleado(id_empleado, nombre, departamento_demo)
    EmpleadoDAO.insertar(empleado)
    print(f"Creado: {empleado}")

def cargar_departamento():

    departamento_ej = [(1, 'Recursos Humanos', 'Carlos Muñoz', 1),
    (2, 'Finanzas', 'María González', 2),
    (3, 'Tecnología', 'Pedro Rodríguez', 3),
    (4, 'Marketing', 'Ana Martínez', 4),
    (5, 'Ventas', 'Jorge Pérez', 5),]
    
    for id_departamento, nombre, id_genrente in departamento_ej:
        existente = DepartamentoDAO.buscar_por_id(id_departamento)
        if existente is not None:
            print(f"Ya existe: {departamento}")
        continue
    
    departamento = Departamento(id_departamento, nombre, id_genrente)
    DepartamentoDAO.insertar(departamento)
    print(f"Creado: {id_departamento}")