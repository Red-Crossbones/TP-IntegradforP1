import os
import csv
import re


class LexiErrorException(Exception):
    """Excepción personalizada para errores léxicos."""

    def __init__(self, message):
        super().__init__(message)


class ParserErrorException(Exception):
    """Excepción personalizada para errores sintácticos."""

    def __init__(self, message):
        super().__init__(message)


class InterpreteBari24:

    def __init__(self):
        self.tablas = {}  # Diccionario para almacenar las tablas cargadas

    def cargar(self, tablas, nom_arch, nom_variable=None, separador=','):
        """Carga una tabla desde un archivo CSV."""
        if not os.path.exists(nom_arch):
            raise FileNotFoundError(f"El archivo {nom_arch} no existe.")
        
        if separador == '':
            separador = ','

        if nom_variable is None:
            nom_variable = os.path.splitext(os.path.basename(nom_arch))[0]

        with open(nom_arch, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=separador)
            rows = list(reader)

        headers = rows[0]
        data = rows[1:]

        if len(headers) != len(set(headers)):
            raise ValueError("El archivo contiene encabezados duplicados.")

        max_cols = len(headers)
        for row in data:
            if len(row) < max_cols:
                row.extend([''] * (max_cols - len(row)))

        tablas[nom_variable] = {'headers': headers, 'rows': data}
        return tablas

    def guarda(self, tablas, nom_arch, nom_variable, separador=','):
        """Guarda una tabla en un archivo CSV."""
        if nom_variable not in tablas:
            raise ValueError(f"La tabla {nom_variable} no existe.")
        
        table = tablas[nom_variable]
        headers = table['headers']
        rows = table['rows']

        if separador == '':
            separador = ','

        with open(nom_arch, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=separador)
            writer.writerow(headers)
            writer.writerows(rows)
        return tablas

    def separa(self, tablas, tabla, nueva_columna, columna):
        """Separa una columna de una tabla en una nueva columna."""
        if tabla not in tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = tablas[tabla]
        headers = table['headers']
        rows = table['rows']

        if isinstance(columna, int):
            if columna < 0 or columna >= len(headers):
                raise IndexError(f"El índice de columna {columna} está fuera de rango.")
            idx = columna
        else:
            if columna not in headers:
                raise ValueError(f"La columna '{columna}' no existe en la tabla '{tabla}'.")
            idx = headers.index(columna)

        headers.append(nueva_columna)
        for row in rows:
            valor = row[idx]
            row.append(valor)

        return tablas

    def agrega(self, tablas, tabla, nueva_columna):
        """Agrega una nueva columna a la tabla."""
        if tabla not in tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = tablas[tabla]
        headers = table['headers']
        rows = table['rows']

        headers.append(nueva_columna)
        for row in rows:
            row.append('')

        return tablas

    def encabezado(self, tablas, tabla):
        """Obtiene los encabezados de una tabla."""
        if tabla not in tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = tablas[tabla]
        headers = table['headers']

        print(f"Encabezados de la tabla '{tabla}': {headers}")
        return tablas

    def todo(self, tablas, tabla, num_lineas):
        """Muestra las primeras 'num_lineas' de una tabla con paginación."""
        if tabla not in tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = tablas[tabla]
        rows = table['rows']
        num_lineas = int(num_lineas)

        for i in range(0, len(rows), num_lineas):
            print(f"Mostrando líneas {i + 1} a {min(i + num_lineas, len(rows))}:")
            for row in rows[i:i + num_lineas]:
                print(', '.join(row))
            print('-' * 50)

        return tablas

    def procesar_instrucciones(self, instrucciones):
        """
        Procesa una lista de instrucciones del lenguaje Bari24.
        Cada instrucción es una tupla: (función, [argumentos]).
        """
        tablas = self.tablas  # Trabajamos sobre el diccionario de tablas

        for instruccion, argumentos in instrucciones:
            try:
                tablas = instruccion(tablas, *argumentos)
            except Exception as e:
                print(f"Error al procesar la instrucción '{instruccion.__name__}': {e}")

        self.tablas = tablas  # Actualizamos el estado final
        return tablas

    def ejecutar_archivo(self, archivo):
        """Ejecuta las instrucciones de un archivo Bari24."""
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"El archivo {archivo} no existe.")

        print(f"Iniciando procesamiento del archivo '{archivo}'...")

        with open(archivo, 'r', encoding='utf-8') as file:
            instrucciones_texto = file.readlines()

        instrucciones = []
        for instruccion in instrucciones_texto:
            instruccion = instruccion.strip()
            if not instruccion or instruccion.startswith('@'):
                continue

            partes = instruccion.split()
            comando = partes[0]
            args = ' '.join(partes[1:]).split(',')

            args = [arg.strip() for arg in args if arg.strip() != '']

            if comando == "CARGA":
                instrucciones.append((self.cargar, args))
            elif comando == "GUARDA":
                instrucciones.append((self.guarda, args))
            elif comando == "SEPARA":
                args[2] = int(args[2]) if args[2].isdigit() else args[2]
                instrucciones.append((self.separa, args))
            elif comando == "AGREGA":
                instrucciones.append((self.agrega, args))
            elif comando == "ENCABEZADO":
                instrucciones.append((self.encabezado, args))
            elif comando == "TODO":
                args[1] = int(args[1])
                instrucciones.append((self.todo, args))
            else:
                print(f"Comando desconocido: {comando}")

        self.procesar_instrucciones(instrucciones)

    def analizar_entrada(self, entrada):
        """Método para analizar una entrada y dividirla en tokens."""
        # Definimos patrones para los diferentes tipos de tokens
        patrones = {
            'COMANDO': r'(CARGA|GUARDA|SEPARA|AGREGA|ENCABEZADO|TODO)',
            'IDENTIFICADOR': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'ENTERO': r'\d+',
            'COMA': r',',
            'ESPACIO': r'\s+',
        }

        # Unir todos los patrones y crear una expresión regular general
        regex = '|'.join(f'(?P<{key}>{pattern})' for key, pattern in patrones.items())
        tokens = []
        for match in re.finditer(regex, entrada):
            tipo = match.lastgroup
            valor = match.group(tipo)
            if tipo != 'ESPACIO':  # Ignorar los espacios
                tokens.append((tipo, valor))
        return tokens

    # Nuevas funciones para carga, guarda, y paginación de datos:
    def validar_guarda(self, tokens):
        """Valida la sintaxis de la instrucción 'GUARDA'."""
        if (self.obtener_token(tokens, 'palabrasReservadas', 0) and
            self.obtener_token(tokens, 'nomArchivo', 1) and
            self.obtener_token(tokens, 'separador', 2) and
            self.obtener_token(tokens, 'nomVariables', 3)):
            return True
        return False

    def obtener_token(self, tokens, esperado, indice):
        """Verifica si el token en la posición indicada coincide con el esperado."""
        if indice < len(tokens):
            return tokens[indice][1] == esperado
        return False
