# Sistema de Gestión de Estudiantes (SGE) básico

Actividad 4 de **Algoritmos y Programación** (UCompensar), etapa de Profundización.
Autor: Milton Cortes Rippe.

Aplicación por consola en Python que permite:

1. Agregar estudiantes (ID único, nombre, edad, programa y nota)
2. Mostrar la lista completa con el total y el promedio general
3. Buscar un estudiante por su ID
4. Salir del sistema (con confirmación)

## Requisitos

- Python **3.10 o superior** 


## Cómo ejecutarlo

En Visual Studio Code: abrir `sge.py` y pulsar el botón **Run Python File**.
Desde la terminal, dentro de la carpeta del proyecto:

```bash
python sge.py
```

## Estructuras de control utilizadas

| Estructura | Dónde | Para qué |
|---|---|---|
| `while not bandera_salir` | `main()` | Repetir el menú hasta que el usuario decida salir |
| `match-case` | `main()` | Dirigir el flujo a la opción elegida; `case _` atiende opciones inválidas |
| `if / elif / else` | validaciones, `buscar_estudiante()` | Validar rangos y saber si el estudiante existe |
| `for` | `buscar_por_id()`, `mostrar_estudiantes()` | Recorrer la lista de estudiantes |
| `while True` + `return`/`break` | funciones `leer_*` | Pedir un dato hasta que sea válido (equivale a un do-while) |
| `try / except` | `leer_entero()`, `leer_decimal()` | Evitar que el programa se caiga si se escribe texto donde va un número |

Variables especiales: contador `total_estudiantes`, acumulador `suma_notas` y bandera `bandera_salir`.
Los estudiantes se guardan en una **lista** de diccionarios.
