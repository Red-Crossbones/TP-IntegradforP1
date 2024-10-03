import re

# Expresiones regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}\.txt\b',
    'separador': r'[,;|]',
    'numero': r'[0-9]+',
    'coma': r',',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODOS)\b',
    'comentario': r'@\s*.*'
}

# Inicializar tokens
tokens = []

# Verificación usando expresiones regulares:
def regex_es_nombre_de_variable(palabra):
    return re.match(lexemas['nomVariables'], palabra) is not None

def regex_es_nombre_de_archivo(palabra):
    return re.match(lexemas['nomArchivo'], palabra) is not None

# Función que elimina espacios en blanco prescindibles
def eliminar_espacio(linea):
    return linea.strip()

# Función para que verifique si una línea es comentario
def es_comentario(linea):
    if re.match(lexemas['comentario'], linea):
        tokens.append(('comentario', linea))
        return True
    return False

# Función para verificar si una línea es palabra reservada
def es_palabra_reservada(linea):
    if re.match(lexemas['palabrasReservadas'], linea):
        tokens.append(('palabrasReservadas', linea))
        return True
    return False

# Función que analiza línea por línea
def analiza_linea(archivo):
    for linea in archivo:
        linea = eliminar_espacio(linea)

        # Comprobaciones de cada tipo de lexema
        if es_comentario(linea):
            continue
        elif es_palabra_reservada(linea):
            continue
        elif regex_es_nombre_de_variable(linea):
            tokens.append(('nomVariables', linea))
        elif regex_es_nombre_de_archivo(linea):
            tokens.append(('nomArchivo', linea))
        else:
            print(f"Error léxico en la línea: {linea}")
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

#Nombres de archivos
def esVarArc(t, tabla, p):
    resp = False
    if len(t) == 0:
        if p not in tabla:
            tabla[p] = 'nomVariable'
    elif t[0] == ' ':
        if p not in tabla:
            tabla[p] = 'nomVariable'
        resp = lexi(t[1:], tabla)
    elif t[0] in SEPARADORES:
        if p not in tabla:
            tabla[p] = 'nomVariable'
        if t[0] not in tabla:
            tabla[t[0]] = 'separador'
        resp = lexi(t[1:], tabla)
    elif t[0].isalnum() and t[0].islower():
        p += t[0]
        resp = esVarArc(t[1:], tabla, p)
    elif t[0] not in NOVALIDOS:
        p += t[0]
        resp = esArc(t[1:], tabla, p)
    else:
        if p not in tabla:
            tabla[p] = ''
        resp = True
    return resp

def esArc(t, tabla, p):
    resp = False
    if len(t) == 0:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
    elif t[0] == ' ':
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        resp = lexi(t[1:], tabla)
    elif t[0] in SEPARADORES:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        if t[0] not in tabla:
            tabla[t[0]] = 'separador'
        resp = lexi(t[1:], tabla)
    elif t[0] not in NOVALIDOS:
        p += t[0]
        resp = esArc(t[1:], tabla, p)
    else:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        resp = True
    return resp

def esNumArc(t, tabla, p):
    resp = False
    if len(t) == 0:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
    elif t[0] == ' ':
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        resp = lexi(t[1:], tabla)
    elif t[0] in SEPARADORES:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        if t[0] not in tabla:
            tabla[t[0]] = 'separador'
        resp = lexi(t[1:], tabla)
    elif t[0] not in NOVALIDOS:
        p += t[0]
        resp = esNumArc(t[1:], tabla, p)
    else:
        if p not in tabla and '.' in p:
            tabla[p] = 'nomArch'
        resp = True
    return resp

def lexi(texto, tabla):
    resp = False
    if len(texto) > 0:
        if texto[0].isalpha(): #puede ser variable o archivo
            palabra = texto[0]
            resp = esVarArc(texto[1:], tabla, palabra)
        elif texto[0].isnumeric(): #puede ser numero o archivo
            resp = esNumArc(texto[1:], tabla, palabra)
        elif texto[0] in SEPARADORES:
            if texto[0] not in tabla:
                tabla[texto[0]] = 'separador'
            resp = lexi(texto[1:], tabla)
        elif texto[0] == ' ':
            resp = lexi(texto[1:], tabla)
        else:
            resp = True
    return resp

def muestra(t, error):
    if error:
        print('ERROR!')
    print('Tabla de símbolos de palabra.txt')
    for lin in t:
        print(t[lin], lin)


###############################################################################
################                    MAIN                  #####################
###############################################################################

NOVALIDOS = '\/:*?"<>|'
SEPARADORES = ',;'
entrada = open('prueba.txt', 'r', encoding='UTF-8')
lineas = entrada.readlines()
entrada.close()

error = False
i = 0
tablaSimbolos = {}

while not error and i < len(lineas):
    lin = lineas[i]
    i += 1
    if lin[0] == '@':
        continue
    error = lexi(lin.strip('\n'), tablaSimbolos)

muestra(tablaSimbolos, error)
