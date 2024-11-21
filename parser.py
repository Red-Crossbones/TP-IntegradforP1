# Función para verificar sintaxis
# Importamos los tokens y la función abrir_archivo desde lexi
from lexi import abrir_archivo

sentencias = []

# Modificación en verificar_sintaxis para usar la nueva función
def verificar_sintaxis(tokens):
    instrucciones = []
    errores_por_linea = {}
    linea_tokens = []  # Tokens de la línea actual
    
    for token in tokens:
        if token[1] == 'fin_de_linea':  # Encontramos un EOL, procesamos la línea
            if linea_tokens:
                argumentos = []
                linea_actual = linea_tokens[0][2]  # Número de línea
                tipo = linea_tokens[0][0]  # La palabra reservada debe estar al inicio
                
                mensaje_error = None
                if tipo == 'GUARDA':  # Unificamos CARGA y GUARDA
                    if validar_guarda(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:],start=1):
                            if item[0] != "," or (index == len(linea_tokens[1:]) and item[1] == "separador"):
                                argumentos.append(item[0])    
                        instrucciones.append((ejecutar_guarda,argumentos))
                    else:
                        mensaje_error = "Sintaxis incorrecta para GUARDA."
                elif tipo == 'CARGA':
                    if validar_carga(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:],start=1):
                            if item[0] != "," or (index == len(linea_tokens[1:]) and item[1] == "separador"):
                                argumentos.append(item[0])                                
                        instrucciones.append((ejecutar_carga,argumentos))
                    else:
                        mensaje_error = "Sintaxis incorrecta para CARGA."
                elif tipo == 'SEPARA':
                    if validar_separa(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:]):
                            if item[0] != ",":
                                argumentos.append(item[0])    
                        instrucciones.append((ejecutar_separa,argumentos))
                    else:
                        mensaje_error = "Sintaxis incorrecta para SEPARA."
                elif tipo == 'AGREGA':
                    if validar_agrega(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:]):
                            if item[0] != ",":
                                argumentos.append(item[0])    
                        instrucciones.append((ejecutar_agrega,argumentos))
                    else:
                        mensaje_error = "Sintaxis incorrecta para AGREGA."
                elif tipo == 'ENCABEZADO':
                    if validar_encabezado(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:]):
                            if item[0] != ",":
                                argumentos.append(item[0])    
                        instrucciones.append((ejecutar_encabezado,argumentos))
                    else:
                        mensaje_error = "Sintaxis incorrecta para ENCABEZADO."
                elif tipo == 'TODO':
                    if validar_todo(linea_tokens):
                        for index, item in enumerate(linea_tokens[1:]):
                            if item[0] != ",":
                                argumentos.append(item[0])
                        instrucciones.append((ejecutar_todo,argumentos))
                    else:
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
    return errores, instrucciones


# Función de ayuda para validar el siguiente token
def obtener_token(tokens, esperado, indice):
    # Verifica que el índice esté dentro del rango antes de intentar acceder
    if indice < len(tokens):
        return tokens[indice][1] == esperado
    return False  # Devuelve False si el índice está fuera de rango


# Función genérica de validación para CARGA y GUARDA
def validar_guarda(tokens):
    # GUARDA <nomArchivo> , <nomVariable>[ , <separador>]
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomArchivo', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        (len(tokens) == 4 or (len(tokens) == 6 and obtener_token(tokens, 'separador', 4)))):
        return True
    return False

# Función genérica de validación para CARGA y GUARDA
def validar_carga(tokens):
    # CARGA <nomArchivo> , <nomVariable>[ , <separador>]
    if (obtener_token(tokens, 'palabrasReservadas', 0) and
        obtener_token(tokens, 'nomArchivo', 1) and
        obtener_token(tokens, 'separador', 2) and
        obtener_token(tokens, 'nomVariables', 3) and
        (len(tokens) == 4 or (len(tokens) == 6 and obtener_token(tokens, 'separador', 4)))):
        return True
    return False

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

