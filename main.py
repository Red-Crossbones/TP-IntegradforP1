import os
from parser2 import InterpreteBari24


def main():
    print("=== Bienvenido al intérprete Bari24 ===")
    interprete = InterpreteBari24()  # Crear una instancia del intérprete
    
    while True:
        archivo = input("¿Qué archivo Bari24 desea ejecutar? (o 'salir' para terminar): ").strip()
        
        if archivo.lower() == "salir":
            print("Saliendo del intérprete Bari24. ¡Hasta luego!")
            break
        
        if not os.path.isfile(archivo):
            print(f"Error: El archivo '{archivo}' no existe. Por favor, intente nuevamente.\n")
            continue

        try:
            print(f"\nEjecutando el archivo '{archivo}'...\n")
            interprete.ejecutar_archivo(archivo)
            print("\n=== Ejecución finalizada ===\n")
        except Exception as e:
            print(f"Error durante la ejecución del archivo '{archivo}': {e}\n")
            continue


if __name__ == "__main__":
    main()
