import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}\.(txt|text|csv)\b',
    'separador': r'[,;]',
    'numero': r'[0-9]+',
    'coma': r',',
    'fin': r'\n',
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
    return re.fullmatch(lexemas['comentario'], palabra) is not None


# Función para dividir la línea en palabras/separadores
def dividir_linea(linea):
    return re.split(r'([,;|])|(\s+)', linea)


# Función que analiza línea por línea, palabra a palabra
def analiza_linea(archivo):
    for linea_num, linea in enumerate(archivo, start=1):
        palabras = dividir_linea(linea)  
        cantPalabrasReservadas = 0
        for palabra in palabras:
            if palabra is None or palabra.strip() == "":
                continue
            # Comprobaciones de cada tipo de lexema
            if regex_es_comentario(palabra):
                if palabra not in tokens:
                    tokens[palabra] = 'comentario'
                break  # Ignorar el resto de la línea
            elif regex_es_palabra_reservada(palabra):
                cantPalabrasReservadas += 1
                if cantPalabrasReservadas > 1:
                    print("Error en la linea: " + str(linea_num) + ". Ya hay una palabra reservada en esa linea")
                    break
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
                    tokens[palabra] = 'error' + ", linea: " + str(linea_num)


# Función para abrir el archivo
def abrir_archivo(ruta_de_archivo):
    return open(ruta_de_archivo, 'r', encoding='UTF-8')


# Función que muestra los resultados de los tokens
def muestra():
    archivo = abrir_archivo("prueba.txt")
    analiza_linea(archivo)
    for token in tokens:
        print(token + " --> " + tokens[token])
    print("FIN")


# Ejecución principal
if __name__ == "__main__":
    muestra()
