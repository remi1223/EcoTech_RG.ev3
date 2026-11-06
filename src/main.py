from dominio.Gestion_departamento import GestionDepartamento
from dominio.gestionPermisos import GestionPermisos
from persistencia.crear_bd import crear_tablas
from persistencia.UsuarioDAO import UsuarioDAO
from menus.menu_dominio_empleado import mostrar_menu_empleado
from menus.menu_dominio_departamento import menu_dominio_departamento
from menus.menu_dominio_proyecto import mostrar_menu_proyecto
from menus.menu_dominio_registroTiempo import menu_dominio_registro_tiempo
from menus.menu_dominio_usuario import menu_dominio_usuario
from menus.menu_dominio_gestionPermisos import menu_dominio_gestionPermisos
from menus.menu_dominio_gestionDepartamento import menu_dominio_gestionDepartamento
from complementos.complementos import limpiar_pantalla


def main():
    usuario_dao = UsuarioDAO("ecotech.db")
    gestion_permisos = GestionPermisos()
    gestion_departamentos = GestionDepartamento()

    while True:
        limpiar_pantalla()
        print("\n===== ECOTECH SOLUTIONS =====")
        print("1. Empleado")
        print("2. Departamento")
        print("3. Proyecto")
        print("4. Registro de Tiempo")
        print("5. Usuario (demostración)")
        print("6. Gestión de Permisos (demostración)")
        print("7. Gestión de Departamento (demostración)")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            if opcion == "1":
                limpiar_pantalla()
                mostrar_menu_empleado()
            elif opcion == "2":
                limpiar_pantalla()
                menu_dominio_departamento()
            elif opcion == "3":
                limpiar_pantalla()
                mostrar_menu_proyecto()
            elif opcion == "4":
                limpiar_pantalla()
                menu_dominio_registro_tiempo()
            elif opcion == "5":
                limpiar_pantalla()
                menu_dominio_usuario(usuario_dao)
            elif opcion == "6":
                limpiar_pantalla()
                menu_dominio_gestionPermisos(usuario_dao, gestion_permisos)
            elif opcion == "7":
                limpiar_pantalla()
                menu_dominio_gestionDepartamento(gestion_departamentos)
            elif opcion == "0":
                limpiar_pantalla()
                print("¡Hasta luego! Gracias por usar EcoTech Solutions.")
                break
            else:
                print("\nOpción no válida. Ingrese un número del 0 al 7.")
                input("Presione Enter para continuar...")
        except Exception as error:
            print(f"\nOcurrió un error inesperado en la navegación: {error}")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    try:
        crear_tablas()
    except Exception as error:
        print("Error al preparar la base de datos:", error)
    else:
        main()