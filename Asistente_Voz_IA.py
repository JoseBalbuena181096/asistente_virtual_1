from utilities import ReconocimientoVoz
from utilities import normalize
from utilities import procesar_comando


# Función principal del programa
def main():
    reconocimiento = ReconocimientoVoz()
    while True:
        comando = reconocimiento.escuchar_audio()  # Escucha el audio
        comando = normalize(comando)  # Normaliza el texto
        procesar_comando(comando)  # Procesa el comando

if __name__ == "__main__":
    main()  # Ejecuta el programa
