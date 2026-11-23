"""Laboratorio de eficiencia: mide 4 algoritmos con n = 1000, 2000, 4000, 8000.

Uso:
    python main.py            -> imprime la tabla de tiempos y razones (R4)
    python main.py --perfil   -> además ejecuta cProfile sobre todo el laboratorio
"""
import random
import sys
import time

from algoritmos import busqueda_binaria, busqueda_lineal, insercion, merge_sort

TAMANOS = [1000, 2000, 4000, 8000]
REPETICIONES = 5        # se toma el MÍNIMO de varias corridas para reducir el ruido del sistema
BUSQUEDAS = 1000        # una sola búsqueda dura microsegundos: se cronometra un lote de búsquedas
AUSENTE = -1            # valor que nunca aparece (datos en 1..10^6): fuerza el peor caso
SEMILLA = 2026          # semilla fija para que los resultados sean reproducibles


def medir(funcion, datos):
    """Devuelve el tiempo en segundos que tarda funcion(datos) (plantilla del enunciado)."""
    copia = list(datos)
    inicio = time.perf_counter()
    funcion(copia)
    return time.perf_counter() - inicio


def medir_min(funcion, datos):
    """Repite la medición REPETICIONES veces y devuelve el menor tiempo."""
    return min(medir(funcion, datos) for _ in range(REPETICIONES))


# --- Envoltorios para las búsquedas: buscan un lote de objetivos ausentes (peor caso) ---
def lote_lineal(lista):
    for _ in range(BUSQUEDAS // 10):   # la lineal es lenta: 100 búsquedas bastan
        busqueda_lineal(lista, AUSENTE)


def lote_binaria(lista_ordenada):
    for _ in range(BUSQUEDAS * 10):    # la binaria es muy rápida: 10 000 búsquedas
        busqueda_binaria(lista_ordenada, AUSENTE)


def verificar():
    """Comprueba que los algoritmos funcionen antes de medirlos."""
    datos = [random.randint(1, 100) for _ in range(300)]
    esperado = sorted(datos)
    assert insercion(list(datos)) == esperado, "inserción falla"
    assert merge_sort(list(datos)) == esperado, "merge sort falla"
    objetivo = datos[150]
    assert datos[busqueda_lineal(datos, objetivo)] == objetivo, "búsqueda lineal falla"
    assert esperado[busqueda_binaria(esperado, objetivo)] == objetivo, "búsqueda binaria falla"
    assert busqueda_lineal(datos, AUSENTE) == -1 and busqueda_binaria(esperado, AUSENTE) == -1


def laboratorio():
    random.seed(SEMILLA)
    verificar()
    print("Algoritmos verificados correctamente.\n")

    datos_por_n = {n: [random.randint(1, 10**6) for _ in range(n)] for n in TAMANOS}
    # La binaria exige lista ordenada: se ordena con el algoritmo eficiente del R2 (Merge Sort).
    # Este ordenamiento previo NO se incluye en el tiempo de la búsqueda.
    ordenados = {n: merge_sort(list(d)) for n, d in datos_por_n.items()}

    pruebas = [
        ("Inserción  O(n^2)", insercion, datos_por_n, "4.00"),
        ("Merge Sort  O(n log n)", merge_sort, datos_por_n, "~2.2"),
        (f"Búsqueda lineal O(n)  [{BUSQUEDAS // 10} búsquedas]", lote_lineal, datos_por_n, "2.00"),
        (f"Búsqueda binaria O(log n)  [{BUSQUEDAS * 10} búsquedas]", lote_binaria, ordenados, "~1.1"),
    ]

    resumen = []
    for nombre, funcion, entradas, esperada in pruebas:
        print(f"== {nombre}  (razón teórica {esperada}) ==")
        print(f"{'n':>6} {'tiempo(s)':>12} {'razon':>8}")
        anterior = None
        fila = []
        for n in TAMANOS:
            t = medir_min(funcion, entradas[n])
            razon = f"{t / anterior:.2f}" if anterior else "-"
            print(f"{n:>6} {t:>12.5f} {razon:>8}")
            fila.append((t, razon))
            anterior = t
        resumen.append((nombre.split(" O(")[0].strip(), esperada, fila))
        print()

    # Tabla resumen: todos los algoritmos juntos
    print("== Resumen: tiempo en segundos (razón respecto a la n anterior) ==")
    print(f"{'Algoritmo':<17}" + "".join(f"{n:>20}" for n in TAMANOS) + f"{'teórica':>10}")
    for nombre, esperada, fila in resumen:
        celdas = "".join(f"{f'{t:.5f} ({r})':>20}" for t, r in fila)
        print(f"{nombre[:17]:<17}{celdas}{esperada:>10}")


if __name__ == "__main__":
    if "--perfil" in sys.argv:
        import cProfile
        import pstats

        perfil = cProfile.Profile()
        perfil.enable()
        laboratorio()
        perfil.disable()
        print("\n== Reporte cProfile (10 funciones con mayor tiempo propio) ==")
        pstats.Stats(perfil).strip_dirs().sort_stats("tottime").print_stats(10)
    else:
        laboratorio()
