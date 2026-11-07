from complementos.complementos import limpiar_pantalla, validar_entero_positivo
from entradas import pedir_dato
from servicios.api import (
    obtener_datos,
    mostrar_indicador,
    convertir_clp_a_usd,
    obtener_pronostico_clima_3_dias,
    DATOS_RESPALDO
)


def menu_api():
    """
    Menú consolidado para indicadores financieros, calculadora de pagos
    y pronóstico del clima a 3 días.
    """
    while True:
        limpiar_pantalla()
        print("==================================================")
        print("         MÓDULO API - SERVICIOS Y CLIMA           ")
        print("==================================================")
        print("1. Consultar valor actual del Dólar (En vivo)")
        print("2. Calculadora de Pago Internacional (CLP -> USD)")
        print("3. Ver pronóstico del Clima (Próximos 3 días)")
        print("0. Volver al menú principal")
        print("==================================================")

        opcion = input("\nSeleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            print("Regresando al menú principal...")
            break

        elif opcion == "1":
            print("--- CONSULTA DE INDICADOR ECONÓMICO ---")
            try:
                datos, origen = obtener_datos()
                mostrar_indicador(datos, origen)
            except Exception:
                print("\n[AVISO] Cargando datos locales de respaldo...\n")
                mostrar_indicador(DATOS_RESPALDO, "datos de respaldo (local)")

            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            print("--- PAGO INTERNACIONAL (CONVERSIÓN CLP A USD) ---")
            try:
                monto_clp = pedir_dato(
                    "Ingrese el monto en Pesos Chilenos (CLP): $",
                    lambda v: validar_entero_positivo(v, "Monto CLP")
                )

                monto_usd, tasa, origen = convertir_clp_a_usd(float(monto_clp))

                print("\n" + "="*45)
                print("         RESUMEN DE TRANSACCIÓN PAGO")
                print("="*45)
                print(f" Monto ingresado  : $ {monto_clp:,.0f} CLP")
                print(f" Tasa de cambio   : $ {tasa:.2f} CLP por USD")
                print(f" Origen de tasa   : {origen}")
                print("-" * 45)
                print(f" Total a pagar    : $ {monto_usd:,.2f} USD")
                print("="*45)

            except Exception as error:
                print(f"\nError en el cálculo de conversión: {error}")

            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            print("--- PRONÓSTICO METEOROLÓGICO (PRÓXIMOS 3 DÍAS) ---")
            try:
                clima, fuente = obtener_pronostico_clima_3_dias()
                print(f"Fuente de información: {fuente}\n")
                
                print(f"{'Jornada':<15} | {'Mínima':<10} | {'Máxima':<10}")
                print("-" * 42)
                for c in clima:
                    min_str = f"{c['temp_min']} °C" if c['temp_min'] != "N/A" else "N/A"
                    max_str = f"{c['temp_max']} °C" if c['temp_max'] != "N/A" else "N/A"
                    print(f"{c['dia']:<15} | {min_str:<10} | {max_str:<10}")

            except Exception as error:
                print(f"\nError al consultar el pronóstico del clima: {error}")

            input("\nPresione Enter para continuar...")

        else:
            print("Opción no válida. Elija un número entre 0 y 3.")
            input("\nPresione Enter para continuar...")