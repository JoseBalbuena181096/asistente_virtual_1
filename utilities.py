import subprocess
import nltk  # Biblioteca para procesamiento del lenguaje natural (gramática y parser)
import pywhatkit  # Permite reproducir videos de YouTube o hacer búsquedas
import speech_recognition as sr  # type: ignore # Reconocimiento de voz
import os  # Módulo para interacciones con el sistema operativo
import pyttsx3  # Síntesis de voz para generar respuestas de audio
import ctypes
import sys
import pyautogui
import datetime
import time

# Clase para la síntesis de voz
class GeneradorVoz:
    def __init__(self):
        """Inicializa el motor de voz."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 120)  # Configura la velocidad de la voz

    def generar_voz(self, textoAudio):
        """Genera audio a partir de texto."""
        self.engine.say(textoAudio)
        self.engine.runAndWait()

# Definición de la gramática que vamos a usar para reconocer comandos
gramatica = nltk.grammar.FeatureGrammar.fromstring("""
        S -> AV NP VP 
        AV -> 'alexa' | 'siri' | 'google' | 'cortana' |'smartlabs'  |'smartlab'
        NP -> DET N | IND N | CONJ N | N
        VP -> V NP | V
        DET -> 'el' | 'la' | 'los' | 'las' | 'al'
        IND -> 'un' | 'una' | 'uno' | 'unos' | 'unas'
        CONJ -> 'y' | 'o' | 'u' | 'a' | 'e' | 'que' | 'como' |\
            'cuando' | 'donde'
        N -> 'cumbia' | 'salsa' | 'luis' | 'miguel' | 'bachata' | 'banda' \
            | 'rock' | 'jose' | 'laser' | 'solidworks' | 'google' | 'bambu'| 'hora'\
            | 'captura' | 'computadora'| 'programa'
        V -> 'corre' | 'come' | 'vuela' | 'grita' | 'ladra' | 'canta' | 'escribe' |\
            'reproduce' | 'reproducir' | 'busca' | 'buscar' | 'abre' | 'abrir' | 'inicia'\
            | 'dime' | 'toma' | 'suspende'| 'termina'
    """)


parser = nltk.FeatureEarleyChartParser(gramatica)  # Parser que usaremos para la gramática

# Instancia para la síntesis de voz
generador_voz = GeneradorVoz()

# Clase para el reconocimiento de voz
class ReconocimientoVoz:
    def __init__(self):
        """Inicializa el reconocimiento de voz."""
        self.recognizer = sr.Recognizer()

    def escuchar_audio(self):
        """Captura y procesa el audio del micrófono."""
        with sr.Microphone() as source:
            print("Ajustando el ruido ambiente...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Escuchando...")
            try:
                # Captura el audio
                audio = self.recognizer.listen(source, timeout=6)
                # Usa Google para reconocer el audio
                text = self.recognizer.recognize_google(audio, language="es-MX")
                print("Texto reconocido: {}".format(text))
                return text.lower()  # Convierte el texto a minúsculas
            except sr.WaitTimeoutError:
                print("No se detectó ningún audio.")
                return ""
            except sr.UnknownValueError:
                print("No se pudo reconocer el audio.")
                return ""

# Función para normalizar texto (quita acentos)
def normalize(s):
    """Normaliza caracteres acentuados en el texto."""
    replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

# Función para procesar el comando de voz reconocido
def procesar_comando(comando):
    """Procesa el comando de voz y ejecuta la acción adecuada."""
    text2 = comando.split()  # Divide el texto en palabras
    try:
        parser.parse(text2)  # Verifica si el comando cumple la gramática
        if len(text2) < 2:
            return  # Si no hay suficientes palabras, no se procesa

        # Extrae la acción principal (verbo) del comando
        accion = text2[1]

        # Si la acción es reproducir, busca en YouTube
        if accion in ['reproduce', 'reproducir']:
            busqueda = ' '.join(text2[2:])  # Extrae lo que se quiere reproducir
            textoAudio = f"Reproduciendo {busqueda} en YouTube"
            generador_voz.generar_voz(textoAudio)
            pywhatkit.playonyt(busqueda)

        # Si la acción es buscar, hace una búsqueda en Google
        elif accion in ['buscar', 'busca']:
            busqueda = ' '.join(text2[2:])  # Extrae lo que se quiere buscar
            textoAudio = f"Buscando {busqueda} en Google"
            generador_voz.generar_voz(textoAudio)
            pywhatkit.search(busqueda)

        # Si la acción es abrir una aplicación, lanza el programa especificado
        elif accion in ['abre', 'abrir', 'inicia']:
            if len(text2) < 3:
                print("Especifica qué aplicación abrir.")
                return

            app = text2[2]  # Extrae la aplicación a abrir
            apps = {
                'laser': 'C:/RDWorksV8/RDWorksV8.exe',
                'solidworks': 'C:/Program Files/SOLIDWORKS Corp/SOLIDWORKS/SLDWORKS.exe',
                'google': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
                'bambu': 'C:/Program Files/Bambu Studio/bambu-studio.exe'
            }

            if app in apps:
                textoAudio = f"Abriendo {app}"
                generador_voz.generar_voz(textoAudio)
                #subprocess.run(apps[app])
                try:
                    # Reemplaza 'tu_comando' y 'tus_argumentos' por el comando que deseas ejecutar
                    subprocess.run(apps[app], check=True)
                except OSError as e:
                    if e.winerror == 740:
                        print("El proceso requiere privilegios de administrador.\
                            Solicitando elevación...")
                        # Solicitar elevación y reiniciar el script
                        ctypes.windll.shell32.ShellExecuteW(
                            None, 
                            "runas", 
                            sys.executable, 
                            ' '.join([f'"{arg}"' for arg in sys.argv]), 
                            None, 
                            1
                            )
                    else:
                        print(f"Ocurrió un error: {e}")

            else:
                textoAudio = "No reconozco la aplicación que quieres abrir"
                generador_voz.generar_voz(textoAudio)

        # Nueva funcionalidad: decir la hora
        elif accion == 'dime' and 'hora' in text2:
            hora_actual = datetime.datetime.now().strftime("%H:%M")
            textoAudio = f"La hora actual es {hora_actual}"
            generador_voz.generar_voz(textoAudio)

        # Nueva funcionalidad: tomar captura de pantalla
        elif accion == 'toma' and 'captura' in text2:
            screenshot = pyautogui.screenshot()
            screenshot.save("captura_pantalla.png")
            textoAudio = "He tomado una captura de pantalla y la he guardado como\
                'captura_pantalla.png'"
            generador_voz.generar_voz(textoAudio)

        # Nueva funcionalidad: suspender la computadora
        elif accion == 'suspende' and 'computadora' in text2:
            textoAudio = "Suspendiendo la computadora en 5 segundos"
            generador_voz.generar_voz(textoAudio)
            time.sleep(5)
            ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)

        elif accion == 'termina' and 'programa' in text2:
            # Generar mensaje de voz
            textoAudio = "Terminando programa adios usuario"
            generador_voz.generar_voz(textoAudio)
            time.sleep(3)
            # Termina el programa correctamente
            sys.exit()
            

    except ValueError:
        print("El comando no está en la gramática. Inténtalo de nuevo.")