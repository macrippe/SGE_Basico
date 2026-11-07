"""
Sistema de Gestión de Estudiantes (SGE) básico
------------------------------------------------
Asignatura : 2026 2-ALGORITMOS Y PROGRAMACION-2317-1A MOM 2 VIRTUAL - UCompensar
Actividad  : 4 - Etapa de Profundización
Autor      : Milton Cortes Rippe 

Aplicación por consola que permite:
    1. Agregar estudiantes
    2. Mostrar la lista completa de estudiantes
    3. Buscar un estudiante por su ID
    4. Salir del sistema

Estructuras usadas:
    - while (repetición condicionada al comienzo) para el menú principal.
    - match-case (decisión múltiple, el "switch" de Python) para las opciones.
    - if / if-else / if-elif (decisión simple y anidada) para validaciones.
    - for (repetición con número conocido de vueltas) para recorrer la lista.
    - while True + break (simula la repetición condicionada al final,
      "do-while") para pedir un dato hasta que sea válido.
    - Variables especiales: contador (total_estudiantes),
      acumulador (suma_notas) y bandera (bandera_salir).
    - Lista de diccionarios para almacenar a los estudiantes.

Requisito: Python 3.10 o superior (match-case no existe en versiones anteriores).
Ejecución en Visual Studio Code: abrir este archivo y pulsar "Run Python File"
o, en la terminal, escribir:  python sge.py
"""

# ---------------------------------------------------------------------------
# Constantes de configuración
# Se agrupan aquí para que cualquier límite se cambie en un solo lugar.
# ---------------------------------------------------------------------------
CAPACIDAD_MAXIMA = 50          # Tope de registros: evita que la lista crezca sin control.
ID_MINIMO, ID_MAXIMO = 1, 9999
EDAD_MINIMA, EDAD_MAXIMA = 14, 70
NOTA_MINIMA, NOTA_MAXIMA = 0.0, 5.0   # Escala de calificación usada.

LINEA = "=" * 64


