import re

#Expresion regulares
lexemas = {
    'nomVariables': r'\b[a-z][a-z0-9]{0,9}\b',
    'nomArchivo': r'\b[a-z][a-z0-9]{0,9}.txt\b',
    'separador': r'[,;|]',
    'numero': r'[0-9]+',
    'coma': r',',
    'palabrasReservadas': r'\b(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODOS)\b',  
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

def regex_es_palabra_reservada(palabra):
    res = re.match(lexemas['palabrasReservadas'], palabra)
    return res!=None

def regex_es_comentario(linea):
  res = re.match(lexemas['comentario'], linea)
  return res!=None

#Codigo para que verifique si es un nombre de variable. Falta que cargue a la tabla
def es_nom_variable(t):
    ret = False
    if len(t)<=10 and t[0].islower():
        ret = es_nom_valido(t[1:])
    
    return ret

# Metodo recursivo, usado solo adentro de es_nom_variable
def es_nom_valido(t):
    ret = False
    if len(t)==0:
        ret=True
    else:
        if t[0].islower() or t[0].isnumeric():
            ret = es_nom_valido(t[1:])
    return ret

#Funcion que elimina espacios en blanco prescindibles
def eliminar_espacio(linea):
    linea = linea.strip()
    return linea

#Funcion para que verifique si una linea es comentario
def es_comentario(linea):
    # comentario = r'@\s*.*'
    if re.match(lexemas['comentario'],linea):
        tokens.append('comentario',linea)
        return tokens
    return False

#Funcion para que veririfique si una linea es palabra reservada
def es_palabra_reservada(linea):
    if re.match(lexemas['palabrasReservadas'], linea):
        tokens.append('palabrasReservadas',linea)
        return True
    return False



#Funcion que analiza linea por linea
def analiza_linea(archivo):
    while True:
        linea = archivo.readline()
        if not linea:
            break
        linea = eliminar_espacio(linea)
        if not es_comentario(linea) and not es_palabra_reservada(linea):
            tokens.append(linea)
        if es_comentario(linea) or es_palabra_reservada(linea):
            tokens.append(linea)
        if es_nom_variable(linea):
            tokens.append(linea)
        if es_nom_valido(linea):
            tokens.append(linea)
        if regex_es_nombre_de_variable(linea):
            tokens.append(linea)
        if regex_es_nombre_de_archivo(linea):
            tokens.append(linea)
        if es_nom_valido(linea) and not es_nom_variable(linea):
            tokens.append(linea)
        if es_nom_valido(linea) and not es_nom_variable(linea) and not es_nom_variable(linea):
            tokens.append(linea)

#Funcion para abrir archivo
def abrir_archivo(ruta_de_archivo):
    with open(ruta_de_archivo, 'r', encoding='UTF-8') as f:
        return f
    
def muestra():
    archivo = abrir_archivo("prueba.txt")
    analiza_linea(archivo)
    archivo.close()
    print(tokens)
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