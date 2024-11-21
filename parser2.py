import os
import csv


class InterpreteBari24:

    def __init__(self):
        self.tablas = {}  # Diccionario para almacenar las tablas cargadas

    def cargar(self, nom_arch, nom_variable, separador=','):
        """Carga una tabla desde un archivo CSV."""
        if not os.path.exists(nom_arch):
            raise FileNotFoundError(f"El archivo {nom_arch} no existe.")
        
        if separador == '':  # Si el separador está vacío, usar coma por defecto
            separador = ','

        with open(nom_arch, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=separador)
            rows = list(reader)

        # Usar la primera línea como encabezados
        headers = rows[0]
        data = rows[1:]

        # Completar filas incompletas
        max_cols = len(headers)
        for row in data:
            row.extend([''] * (max_cols - len(row)))

        # Guardar la tabla en el diccionario
        self.tablas[nom_variable] = {'headers': headers, 'rows': data}

    def guarda(self, nom_arch, nom_variable, separador=','):
        """Guarda una tabla en un archivo CSV."""
        if nom_variable not in self.tablas:
            raise ValueError(f"La tabla {nom_variable} no existe.")
        
        table = self.tablas[nom_variable]
        headers = table['headers']
        rows = table['rows']

        if separador == '':  # Si el separador está vacío, usar coma por defecto
            separador = ','

        with open(nom_arch, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=separador)
            writer.writerow(headers)  # Escribir encabezados
            writer.writerows(rows)  # Escribir filas

    def separa(self, tabla, nueva_columna, columna):
        """Separa una columna de una tabla en una nueva columna."""
        if tabla not in self.tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = self.tablas[tabla]
        headers = table['headers']
        rows = table['rows']

        # Asegurarse de que la columna existe
        if columna not in headers:
            raise ValueError(f"La columna {columna} no existe en la tabla {tabla}.")
        
        # Separar la columna
        idx = headers.index(columna)
        nueva_columna_idx = len(headers)
        headers.append(nueva_columna)

        for row in rows:
            valor = row[idx]
            row.append(valor)  # Se agrega el valor de la columna original a la nueva columna

    def agrega(self, tabla, nueva_columna):
        """Agrega una nueva columna a la tabla."""
        if tabla not in self.tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = self.tablas[tabla]
        headers = table['headers']
        rows = table['rows']

        # Agregar la nueva columna a los encabezados
        headers.append(nueva_columna)

        # Agregar valores vacíos a todas las filas
        for row in rows:
            row.append('')

    def encabezado(self, tabla):
        """Obtiene los encabezados de una tabla."""
        if tabla not in self.tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = self.tablas[tabla]
        headers = table['headers']

        return headers

    def todo(self, tabla, valor):
        """Realiza alguna operación en toda la tabla (ejemplo de operación)."""
        if tabla not in self.tablas:
            raise ValueError(f"La tabla {tabla} no existe.")
        
        table = self.tablas[tabla]
        rows = table['rows']

        # Realizar una operación en todas las filas (aquí un ejemplo de multiplicar por un valor)
        for row in rows:
            for idx, cell in enumerate(row):
                if cell.isdigit():
                    row[idx] = str(int(cell) * valor)

    def procesar_instruccion(self, instruccion):
        """Procesa una instrucción del lenguaje Bari24."""
        partes = instruccion.strip().split()
        comando = partes[0]
        args = ' '.join(partes[1:]).split(',')

        # Asegurarse de que no haya parámetros vacíos innecesarios
        args = [arg.strip() for arg in args if arg.strip() != '']

        if comando == "CARGA":
            self.cargar(args[0], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else ',')
        elif comando == "GUARDA":
            self.guarda(args[0], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else ',')
        elif comando == "SEPARA":
            columna = int(args[2]) if args[2].strip().isdigit() else args[2].strip()
            self.separa(args[0], args[1], columna)
        elif comando == "AGREGA":
            self.agrega(args[0], args[1])
        elif comando == "ENCABEZADO":
            self.encabezado(args[0])
        elif comando == "TODO":
            self.todo(args[0], int(args[1]))
        else:
            raise ValueError(f"Comando desconocido: {comando}")
    
    def ejecutar_archivo(self, archivo):

        """Ejecuta las instrucciones de un archivo Bari24."""
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"El archivo {archivo} no existe.")
        
        with open(archivo, 'r', encoding='utf-8') as file:
            instrucciones = file.readlines()
        
        for instruccion in instrucciones:
            instruccion = instruccion.strip()
            if not instruccion or instruccion.startswith('@'):  # Ignorar líneas vacías o que empiezan con '@'
                continue
            try:
                self.procesar_instruccion(instruccion)
            except ValueError as e:
                print(f"Error al procesar la instrucción: {e}")
