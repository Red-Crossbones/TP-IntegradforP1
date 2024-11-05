# Función para verificar sintaxis
# Importamos los tokens y la función abrir_archivo desde lexi
from lexi import tokens, abrir_archivo


# Función genérica de validación para CARGA y GUARDA
def validar_carga_guarda(tokens):
    # CARGA o GUARDA <nomArchivo> , <nomVariable>[ , <separador>]
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomArchivo', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        (len(tokens) == 4 or (len(tokens) == 6 and obtener_token(tokens, 'separador', 4)))):
        return True
    return False


# Modificación en verificar_sintaxis para usar la nueva función
def verificar_sintaxis(tokens):
    errores_por_linea = {}
    linea_tokens = []  # Tokens de la línea actual
    
    for token in tokens:
        if token[1] == 'fin_de_linea':  # Encontramos un EOL, procesamos la línea
            if linea_tokens:
                linea_actual = linea_tokens[0][2]  # Número de línea
                tipo = linea_tokens[0][0]  # La palabra reservada debe estar al inicio
                
                mensaje_error = None
                if tipo in ['CARGA', 'GUARDA']:  # Unificamos CARGA y GUARDA
                    if not validar_carga_guarda(linea_tokens):
                        mensaje_error = f"Sintaxis incorrecta para {tipo}."
                elif tipo == 'SEPARA':
                    if not validar_separa(linea_tokens):
                        mensaje_error = "Sintaxis incorrecta para SEPARA."
                elif tipo == 'AGREGA':
                    if not validar_agrega(linea_tokens):
                        mensaje_error = "Sintaxis incorrecta para AGREGA."
                elif tipo == 'ENCABEZADO':
                    if not validar_encabezado(linea_tokens):
                        mensaje_error = "Sintaxis incorrecta para ENCABEZADO."
                elif tipo == 'TODO':
                    if not validar_todo(linea_tokens):
                        mensaje_error = "Sintaxis incorrecta para TODO."
                else:
                    mensaje_error = "Comando desconocido."
                
                # Agrega el mensaje de error al diccionario si existe
                if mensaje_error:
                    if linea_actual not in errores_por_linea:
                        errores_por_linea[linea_actual] = []
                    errores_por_linea[linea_actual].append(mensaje_error)
            
            linea_tokens = []  # Reinicia la lista para la próxima línea
        else:
            linea_tokens.append(token)
    
    # Convierte el diccionario de errores en una lista de mensajes de error
    errores = [f"Error en línea {linea}: {', '.join(mensajes)}" for linea, mensajes in errores_por_linea.items()]
    return errores


# Función de ayuda para validar el siguiente token
def obtener_token(tokens, esperado, indice):
    # Verifica que el índice esté dentro del rango antes de intentar acceder
    if indice < len(tokens):
        return tokens[indice][1] == esperado
    return False  # Devuelve False si el índice está fuera de rango


# Funciones específicas de validación
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
    try:
        # Intentamos abrir el archivo y analizar los tokens
        abrir_archivo("prueba.txt")
        
        if not tokens:
            raise ValueError("Los tokens no son válidos o están vacíos.")
        
        errores = verificar_sintaxis(tokens)
        
        if errores:
            for error in errores:
                print(error)
        else:
            print("Todas las sentencias están correctamente escritas.")
    
    except FileNotFoundError:
        print("Error: El archivo no se encontró. Verifique la ruta y el nombre del archivo.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