# Función para cargar un archivo como tabla
def ejecutar_carga(tablas, nom_arch, nom_variable, separador=','):
    try:
        with open(nom_arch, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        # Convertir líneas en listas de campos
        tabla = [linea.strip().split(separador) for linea in lineas]
        tablas[nom_variable] = tabla
        print(f"Tabla '{nom_variable}' cargada con éxito desde '{nom_arch}'.")
        return tablas
    except Exception as e:
        print(f"Error al cargar archivo '{nom_arch}': {e}")
        return tablas

# Función para guardar una tabla en un archivo
def ejecutar_guarda(tablas, nom_arch, nom_variable, separador=','):
    if nom_variable not in tablas:
        print(f"Error: La variable '{nom_variable}' no existe.")
        return tablas
    try:
        with open(nom_arch, 'w', encoding='utf-8') as archivo:
            for fila in tablas[nom_variable]:
                archivo.write(separador.join(map(str, fila)) + '\n')
        print(f"Tabla '{nom_variable}' guardada con éxito en '{nom_arch}'.")
        return tablas
    except Exception as e:
        print(f"Error al guardar archivo '{nom_arch}': {e}")
        return tablas

# Función para separar una columna como nueva tabla
def ejecutar_separa(tablas, nom_variable1, nom_variable2, columna):
    if nom_variable1 not in tablas:
        print(f"Error: La variable '{nom_variable1}' no existe.")
        return tablas
    try:
        tabla = tablas[nom_variable1]
        indice_columna = columna if isinstance(columna, int) else tabla[0].index(columna)
        nueva_tabla = [[fila[indice_columna]] for fila in tabla]
        tablas[nom_variable2] = nueva_tabla
        print(f"Columna '{columna}' separada como nueva tabla '{nom_variable2}'.")
        return tablas
    except ValueError:
        print(f"Error: La columna '{columna}' no existe en la tabla '{nom_variable1}'.")
        return tablas
    except Exception as e:
        print(f"Error al separar columna '{columna}': {e}")
        return tablas

# Función para agregar una columna de una tabla a otra
def ejecutar_agrega(tablas, nom_variable1, nom_variable2):
    if nom_variable1 not in tablas or nom_variable2 not in tablas:
        print(f"Error: Una de las variables '{nom_variable1}' o '{nom_variable2}' no existe.")
        return tablas
    try:
        tabla1 = tablas[nom_variable1]
        tabla2 = tablas[nom_variable2]
        if len(tabla2[0]) != 1:
            print(f"Error: La tabla '{nom_variable2}' no tiene exactamente una columna.")
            return tablas
        if len(tabla1) != len(tabla2):
            print(f"Error: Las tablas '{nom_variable1}' y '{nom_variable2}' no tienen la misma cantidad de filas.")
            return tablas
        for i, fila in enumerate(tabla1):
            fila.append(tabla2[i][0])
        print(f"Columna de '{nom_variable2}' agregada a la tabla '{nom_variable1}'.")
        return tablas
    except Exception as e:
        print(f"Error al agregar columna: {e}")
        return tablas

# Función para mostrar encabezados de una tabla
def ejecutar_encabezado(tablas, nom_variable):
    if nom_variable not in tablas:
        print(f"Error: La variable '{nom_variable}' no existe.")
        return tablas
    try:
        encabezados = tablas[nom_variable][0]
        print(f"Encabezados de '{nom_variable}': {', '.join(encabezados)}")
        return tablas
    except Exception as e:
        print(f"Error al mostrar encabezados: {e}")
        return tablas

# Función para mostrar contenido paginado de una tabla
def ejecutar_todo(tablas, nom_variable, cant_lineas):
    if nom_variable not in tablas:
        print(f"Error: La variable '{nom_variable}' no existe.")
        return tablas
    try:
        tabla = tablas[nom_variable]
        encabezados = tabla[0]
        cant_lineas = int(cant_lineas)
        print('\t'.join(encabezados))
        for i in range(1, len(tabla), cant_lineas):
            pagina = tabla[i:i + cant_lineas]
            for fila in pagina:
                print('\t'.join(map(str, fila)))
            input("Presiona Enter para continuar...")
        return tablas
    except Exception as e:
        print(f"Error al mostrar la tabla: {e}")
        return tablas
        
class LexiErrorException(Exception):
    """Exception raised for custom error scenarios.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ParserErrorException(Exception):
    """Exception raised for custom error scenarios.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Llamada principal para ejecutar el parser
if __name__ == "__main__":
    try:
        # Intentamos abrir el archivo y analizar los tokens
        tokens, erroresLexi, contenido = abrir_archivo("prueba_v2.txt")
        
        if not tokens:
            raise ValueError("Los tokens no son válidos o están vacíos.")
        if erroresLexi:
            for error in erroresLexi:
                print(error)
            raise LexiErrorException("Se han encontrado errores léxicos.")

        errores, instrucciones = verificar_sintaxis(contenido)
        
        if errores:
            for error in errores:
                print(error)
            raise ParserErrorException("Se han encontrado errores Sintácticos.")
        
        tablas = {}
        for instruccion, argumentos in instrucciones:
            tablas = instruccion(tablas,*argumentos)
    
    except FileNotFoundError:
        print("Error: El archivo no se encontró. Verifique la ruta y el nombre del archivo.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except LexiErrorException or ParserErrorException as e:
        print(e)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
