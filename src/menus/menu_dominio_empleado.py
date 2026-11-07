from datetime import datetime, date
from complementos.complementos import (
    limpiar_pantalla,
    validar_correo,
    validar_entero_positivo,
    validar_fecha_DD_MM_YYYY,
    validar_nombre,
    validar_salario,
    validar_telefono,
    validar_texto_longitud,
)
from dominio.empleado import Empleado
from entradas import pedir_dato
from persistencia.empleado_dao import EmpleadoDAO


def mostrar_menu_empleado():
    print("\n===== EMPLEADOS - ECOTECH =====")
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("0. Volver al menu principal")


def main_empleado():
    while True:
        limpiar_pantalla()
        mostrar_menu_empleado()
        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = pedir_dato(
                    "Nombre (máx 50 caracteres): ",
                    lambda v: validar_nombre(v, 50),
                )
                direccion = pedir_dato(
                    "Dirección (máx 100 caracteres): ",
                    lambda v: validar_texto_longitud(v, 100, "Dirección"),
                )
                numero = pedir_dato(
                    "Número de teléfono (ej. +56912345678): ", validar_telefono
                )
                correo = pedir_dato(
                    "Correo electrónico (máx 80 caracteres): ",
                    lambda v: validar_correo(v, 80),
                )

                fecha_str = pedir_dato(
                    "Fecha de contrato (DD-MM-YYYY): ", validar_fecha_DD_MM_YYYY
                )
                try:
                    fecha_contrato = datetime.strptime(fecha_str, "%d-%m-%Y").date()
                except ValueError:
                    raise ValueError("La fecha ingresada no es válida. Use DD-MM-YYYY.")

                salario = pedir_dato("Salario: ", validar_salario)
                cargo = pedir_dato(
                    "Cargo (máx 40 caracteres): ",
                    lambda v: validar_texto_longitud(v, 40, "Cargo"),
                )

                empleado = Empleado(
                    nombre,
                    direccion,
                    numero,
                    correo,
                    fecha_contrato,
                    salario,
                    cargo,
                )
                EmpleadoDAO.insertar(empleado)
                print(
                    f"\nEmpleado registrado exitosamente con ID: {empleado._id}"
                )
            except Exception as error:
                print("\nError al registrar el empleado:", error)
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            try:
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for empleado in empleados:
                        print(empleado.mostrar_datos())
            except Exception as error:
                print("Error al listar empleados:", error)
            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            try:
                id_empleado = pedir_dato(
                    "ID del empleado: ",
                    lambda v: validar_entero_positivo(v, "ID Empleado"),
                )
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                else:
                    print(empleado.mostrar_datos())
                    print("Teléfono:", empleado._numero)
                    print("Fecha de contrato:", empleado._fecha_contrato)
                    print("Salario:", empleado.ver_salario())
            except Exception as error:
                print("Error al buscar el empleado:", error)
            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            try:
                id_empleado = pedir_dato(
                    "ID del empleado a actualizar: ",
                    lambda v: validar_entero_positivo(v, "ID Empleado"),
                )
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                print("Deja el campo vacío si no quieres modificarlo.")

                nom_in = input(f"Nombre [{empleado._nombre}]: ").strip()
                nombre = (
                    validar_nombre(nom_in, 50) if nom_in else empleado._nombre
                )

                dir_in = input(f"Dirección [{empleado._direccion}]: ").strip()
                direccion = (
                    validar_texto_longitud(dir_in, 100, "Dirección")
                    if dir_in
                    else empleado._direccion
                )

                num_in = input(f"Teléfono [{empleado._numero}]: ").strip()
                numero = (
                    validar_telefono(num_in) if num_in else empleado._numero
                )

                cor_in = input(f"Correo [{empleado._correo}]: ").strip()
                correo = (
                    validar_correo(cor_in, 80) if cor_in else empleado._correo
                )

                fec_in = input(
                    f"Fecha contrato [{empleado._fecha_contrato}] (DD-MM-YYYY): "
                ).strip()
                
                if fec_in:
                    try:
                        fecha = datetime.strptime(fec_in, "%d-%m-%Y").date()
                    except ValueError:
                        raise ValueError("Formato de fecha inválido. Use DD-MM-YYYY.")
                else:
                    fecha = empleado._fecha_contrato

                sal_in = input(f"Salario [{empleado._salario}]: ").strip()
                salario = (
                    validar_salario(sal_in) if sal_in else empleado._salario
                )

                car_in = input(f"Cargo [{empleado._cargo}]: ").strip()
                cargo = (
                    validar_texto_longitud(car_in, 40, "Cargo")
                    if car_in
                    else empleado._cargo
                )

                actualizado = Empleado(
                    nombre=nombre,
                    direccion=direccion,
                    numero=numero,
                    correo=correo,
                    fecha_contrato=fecha,
                    salario=salario,
                    cargo=cargo,
                    id=empleado._id,
                )
                if EmpleadoDAO.actualizar(actualizado):
                    print("\nEmpleado actualizado correctamente.")
                else:
                    print("\nNo se detectaron cambios guardados.")
            except Exception as error:
                print("\nError al actualizar el empleado:", error)
            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            try:
                id_empleado = pedir_dato(
                    "ID del empleado a eliminar: ",
                    lambda v: validar_entero_positivo(v, "ID Empleado"),
                )
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                print(empleado.mostrar_datos())
                confirmar = (
                    input("Confirmar eliminación (s/n): ").lower().strip()
                )
                if confirmar == "s":
                    if EmpleadoDAO.eliminar(id_empleado):
                        print("Empleado eliminado.")
                    else:
                        print("No se pudo eliminar el empleado.")
                else:
                    print("Eliminación cancelada.")
            except Exception as error:
                print("Error al eliminar el empleado:", error)
            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            return
        else:
            print("Opción no válida.")
            input("\nPresione Enter para continuar...")