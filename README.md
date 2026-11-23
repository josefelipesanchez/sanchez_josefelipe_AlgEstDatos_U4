# Laboratorio de eficiencia en Python – Unidad 4

Laboratorio que implementa cuatro algoritmos clásicos, mide su tiempo real de ejecución con
listas aleatorias de 1 000, 2 000, 4 000 y 8 000 elementos, y compara la razón entre mediciones
consecutivas con la complejidad teórica.

## Algoritmos comparados

| Algoritmo | Tipo | Complejidad temporal | Espacio extra |
|---|---|---|---|
| Inserción | Ordenamiento simple | O(n²) | O(1) |
| Merge Sort | Ordenamiento eficiente | O(n log n) | O(n) |
| Búsqueda lineal | Búsqueda | O(n) | O(1) |
| Búsqueda binaria | Búsqueda (lista ordenada con Merge Sort) | O(log n) | O(1) |

## Estructura

- `algoritmos.py`: implementación de los cuatro algoritmos, con su complejidad comentada.
- `main.py`: verifica que los algoritmos funcionen, genera los datos, mide con `time.perf_counter()` e imprime las tablas de tiempos y razones.
- `informe.md`: análisis teórico previo (R1), resultados (R4) y conclusiones.
- `perfil_cprofile.txt`: salida de cProfile (opcional).

## Cómo ejecutar

Requiere Python 3.8 o superior. Solo usa la biblioteca estándar (`random`, `time`, `cProfile`).

```bash
python main.py
```

Para incluir además el reporte de cProfile:

```bash
python main.py --perfil
```

## Metodología de medición

- Datos: enteros aleatorios entre 1 y 10⁶, con semilla fija (2026) para que los resultados sean reproducibles.
- Cada tiempo es el **mínimo de 5 corridas**, lo que reduce el ruido del sistema operativo.
- Las búsquedas se cronometran en lotes (100 lineales y 10 000 binarias) de un valor ausente (peor caso), porque una sola búsqueda dura microsegundos.
- La razón de cada fila es `t(n) / t(n/2)`. Valores teóricos: ≈4 para O(n²), ≈2,2 para O(n log n), 2 para O(n) y ≈1,1 para O(log n).
