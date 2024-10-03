import re

#Expresion regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}.(txt|text|csv)\b',
    'separador': r'[,;|]',
    'numero': r'[0-9]+',
    'coma': r',',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)\b',  
    'comentario': r'@\s*.*'
}

#Inicializar tokens
tokens = []

## Verificacion usando expresiones regulares:

def regex_es_nombre_de_variable(palabra):
    res = re.match(lexemas['nomVariables'], palabra)
    return res!=None

def regex_es_nombre_de_archivo(palabra):
    res = re.match(lexemas['nomArchivo'], palabra)
    return res!=None

def regex_es_numero(palabra):
  res = re.match(lexemas['numero'],palabra)
  return res!=None

def regex_es_palabra_reservada(palabra):
    res = re.match(lexemas['palabrasReservadas'], palabra)
    return res!=None

def regex_es_comentario(linea):
  res = re.match(lexemas['comentario'], linea)
  return res!=None

# Función para dividir la línea en palabras/separadores
def dividir_linea(linea):
    return re.split(lexemas['separador'] + '|' + lexemas['coma'], linea)


# Función que analiza línea por línea
def analiza_linea(archivo):
    for linea in archivo:
        palabras = dividir_linea(linea)

        for palabra in palabras:
            if palabra.strip() == "":
                continue
            # Comprobaciones de cada tipo de lexema
            if regex_es_comentario(palabra):
                tokens.append(('Comentario', linea))
                break
            elif regex_es_palabra_reservada(palabra):
                tokens.append(('Palabras Reservadas', linea))
            elif regex_es_nombre_de_variable(palabra):
                tokens.append(('Nombre Variable', linea))
            elif regex_es_nombre_de_archivo(palabra):
                tokens.append(('nomArchivo', linea))
            elif regex_es_numero(palabra):
                tokens.append(('numero', linea))
            elif re.match(lexemas['separador'], palabra):
                tokens.append(('separador', linea))
            else:
                print(f"Error léxico en la palabra: '{palabra}'")
                tokens.append(('error', linea))


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
