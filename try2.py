import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}\.(txt|text|csv)\b',
    'separador': r'[,;|]',
    'numero': r'[0-9]+',
    'coma': r',',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)\b',
    'comentario': r'@\s*.*'
}

# Inicializar tokens
tokens = {}


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
    return re.match(lexemas['comentario'], palabra) is not None


# Función para dividir la línea en palabras/separadores
def dividir_linea(linea):
    return re.split(r'([,;|])|(\s+)', linea)


# Función que analiza línea por línea
def analiza_linea(archivo):
    for linea_num, linea in enumerate(archivo, start=1):
        palabras = dividir_linea(linea)  

        for palabra in palabras:
            if palabra is None or palabra.strip() == "":
                continue
            # Comprobaciones de cada tipo de lexema
            if regex_es_comentario(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'comentario'
                break  # Ignorar el resto de la línea
            elif regex_es_palabra_reservada(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'palabrasReservadas'
            elif regex_es_nombre_de_variable(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'nomVariables'
            elif regex_es_nombre_de_archivo(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'nomArchivo'
            elif regex_es_numero(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'numero'
            elif re.fullmatch(lexemas['separador'], palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'separador'
            else:
                print(f"Error léxico en la palabra: '{palabra}' en la línea {linea_num}")
                if palabra not in tokens:
                    tokens[palabra] = 'error'

# Función para abrir el archivo
def abrir_archivo(ruta_de_archivo):
    with open(ruta_de_archivo, 'r', encoding='UTF-8') as f:
        analiza_linea(f)


# Función que muestra los resultados de los tokens
def muestra():
    abrir_archivo('prueba.txt')
    for token in tokens:
        print(token + " - " + tokens[token])
    print("FIN")


# Ejecución principal
if __name__ == "__main__":
    muestra()
