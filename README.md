---

### Reporte: Asistente de Voz SmartVoice

#### Resumen

SmartVoice Assistant es una aplicación basada en Python diseñada para interpretar y ejecutar comandos de voz del usuario. Aprovechando diversas bibliotecas para reconocimiento de voz, procesamiento de lenguaje natural y control del sistema, el asistente proporciona una forma fluida de controlar funciones de la computadora utilizando lenguaje natural.

#### Componentes

1. **Programa Principal (`main.py`):**

   - **Propósito:** Sirve como punto de entrada de la aplicación.
   - **Funcionalidad:** Inicializa el sistema de reconocimiento de voz y entra en un bucle infinito donde escucha comandos del usuario, normaliza el texto y procesa los comandos en consecuencia.

2. **Módulo de Utilidades (`utilities.py`):**

   - **Importaciones:**

     - **Bibliotecas Estándar:** `subprocess`, `os`, `ctypes`, `sys`, `datetime`, `time`
     - **Bibliotecas de Terceros:** `nltk`, `pywhatkit`, `speech_recognition`, `pyttsx3`, `pyautogui`

   - **Clases:**

     - **`GeneradorVoz`:**

       - **Propósito:** Maneja las operaciones de texto a voz.
       - **Métodos:**
         - `__init__`: Inicializa el motor `pyttsx3` y configura la velocidad de la voz.
         - `generar_voz`: Convierte texto de entrada en voz audible.

     - **`ReconocimientoVoz`:**
       - **Propósito:** Gestiona el reconocimiento de voz.
       - **Métodos:**
         - `__init__`: Inicializa el reconocedor de voz.
         - `escuchar_audio`: Escucha la entrada del micrófono, procesa el audio y retorna el texto reconocido en minúsculas. Maneja excepciones por tiempos de espera y audio no reconocible.

   - **Funciones:**

     - **`normalize(s)`:**

       - **Propósito:** Elimina acentos de los caracteres para estandarizar el texto para el procesamiento.
       - **Método:** Reemplaza vocales acentuadas con sus contrapartes no acentuadas.

     - **`procesar_comando(comando)`:**
       - **Propósito:** Analiza y ejecuta el comando de voz reconocido.
       - **Metodología:**
         - **Análisis:** Utiliza el `FeatureEarleyChartParser` de NLTK con una gramática predefinida para analizar el comando.
         - **Extracción de Acción:** Identifica la acción principal (verbo) del comando.
         - **Manejo de Acciones:** Ejecuta diferentes acciones basadas en el verbo identificado:
           - **Reproducir/Reproducir:** Reproduce un video especificado en YouTube usando `pywhatkit`.
           - **Buscar/Busca:** Realiza una búsqueda en Google.
           - **Abrir/Abrir/Inicia:** Abre aplicaciones especificadas mapeando nombres de aplicaciones a sus rutas ejecutables. Maneja la elevación de privilegios si es necesario.
           - **Dime la hora:** Anuncia la hora actual del sistema.
           - **Toma captura:** Toma una captura de pantalla y la guarda como `captura_pantalla.png`.
           - **Suspende computadora:** Suspende la computadora después de una demora de 5 segundos.
           - **Termina programa:** Proporciona un mensaje de despedida y cierra el programa de manera correcta.
         - **Manejo de Errores:** Notifica al usuario si el comando no coincide con la gramática definida o si hay problemas al ejecutar la acción.

   - **Definición de Gramática (`gramatica`):**

     - **Propósito:** Define la estructura de los comandos de voz válidos utilizando `FeatureGrammar` de NLTK.
     - **Componentes:**
       - **S (Oración):** Compuesta por un direccionador (`AV`), frase nominal (`NP`) y frase verbal (`VP`).
       - **AV (Direccionador):** Palabras de activación como 'alexa', 'siri', 'google', etc.
       - **NP (Frase Nominal):** Incluye determinantes, sustantivos y conjunciones.
       - **VP (Frase Verbal):** Compuesta por verbos y opcionalmente frases nominales.
       - **Determinantes, Indefinidos, Conjunciones, Sustantivos y Verbos:** Definidos con una lista de palabras en español relevantes para la funcionalidad de la aplicación.

