import re
from lexi import tokens, abrir_archivo

# Función para verificar sintaxis
# Importamos los tokens y la función abrir_archivo desde lexi
import re
from lexi import tokens, abrir_archivo

# Función para verificar sintaxis línea por línea
def verificar_sintaxis(tokens):
    errores = []
    linea_tokens = []  # Tokens de la línea actual
    
    for token in tokens:
        if token[1] == 'fin_de_linea':  # Encontramos un EOL, procesamos la línea
            if linea_tokens:
                tipo = linea_tokens[0][0]  # La palabra reservada debe estar al inicio
                if tipo == 'CARGA':
                    if not validar_carga(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para CARGA.")
                elif tipo == 'GUARDA':
                    if not validar_guarda(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para GUARDA.")
                elif tipo == 'SEPARA':
                    if not validar_separa(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para SEPARA.")
                elif tipo == 'AGREGA':
                    if not validar_agrega(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para AGREGA.")
                elif tipo == 'ENCABEZADO':
                    if not validar_encabezado(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para ENCABEZADO.")
                elif tipo == 'TODO':
                    if not validar_todo(linea_tokens):
                        errores.append(f"Error en línea {linea_tokens[0][2]}: Sintaxis incorrecta para TODO.")
                else:
                    errores.append(f"Error en línea {linea_tokens[0][2]}: Comando desconocido.")
            linea_tokens = []  # Reinicia la lista para la próxima línea
        else:
            linea_tokens.append(token)
    
    return errores
  
# Función de ayuda para validar el siguiente token
def obtener_token(tokens, esperado, indice):
    return tokens[indice][1] == esperado if indice < len(tokens) else False

# Funciones específicas de validación
def validar_carga(tokens):
    # CARGA <nomArchivo> , <nomVariable>[ , <separador>]
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomArchivo', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        (len(tokens) == 4 or (len(tokens) == 6 and obtener_token(tokens, 'separador', 4)))):
        return True
    return False

def validar_guarda(tokens):
    # GUARDA <nomArchivo> , <nomVariable>[ , <separador>]
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomArchivo', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        (len(tokens) == 4 or (len(tokens) == 6 and obtener_token(tokens, 'separador', 4)))):
        return True
    return False

def validar_separa(tokens):
    # SEPARA <nomVariable1> , <nomVariable2> , (<nomColumna>|<numColumna>)
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomVariables', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        obtener_token(tokens, 'separador', 4) and
        (obtener_token(tokens, 'nomVariables', 5) or obtener_token(tokens, 'numero', 5))):
        return True
    return False

def validar_agrega(tokens):
    # AGREGA <nomVariable1> , <nomVariable2>
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomVariables', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        len(tokens) == 4):
        return True
    return False

def validar_encabezado(tokens):
    # ENCABEZADO <nomVariable>
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomVariables', 1) and
        len(tokens) == 2):
        return True
    return False

def validar_todo(tokens):
    # TODO <nomVariable> , <cantLíneas>
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomVariables', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'numero', 3) and
        len(tokens) == 4):
        return True
    return False

# Llamada principal para ejecutar el parser
if __name__ == "__main__":
    abrir_archivo("prueba.txt")  # Cargar el archivo y analizarlo
    errores = verificar_sintaxis(tokens)
    if errores:
        for error in errores:
            print(error)
    else:
        print("Todas las sentencias están correctamente escritas.")
