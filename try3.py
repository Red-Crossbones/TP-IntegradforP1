import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}\.(txt|text|csv)\b',
    'separador': r'[,;]',
    'numero': r'[0-9]+',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)\b',
    'comentario': r'@\s*.*'
}

# Inicializar tokens (cambiado a lista de tuplas para registrar todos los tokens)
tokens = []


# Funciones de verificación
def regex_es_nombre_de_variable(palabra):
    return re.fullmatch(lexemas['nomVariables'], palabra) is not None


def regex_es_nombre_de_archivo(palabra):
    return re.fullmatch(lexemas['nomArchivo'], palabra) is not None


def regex_es_numero(palabra):
    return re.fullmatch(lexemas['numero'], palabra) is not None


def regex_es_palabra_reservada(palabra):
    return re.fullmatch(lexemas['palabrasReservadas'], palabra) is not None


def regex_es_comentario(palabra):
    return re.fullmatch(lexemas['comentario'], palabra) is not None


# Función para dividir la línea en palabras, separadores y espacios
def dividir_linea(linea):
    # Divide por cualquier cantidad de espacios o por los separadores (, ;), manteniéndolos en la salida
    return re.split(r'(\s+|[,;])', linea)


# Función que analiza línea por línea, palabra a palabra
def analiza_linea(archivo):
    for linea_num, linea in enumerate(archivo, start=1):
        palabras = dividir_linea(linea)
        cantPalabrasReservadas = 0
        for palabra in palabras:
            if palabra is None or palabra.strip() == "":
                continue
            # Comprobaciones de cada tipo de lexema
            if regex_es_comentario(linea.strip()):  # Si toda la línea es un comentario
                tokens.append((linea.strip(), 'comentario', linea_num))
                break  # Ignorar el resto de la línea
            elif regex_es_palabra_reservada(palabra):
                cantPalabrasReservadas += 1
                if cantPalabrasReservadas > 1:
                    print(f"Error en la línea {linea_num}: más de una palabra reservada en una sola línea")
                    break
                tokens.append((palabra, 'palabrasReservadas', linea_num))
            elif regex_es_nombre_de_variable(palabra):
                tokens.append((palabra, 'nomVariables', linea_num))
            elif regex_es_nombre_de_archivo(palabra):
                tokens.append((palabra, 'nomArchivo', linea_num))
            elif regex_es_numero(palabra):
                tokens.append((palabra, 'numero', linea_num))
            elif re.fullmatch(lexemas['separador'], palabra):
                tokens.append((palabra, 'separador', linea_num))
            else:
                print(f"Error léxico en la palabra: '{palabra}' en la línea {linea_num}")
                tokens.append((palabra, f"error", linea_num))


# Función para abrir el archivo
def abrir_archivo(ruta_de_archivo):
    with open(ruta_de_archivo, 'r', encoding='UTF-8') as archivo:
        analiza_linea(archivo)


# Función que muestra los resultados de los tokens
def muestra():
    abrir_archivo("prueba.txt")
    for token in tokens:
        print(f"{token[0]} --> {token[1]} (Línea {token[2]})")
    print("FIN")


# Ejecución principal
if __name__ == "__main__":
    muestra()