#### Flujo de Trabajo

1. **Inicialización:**

   - La función `main` inicializa una instancia de `ReconocimientoVoz` para comenzar a escuchar la entrada de voz.

2. **Bucle de Escucha:**

   - Escucha continuamente la entrada de audio del micrófono.
   - Al capturar audio, normaliza el texto para eliminar acentos y asegurar un procesamiento consistente.

3. **Procesamiento de Comandos:**

   - El texto normalizado se analiza contra la gramática predefinida para asegurar que se ajuste a las estructuras esperadas.
   - Si el comando es válido, se ejecuta la acción correspondiente.
   - Proporciona retroalimentación audible al usuario para cada acción usando la clase `GeneradorVoz`.

4. **Ejecución de Acciones:**

   - **Reproducción de Medios:** Utiliza `pywhatkit` para interactuar con YouTube o realizar búsquedas en Google.
   - **Control de Aplicaciones:** Abre aplicaciones especificadas ejecutando sus rutas. Maneja la elevación de privilegios si es necesario.
   - **Control del Sistema:** Puede tomar capturas de pantalla, anunciar la hora, suspender la computadora o terminar el programa basado en comandos.

5. **Manejo de Errores:**

   - Si el comando no se ajusta a la gramática o ocurre un error durante la ejecución, se imprimen mensajes apropiados y se proporciona retroalimentación audible cuando es aplicable.

#### Dependencias y Bibliotecas

- **`nltk`:** Utilizado para definir y analizar la gramática de los comandos de voz.
- **`pywhatkit`:** Facilita acciones como reproducir videos de YouTube y realizar búsquedas en Google.
- **`speech_recognition`:** Captura y convierte el habla a texto utilizando la API de Google.
- **`pyttsx3`:** Convierte respuestas de texto en voz audible.
- **`pyautogui`:** Maneja tareas a nivel de sistema como tomar capturas de pantalla.
- **`subprocess`:** Gestiona la apertura de aplicaciones externas.
- **`ctypes`:** Maneja operaciones a nivel de sistema como suspender la computadora.
- **`sys`:** Gestiona parámetros y funciones específicas del sistema.
- **`datetime`:** Recupera la hora actual para la funcionalidad de indicar la hora.
- **`time`:** Gestiona retrasos y funciones de sueño.

#### Seguridad y Permisos

- **Privilegios de Administrador:** Algunas acciones, como abrir ciertas aplicaciones o suspender la computadora, pueden requerir permisos elevados. La aplicación intenta solicitar estos permisos cuando es necesario.
- **Manejo de Errores:** Implementa bloques try-except para gestionar potenciales errores de manera elegante, asegurando que la aplicación no se cierre inesperadamente.

#### Extensibilidad

- **Añadir Nuevos Comandos:** Actualizando la gramática y extendiendo la función `procesar_comando`, se pueden integrar nuevos comandos de voz y acciones correspondientes.
- **Soporte para Más Idiomas:** Aunque actualmente está adaptado para español (México), la aplicación puede adaptarse para soportar otros idiomas modificando la gramática y las configuraciones de reconocimiento de voz.

#### Conclusión

SmartVoice Assistant ofrece un marco robusto para interacciones controladas por voz con una computadora. Su diseño modular, aprovechando poderosas bibliotecas de Python, permite una fácil extensión y personalización para satisfacer diversas necesidades de los usuarios. Con funcionalidades que van desde la reproducción de medios hasta el control del sistema, ejemplifica una implementación práctica de reconocimiento de voz y procesamiento de lenguaje natural en aplicaciones de escritorio.

### Video demostrativo de uso

https://youtu.be/vjM9uvp47UM
