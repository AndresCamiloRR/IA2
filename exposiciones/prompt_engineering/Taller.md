### Ejercicio 1: Generación de una Función de Código
#### 1.A: Prompt Simple

[](https://github.com/JuanJojoa7/advanced-prompt-engineering/blob/main/EJERCICIOS.md#1a-prompt-simple)

```
Haz una función en Python para validar una contraseña.
```
https://chatgpt.com/share/68bcb434-78e0-8002-aab9-6f4593cc3c32
```python
import re

def validar_contrasena(password: str) -> bool:
    """
    Valida si una contraseña cumple con los criterios de seguridad:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[@$!%*?&.#_]", password):
        return False

    return True


# Ejemplo de uso
print(validar_contrasena("Abc123!@"))  # True
print(validar_contrasena("abc123"))    # False

```
#### 1.B: Prompt Avanzado
```
**Rol:** Eres un desarrollador de software senior especializado en ciberseguridad.

**Tarea:** Genera una función en Python llamada `validar_contrasena`.

**Contexto:** La función recibirá una cadena de texto (la contraseña) y debe retornar `True` si cumple con TODAS las siguientes reglas, o `False` si falla al menos una.

**Reglas de Validación (Criterios):**
1.  Debe tener una longitud mínima de 12 caracteres.
2.  Debe contener al menos una letra mayúscula (A-Z).
3.  Debe contener al menos una letra minúscula (a-z).
4.  Debe contener al menos un número (0-9).
5.  Debe contener al menos un carácter especial (ej: @, #, $, %, &, !).

**Formato de Salida:**
-   El bloque de código de la función en Python.
-   Debe incluir docstrings que expliquen qué hace la función, sus parámetros y qué retorna.
-   Añade 3 ejemplos de uso: uno con una contraseña válida y dos con contraseñas inválidas que demuestren diferentes fallos.

**Restricciones:**
-   No uses librerías externas, solo el core de Python.
-   El código debe ser legible y seguir las convenciones de estilo de PEP 8.
```
https://chatgpt.com/share/68bcb458-c5b8-8002-b3c4-6dbb45a599d7
```python
def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si una contraseña cumple con los criterios de seguridad establecidos.

    Criterios de validación:
    1. Longitud mínima de 12 caracteres.
    2. Al menos una letra mayúscula (A-Z).
    3. Al menos una letra minúscula (a-z).
    4. Al menos un número (0-9).
    5. Al menos un carácter especial (@, #, $, %, &, !).

    Parámetros
    ----------
    contrasena : str
        La contraseña a validar.

    Retorna
    -------
    bool
        True si la contraseña cumple con todos los criterios, False en caso contrario.
    """
    if len(contrasena) < 12:
        return False

    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    tiene_especial = any(c in "@#$%&!" for c in contrasena)

    return all([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])


# Ejemplos de uso
print(validar_contrasena("Password123!"))       # True → cumple todas las reglas
print(validar_contrasena("password123!"))       # False → falta una letra mayúscula
print(validar_contrasena("PASSWORDONLY!!!!"))   # False → falta un número y minúscula

```def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si una contraseña cumple con los criterios de seguridad establecidos.

    Criterios de validación:
    1. Longitud mínima de 12 caracteres.
    2. Al menos una letra mayúscula (A-Z).
    3. Al menos una letra minúscula (a-z).
    4. Al menos un número (0-9).
    5. Al menos un carácter especial (@, #, $, %, &, !).

    Parámetros
    ----------
    contrasena : str
        La contraseña a validar.

    Retorna
    -------
    bool
        True si la contraseña cumple con todos los criterios, False en caso contrario.
    """
    if len(contrasena) < 12:
        return False

    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    tiene_especial = any(c in "@#$%&!" for c in contrasena)

    return all([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])


# Ejemplos de uso
print(validar_contrasena("Password123!"))       # True → cumple todas las reglas
print(validar_contrasena("password123!"))       # False → falta una letra mayúscula
print(validar_contrasena("PASSWORDONLY!!!!"))   # False → falta un número y minúscula

```
#### 1.C: Evaluación Comparativa
-   **Completitud:**  ¿La función del prompt simple incluyó todas las reglas?
	-	Sí, incluyó todas las reglas, ejemplos, validación, docstrings y pep8 la única diferencia es que en el prompt simple hizo uso de re para patrones regex
-   **Claridad:**  ¿El código está bien documentado? ¿Es fácil de entender?
	- Sí, en ambos un código corto y fácil de entender
-   **Utilidad:**  ¿El prompt avanzado proporcionó ejemplos de uso que facilitan la prueba y la integración?
	-	Sí, aunque el prompt simple también lo hizo
-   **Robustez:**  ¿La función maneja casos borde que el prompt simple podría haber ignorado?
	- No, se limitó a lo descrito en el prompt
### Ejercicio 2: Extracción de Información a Formato JSON
#### 2.A: Prompt Simple

[](https://github.com/JuanJojoa7/advanced-prompt-engineering/blob/main/EJERCICIOS.md#2a-prompt-simple)

```
Saca los datos importantes de este texto en JSON:

"La reunión de lanzamiento del Proyecto Fénix será el 15 de octubre de 2024 a las 10:30 AM en la Sala Júpiter. Los asistentes confirmados son Ana García (Líder de Proyecto), Carlos Rodríguez (Desarrollador Principal) y Elena Fernández (Diseñadora UX). El presupuesto asignado es de $25,000 USD."
```
https://chatgpt.com/share/68bcb645-f458-8002-9639-2cde7e15fece
```json
{
  "proyecto": "Proyecto Fénix",
  "evento": "Reunión de lanzamiento",
  "fecha": "2024-10-15",
  "hora": "10:30 AM",
  "lugar": "Sala Júpiter",
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ],
  "presupuesto_asignado": {
    "monto": 25000,
    "moneda": "USD"
  }
}

```

#### 2.B: Prompt Avanzado

[](https://github.com/JuanJojoa7/advanced-prompt-engineering/blob/main/EJERCICIOS.md#2b-prompt-avanzado)

```
**Rol:** Eres un asistente de procesamiento de datos altamente preciso.

**Tarea:** Extrae la información clave del siguiente texto y formatéala estrictamente como un objeto JSON.

**Texto de Entrada:**
La reunión de lanzamiento del Proyecto Fénix será el 15 de octubre de 2024 a las 10:30 AM en la Sala Júpiter. Los asistentes confirmados son Ana García (Líder de Proyecto), Carlos Rodríguez (Desarrollador Principal) y Elena Fernández (Diseñadora UX). El presupuesto asignado es de $25,000 USD.

**Esquema JSON de Salida (Schema):**
Debes seguir esta estructura exacta. Si un campo no se encuentra en el texto, déjalo como `null`.

```json
{
  "proyecto": {
    "nombre": "string",
    "presupuesto": {
      "monto": "number",
      "moneda": "string"
    }
  },
  "reunion": {
    "fecha": "string (formato YYYY-MM-DD)",
    "hora": "string (formato HH:MM)",
    "ubicacion": "string"
  },
  "asistentes": [
    {
      "nombre": "string",
      "rol": "string"
    }
  ]
}

**Restricciones:**
-   El  `monto`  del presupuesto debe ser un número, no un string.
-   La  `fecha`  y  `hora`  deben ser normalizadas a los formatos especificados.
-   No incluyas campos que no estén en el esquema.
```
https://chatgpt.com/share/68bcb6fb-5398-8002-82c9-43e99b66d4a5
```json
{
  "proyecto": {
    "nombre": "Proyecto Fénix",
    "presupuesto": {
      "monto": 25000,
      "moneda": "USD"
    }
  },
  "reunion": {
    "fecha": "2024-10-15",
    "hora": "10:30",
    "ubicacion": "Sala Júpiter"
  },
  "asistentes": [
    {
      "nombre": "Ana García",
      "rol": "Líder de Proyecto"
    },
    {
      "nombre": "Carlos Rodríguez",
      "rol": "Desarrollador Principal"
    },
    {
      "nombre": "Elena Fernández",
      "rol": "Diseñadora UX"
    }
  ]
}

```
#### 2.C: Evaluación Comparativa
-   **Estructura:** ¿El JSON del prompt simple tiene una estructura lógica y predecible?
	- Más o menos porque terminó por agrupar las propiedades de presupuesto asignado como monto y moneda al mismo nivel de proyecto, cuando tiene más sentido que sea un hijo suyo, de la misma forma en que evento, fecha, hora y lugar podrían haber sido agrupados como en el caso del prompt avanzado
-   **Precisión:** ¿Los tipos de datos son correctos (números vs. strings)?
	-  Sí todos los tipos de datos son correctos en ambos prompts
-   **Parseabilidad:** ¿El JSON generado por el prompt avanzado es directamente utilizable por una aplicación sin necesidad de limpieza o conversión?
	- Ambos JSON generados son correctos, la única dificultad es para el caso del prompt simple donde como mencioné en la pregunta de la estructura, probablemente toque leer el json y agrupar ciertos campos para que tenga más sentido como entidad
-   **Manejo de Nulos:** ¿Cómo manejaría cada uno un texto donde, por ejemplo, el presupuesto no se menciona?
	- Para el caso del prompt simple no incluiría el campo ya que desconoce la estructura de salida, mientras que el avanzado seguramente lo marcaría como null
### Ejercicio 3: Escritura Creativa con Tono y Estilo
#### 3.A: Prompt Simple
```
Escribe sobre los agujeros negros.
```
https://chatgpt.com/share/68bcc009-98f0-8002-bd13-9d08f238c80b

Los **agujeros negros** son uno de los fenómenos más fascinantes y extremos del universo. Se forman cuando una cantidad enorme de masa se concentra en un espacio extremadamente reducido, generando un campo gravitacional tan intenso que nada puede escapar de él, ni siquiera la luz.

### Formación

La mayoría de los agujeros negros se originan tras la muerte de estrellas muy masivas. Cuando una estrella agota su combustible nuclear, su núcleo colapsa bajo su propia gravedad. Si la masa remanente es suficientemente grande, se forma un agujero negro.

### Partes principales

Un agujero negro no es un “vacío” en el espacio, sino una región con propiedades muy definidas:

-   **Horizonte de sucesos:** la frontera invisible a partir de la cual nada puede escapar.
    
-   **Singularidad:** el centro, donde la densidad es teóricamente infinita y las leyes de la física clásica dejan de describir la realidad.
    
-   **Disco de acreción:** gas, polvo o materia cercana que gira alrededor antes de caer, calentándose y emitiendo radiación muy intensa.
    

### Tipos

-   **Agujeros negros estelares:** resultado del colapso de estrellas masivas, con masas de unas pocas decenas de veces la del Sol.
    
-   **Agujeros negros supermasivos:** se encuentran en el centro de muchas galaxias, incluida la Vía Láctea, y pueden tener millones o miles de millones de veces la masa solar.
    
-   **Agujeros negros de masa intermedia:** menos comunes y aún en estudio.
    
-   **Agujeros negros primordiales:** hipotéticos, formados poco después del Big Bang.
    

### Importancia científica

El estudio de los agujeros negros permite poner a prueba la teoría de la **relatividad general** de Einstein y explorar los límites de la física. Además, son responsables de fenómenos cósmicos extremos como los **cuásares** y las **ondas gravitacionales**, detectadas por primera vez en 2015.

### Misterios abiertos

-   ¿Qué ocurre exactamente en la singularidad?
    
-   ¿Existe una forma de unificar la relatividad general y la mecánica cuántica para describirlos completamente?
    
-   ¿Pueden los agujeros negros “evaporarse” mediante la llamada **radiación de Hawking**?
    

En pocas palabras, los agujeros negros son laboratorios naturales del cosmos que nos obligan a cuestionar nuestra comprensión del espacio, el tiempo y la física misma.

¿Quieres que lo resuma en un estilo **divulgativo sencillo**, como para niños/jóvenes, o prefieres un **nivel más técnico** para profundizar en su física?

#### 3.B: Prompt Avanzado


```

**Rol:**  Eres un divulgador científico como Carl Sagan, capaz de explicar conceptos complejos con asombro y claridad.

**Tarea:**  Escribe un párrafo corto (aproximadamente 100 palabras) sobre los agujeros negros.

**Audiencia:**  Niños de 10 a 12 años.

**Tono y Estilo:**

-   Usa un lenguaje sencillo y evocador.
-   Evita la jerga técnica y las fórmulas matemáticas.
-   Utiliza analogías o metáforas fáciles de entender (ej: "un aspirador cósmico del que ni la luz puede escapar").
-   El tono debe ser de misterio y fascinación, no de miedo.

**Formato de Salida:**

-   Un único párrafo de texto.

**Restricción:**

-   No menciones la "singularidad" o la "relatividad general" directamente. Enfócate en el fenómeno observable.

```
https://chatgpt.com/share/68bcc048-7f90-8002-95ba-0c5099e9abd0

Imagina un lugar en el espacio donde la gravedad es tan fuerte que nada puede escapar, ni siquiera la luz: eso es un agujero negro. Es como un aspirador cósmico escondido en la oscuridad, que traga todo lo que se acerque demasiado. Pero no todo es vacío y silencio: alrededor de un agujero negro, la materia gira y brilla como un remolino de fuego, revelando su presencia. Son puertas misteriosas en el universo, invisibles a simple vista, que nos recuerdan lo inmenso y sorprendente que es el cosmos, lleno de secretos aún por descubrir.
#### 3.C: Evaluación Comparativa

-   **Adecuación a la Audiencia:** ¿Qué respuesta es más apropiada y comprensible para un niño?
	- El prompt avanzado ya que da una respuesta muchísimo más límitada y lenguaje poco técnico
-   **Tono:** ¿Logró el prompt simple capturar el tono de asombro solicitado?
	- Sí, los presenta como uno de los fenómenos más fascinantes y extremos del universo
-   **Creatividad:** ¿Qué respuesta es más original y memorable?
	- El avanzado es más creativo aunque considero que el simple es más memorable
-   **Cumplimiento de Restricciones:** ¿El prompt avanzado logró evitar la jerga técnica como se le pidió?
	- Sí, cumplió las restricciones
