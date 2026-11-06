from complementos.complementos import (limpiar_pantalla, validar_texto_longitud, validar_fecha_YYYY_MM_DD, validar_entero_positivo)
from datetime import date
from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDao
from entradas import pedir_dato


def mostrar_menu_proyecto():
    print("\n===== PROYECTOS - ECOTECH =====")
    print("1. Registrar Proyecto")
    print("2. Listar Proyectos")
    print("3. Buscar Proyecto")
    print("4. Actualizar Proyecto")
    print("5. Eliminar Proyecto")
    print("0. Volver al menu principal")


def main_proyecto():
    while True:
        limpiar_pantalla()
        mostrar_menu_proyecto()
        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = pedir_dato("Nombre del proyecto (máx 60 caracteres): ", lambda v: validar_texto_longitud(v, 60, "Nombre"))
                fecha_str = pedir_dato("Fecha de inicio (YYYY-MM-DD): ", validar_fecha_YYYY_MM_DD)
                fecha_inicio = date.fromisoformat(fecha_str)
                descripcion = pedir_dato("Descripción (máx 200 caracteres): ", lambda v: validar_texto_longitud(v, 200, "Descripción"))

                proyecto = Proyecto(nombre, fecha_inicio, descripcion)
                ProyectoDao.insertar(proyecto)
                print(f"\nProyecto registrado con ID: {proyecto._id_proyecto}")
            except Exception as error:
                print("\nError al registrar proyecto:", error)

        elif opcion == "2":
            try:
                proyectos = ProyectoDao.listar()
                if not proyectos:
                    print("No hay proyectos registrados.")
                else:
                    for p in proyectos:
                        print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except Exception as error:
                print("Error al listar proyectos:", error)

        elif opcion == "3":
            try:
                id_proyecto = pedir_dato("ID del proyecto: ", lambda v: validar_entero_positivo(v, "ID Proyecto"))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                else:
                    print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except Exception as error:
                print("Error al buscar proyecto:", error)

        elif opcion == "4":
            try:
                id_proyecto = pedir_dato("ID del proyecto a actualizar: ", lambda v: validar_entero_positivo(v, "ID Proyecto"))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                nom_in = input(f"Nombre [{p._nombre}]: ").strip()
                nombre = validar_texto_longitud(nom_in, 60, "Nombre") if nom_in else p._nombre

                fec_in = input(f"Fecha de inicio [{p._fecha_inicio}] (YYYY-MM-DD): ").strip()
                fecha = date.fromisoformat(validar_fecha_YYYY_MM_DD(fec_in)) if fec_in else p._fecha_inicio

                desc_in = input(f"Descripción [{p._descripcion}]: ").strip()
                descripcion = validar_texto_longitud(desc_in, 200, "Descripción") if desc_in else p._descripcion

                actualizado = Proyecto(
                    nombre=nombre,
                    fecha_inicio=fecha,
                    descripcion=descripcion,
                    id_proyecto=p._id_proyecto
                )
                if ProyectoDao.actualizar(actualizado):
                    print("\nProyecto actualizado correctamente.")
                else:
                    print("\nNo se detectaron cambios guardados.")
            except Exception as error:
                print("\nError al actualizar proyecto:", error)

        elif opcion == "5":
            try:
                id_proyecto = pedir_dato("ID del proyecto a eliminar: ", lambda v: validar_entero_positivo(v, "ID Proyecto"))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                confirmar = input(f"¿Eliminar {p._nombre}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if ProyectoDao.eliminar(id_proyecto):
                        print("Proyecto eliminado.")
                    else:
                        print("No se pudo eliminar el proyecto.")
                else:
                    print("Eliminación cancelada.")
            except Exception as error:
                print("Error al eliminar proyecto:", error)

        elif opcion == "0":
            return
        else:
            print("Opción no válida.")
        input("\nPresione Enter para continuar...")