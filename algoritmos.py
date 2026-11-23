"""Algoritmos de ordenamiento y búsqueda para el laboratorio de eficiencia (Unidad 4)."""


# insercion: O(n^2) en tiempo (peor y promedio), O(n) en el mejor caso; O(1) espacio extra
def insercion(lista):
    """Ordena la lista in situ con el método de inserción y la devuelve."""
    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        # desplaza a la derecha los elementos mayores que la clave
        while j >= 0 and lista[j] > clave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = clave
    return lista


# merge sort: O(n log n) en tiempo (todos los casos); O(n) espacio extra
def merge_sort(lista):
    """Devuelve una nueva lista ordenada usando Merge Sort."""
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return _mezclar(izquierda, derecha)


# mezcla de dos listas ordenadas: O(n) tiempo y espacio
def _mezclar(izquierda, derecha):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


# busqueda lineal: O(n) en tiempo (peor caso); O(1) espacio extra
def busqueda_lineal(lista, objetivo):
    """Devuelve el índice de objetivo en lista, o -1 si no está."""
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1


# busqueda binaria (iterativa): O(log n) en tiempo; O(1) espacio extra. Requiere lista ordenada.
def busqueda_binaria(lista, objetivo):
    """Devuelve el índice de objetivo en la lista ORDENADA, o -1 si no está."""
    bajo, alto = 0, len(lista) - 1
    while bajo <= alto:
        medio = (bajo + alto) // 2
        if lista[medio] == objetivo:
            return medio
        if lista[medio] < objetivo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1
