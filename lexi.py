import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,50}\.(txt|text|csv)\b',
    'separador': r'[,;]',
    'numero': r'[0-9]+',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)\b',
    'comentario': r'@\s*.*'
}

# Función para dividir la línea en palabras, separadores y espacios
def dividir_linea(linea):
    return re.split(r'(\s+|[,;])', linea)

# Función para analizar línea por línea y actualizar la lista de tokens
def analiza_linea(archivo, tokens, contenido):
    errores = []
    for linea_num, linea in enumerate(archivo, start=1):
        palabras = dividir_linea(linea)
        cant_palabras_reservadas = 0
        for palabra in palabras:
            if palabra is None or palabra.strip() == "":
                continue

            # Determinar tipo de token
            if re.fullmatch(lexemas['comentario'], palabra.strip()):
                break  # Ignorar comentarios
            elif re.fullmatch(lexemas['palabrasReservadas'], palabra.strip()):
                cant_palabras_reservadas += 1
                if cant_palabras_reservadas > 1:
                    errores.append(f"Error en la línea {linea_num}: más de una palabra reservada en una sola línea")
                    break
                agregar_token(tokens, palabra.strip(), 'palabrasReservadas', linea_num)
                contenido.append((palabra.strip(), 'palabrasReservadas', linea_num))
            elif re.fullmatch(lexemas['nomVariables'], palabra.strip()):
                agregar_token(tokens, palabra.strip(), 'nomVariables', linea_num)
                contenido.append((palabra.strip(), 'nomVariables', linea_num))
            elif re.fullmatch(lexemas['nomArchivo'], palabra.strip()):
                agregar_token(tokens, palabra.strip(), 'nomArchivo', linea_num)
                contenido.append((palabra.strip(), 'nomArchivo', linea_num))
            elif re.fullmatch(lexemas['numero'], palabra.strip()):
                agregar_token(tokens, palabra.strip(), 'numero', linea_num)
                contenido.append((palabra.strip(), 'numero', linea_num))
            elif re.fullmatch(lexemas['separador'], palabra.strip()):
                agregar_token(tokens, palabra.strip(), 'separador', linea_num)
                contenido.append((palabra.strip(), 'separador', linea_num))
            else:
                errores.append(f"Error léxico en la palabra: '{palabra.strip()}' en la línea {linea_num}")

        # Agregar el token de fin de línea
        contenido.append(('EOL', 'fin_de_linea', linea_num))

    return errores

# Función para agregar tokens únicos sin considerar el número de línea
def agregar_token(tokens, palabra, tipo, linea_num):
    if not any(token[0] == palabra and token[1] == tipo for token in tokens):
        tokens.append((palabra, tipo, linea_num))

# Función para abrir el archivo y generar los tokens
def abrir_archivo(ruta_de_archivo):
    tokens = []
    contenido = []
    with open(ruta_de_archivo, 'r', encoding='UTF-8') as archivo:
        errores = analiza_linea(archivo, tokens, contenido)
    return tokens, errores, contenido
