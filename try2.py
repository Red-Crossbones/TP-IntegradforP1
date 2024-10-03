import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}.(txt|text|csv)\b',
    'separador': r'[,;|]',
    'numero': r'[0-9]+',
    'coma': r',',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)\b',
    'comentario': r'@\s*.*'
}

# Inicializar tokens
tokens = []


# Verificación usando expresiones regulares:
def regex_es_nombre_de_variable(palabra):
    return re.match(lexemas['nomVariables'], palabra) is not None


def regex_es_nombre_de_archivo(palabra):
    return re.match(lexemas['nomArchivo'], palabra) is not None


def regex_es_numero(palabra):
    return re.match(lexemas['numero'], palabra) is not None


def regex_es_palabra_reservada(palabra):
    return re.match(lexemas['palabrasReservadas'], palabra) is not None


def regex_es_comentario(palabra):
    return re.match(lexemas['comentario'], palabra) is not None


# Función para dividir la línea en palabras/separadores
def dividir_linea(linea):
    # Dividimos por espacios y separadores (, ; |) manteniéndolos en el resultado
    return re.split(r'(\s+|[,;|])', linea)


# Función que analiza línea por línea
def analiza_linea(archivo):
    for linea in archivo:
        palabras = dividir_linea(linea)  

        for palabra in palabras:
            if palabra.strip() == "": 
                continue
            # Comprobaciones de cada tipo de lexema
            if regex_es_comentario(palabra):
                tokens.append(('comentario', palabra))
                break  
            elif regex_es_palabra_reservada(palabra):
                tokens.append(('palabrasReservadas', palabra))
            elif regex_es_nombre_de_variable(palabra):
                tokens.append(('nomVariables', palabra))
            elif regex_es_nombre_de_archivo(palabra):
                tokens.append(('nomArchivo', palabra))
            elif regex_es_numero(palabra):
                tokens.append(('numero', palabra))
            elif re.match(lexemas['separador'], palabra):
                tokens.append(('separador', palabra))
            else:
                print(f"Error léxico en la palabra: '{palabra}'")
                tokens.append(('error', palabra))


# Función para abrir el archivo
def abrir_archivo(ruta_de_archivo):
    with open(ruta_de_archivo, 'r', encoding='UTF-8') as f:
        analiza_linea(f)


# Función que muestra los resultados de los tokens
def muestra():
    abrir_archivo('prueba.txt')
    for token in tokens:
        print(token)
    print("FIN")


# Ejecución principal
if __name__ == "__main__":
    muestra()