# ---------------------------------------------------------------------------
# Funciones de entrada con validación
# Todas repiten la pregunta hasta recibir un dato correcto, así el programa
# nunca se cae por un error de digitación (texto donde se espera un número).
# ---------------------------------------------------------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero y lo devuelve solo cuando es válido."""
    while True:  # Se ejecuta al menos una vez, como un do-while.
        dato = input(mensaje).strip()
        try:
            numero = int(dato)
        except ValueError:
            # int() lanza ValueError si el usuario escribe letras o deja vacío.
            print("  [Error] Debe ingresar un número entero. Intente de nuevo.")
            continue

        if minimo is not None and numero < minimo:
            print(f"  [Error] El valor mínimo permitido es {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"  [Error] El valor máximo permitido es {maximo}.")
        else:
            return numero  # Condición de salida del ciclo: dato válido.


def leer_decimal(mensaje, minimo, maximo):
    """Pide un número decimal dentro de un rango (acepta coma o punto)."""
    while True:
        dato = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(dato)
        except ValueError:
            print("  [Error] Debe ingresar un número (ejemplo: 4.2).")
            continue

        if minimo <= numero <= maximo:
            return round(numero, 1)
        print(f"  [Error] El valor debe estar entre {minimo} y {maximo}.")


def leer_texto(mensaje, solo_letras=False):
    """Pide un texto no vacío. Si solo_letras es True, rechaza números y símbolos."""
    while True:
        texto = " ".join(input(mensaje).split())  # Quita espacios sobrantes.
        if texto == "":
            print("  [Error] Este campo no puede quedar vacío.")
        elif solo_letras and not all(c.isalpha() or c == " " for c in texto):
            print("  [Error] Use solo letras y espacios.")
        else:
            return texto.title() if solo_letras else texto


def leer_confirmacion(mensaje):
    """Pide S o N; devuelve True si el usuario confirma."""
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("  [Error] Responda S (sí) o N (no).")


# ---------------------------------------------------------------------------
# Funciones del sistema (una responsabilidad por función)
# ---------------------------------------------------------------------------
def mostrar_menu(total_estudiantes):
    """Imprime el menú principal junto con el contador de registros."""
    print()
    print(LINEA)
    print("      SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE) - UCompensar")
    print(LINEA)
    print(f"  Estudiantes registrados: {total_estudiantes} / {CAPACIDAD_MAXIMA}")
    print("-" * 64)
    print("  1. Agregar estudiante")
    print("  2. Mostrar lista de estudiantes")
    print("  3. Buscar estudiante por ID")
    print("  4. Salir")
    print(LINEA)


def buscar_por_id(estudiantes, id_buscado):
    """Recorre la lista y devuelve el estudiante con ese ID, o None si no existe.

    Es una búsqueda secuencial: en el peor caso revisa todos los elementos,
    por eso su costo crece de forma lineal con el número de estudiantes, O(n).
    """
    for estudiante in estudiantes:
        if estudiante["id"] == id_buscado:
            return estudiante  # Se detiene apenas lo encuentra.
    return None


def mostrar_estudiante(estudiante):
    """Muestra la ficha de un solo estudiante (se reutiliza al agregar y al buscar)."""
    print("-" * 40)
    print(f"  ID       : {estudiante['id']}")
    print(f"  Nombre   : {estudiante['nombre']}")
    print(f"  Edad     : {estudiante['edad']} años")
    print(f"  Programa : {estudiante['programa']}")
    print(f"  Nota     : {estudiante['nota']:.1f}")
    print("-" * 40)


def agregar_estudiante(estudiantes, total_estudiantes):
    """Pide los datos de un estudiante nuevo, lo guarda y devuelve el contador actualizado."""
    print("\n--- AGREGAR ESTUDIANTE ---")

    # Decisión simple: si la lista está llena no se piden datos.
    if total_estudiantes >= CAPACIDAD_MAXIMA:
        print(f"  [Aviso] Se alcanzó la capacidad máxima de {CAPACIDAD_MAXIMA} estudiantes.")
        return total_estudiantes

    # El ID se pide hasta que sea único; un ID repetido haría ambigua la búsqueda.
    while True:
        id_nuevo = leer_entero("  ID del estudiante: ", ID_MINIMO, ID_MAXIMO)
        if buscar_por_id(estudiantes, id_nuevo) is None:
            break
        print(f"  [Error] Ya existe un estudiante con el ID {id_nuevo}.")

    nombre = leer_texto("  Nombre completo: ", solo_letras=True)
    edad = leer_entero("  Edad: ", EDAD_MINIMA, EDAD_MAXIMA)
    programa = leer_texto("  Programa académico: ")
    nota = leer_decimal("  Nota promedio (0.0 a 5.0): ", NOTA_MINIMA, NOTA_MAXIMA)

    # Cada estudiante es un diccionario; la lista guarda todos los diccionarios.
    estudiante = {
        "id": id_nuevo,
        "nombre": nombre,
        "edad": edad,
        "programa": programa,
        "nota": nota,
    }
    estudiantes.append(estudiante)
    total_estudiantes += 1  # Contador: suma 1 por cada registro exitoso.

    print("\n  Estudiante agregado correctamente:")
    mostrar_estudiante(estudiante)
    return total_estudiantes


def mostrar_estudiantes(estudiantes, total_estudiantes):
    """Muestra todos los estudiantes en forma de tabla y el promedio general."""
    print("\n--- LISTA DE ESTUDIANTES ---")

    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return

    print(f"  {'N°':<4}{'ID':<9}{'Nombre':<22}{'Edad':<6}{'Programa':<24}{'Nota':>5}")
    print("  " + "-" * 68)

    suma_notas = 0.0  # Acumulador: suma todas las notas para el promedio.
    for posicion, estudiante in enumerate(estudiantes, start=1):
        print(f"  {posicion:<4}{estudiante['id']:<9}{estudiante['nombre'][:21]:<22}"
              f"{estudiante['edad']:<6}{estudiante['programa'][:23]:<24}{estudiante['nota']:>5.1f}")
        suma_notas += estudiante["nota"]

    promedio = suma_notas / total_estudiantes
    print("  " + "-" * 68)
    print(f"  Total de estudiantes: {total_estudiantes}    Promedio general: {promedio:.2f}")


def buscar_estudiante(estudiantes):
    """Pide un ID e informa si el estudiante existe o no."""
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")
    id_buscado = leer_entero("  ID a buscar: ", ID_MINIMO, ID_MAXIMO)
    estudiante = buscar_por_id(estudiantes, id_buscado)

    # Decisión simple (if-else): ¿se encontró o no?
    if estudiante is None:
        print(f"  No se encontró ningún estudiante con el ID {id_buscado}.")
    else:
        print("  Estudiante encontrado:")
        mostrar_estudiante(estudiante)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    estudiantes = []          # Lista: crece dinámicamente con cada registro.
    total_estudiantes = 0     # Contador de estudiantes registrados.
    bandera_salir = False     # Bandera: se vuelve True cuando el usuario decide salir.

    # Repetición condicionada al comienzo: el menú se repite mientras
    # la bandera indique que el usuario NO ha pedido salir.
    while not bandera_salir:
        mostrar_menu(total_estudiantes)
        opcion = leer_entero("  Seleccione una opción: ")

        # Decisión múltiple: dirige el flujo a la funcionalidad elegida.
        match opcion:
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes)
            case 4:
                if leer_confirmacion("  ¿Seguro que desea salir? (S/N): "):
                    bandera_salir = True  # Cambia la bandera: el while termina.
            case _:
                # Caso por defecto: cubre cualquier número fuera del menú.
                print(f"  [Error] La opción {opcion} no existe. Elija entre 1 y 4.")

    print(f"\nSesión finalizada. Se registraron {total_estudiantes} estudiante(s).")
    print("Gracias por usar el SGE.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o cierre de la entrada: se termina con un mensaje, no con un error.
        print("\n\nEjecución interrumpida por el usuario. Hasta pronto.")
