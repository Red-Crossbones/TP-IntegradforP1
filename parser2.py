import csv
import os


class InterpreteBari24:

    def __init__(self):
        self.tablas = {}  # Diccionario para almacenar las tablas como variables

    def cargar(self, nom_arch, nom_variable, separador=','):
        """Carga una tabla desde un archivo CSV."""
        if not os.path.exists(nom_arch):
            raise FileNotFoundError(f"El archivo {nom_arch} no existe.")
        
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

        with open(nom_arch, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=separador)
            writer.writerow(headers)  # Escribir encabezados
            writer.writerows(rows)  # Escribir filas

    def separa(self, nom_variable1, nom_variable2, columna):
        """Separa una columna de una tabla y la guarda como otra tabla."""
        if nom_variable1 not in self.tablas:
            raise ValueError(f"La tabla {nom_variable1} no existe.")
        
        table = self.tablas[nom_variable1]
        headers = table['headers']
        rows = table['rows']

        # Determinar el índice de la columna
        if isinstance(columna, int):
            col_index = columna - 1
        elif isinstance(columna, str):
            col_index = headers.index(columna)
        else:
            raise ValueError("La columna debe ser un nombre o un número.")

        # Extraer la columna
        new_headers = [headers[col_index]]
        new_rows = [[row[col_index]] for row in rows]

        self.tablas[nom_variable2] = {'headers': new_headers, 'rows': new_rows}

    def agrega(self, nom_variable1, nom_variable2):
        """Agrega una columna de una tabla a otra."""
        if nom_variable1 not in self.tablas or nom_variable2 not in self.tablas:
            raise ValueError("Una o ambas tablas no existen.")
        
        table1 = self.tablas[nom_variable1]
        table2 = self.tablas[nom_variable2]

        if len(table2['headers']) != 1:
            raise ValueError("La tabla que se agrega debe tener exactamente una columna.")
        if len(table1['rows']) != len(table2['rows']):
            raise ValueError("Las tablas deben tener el mismo número de filas.")

        # Agregar la columna
        new_header = table2['headers'][0]
        table1['headers'].append(new_header)
        for row1, row2 in zip(table1['rows'], table2['rows']):
            row1.append(row2[0])

    def encabezado(self, nom_variable):
        """Muestra los encabezados de una tabla."""
        if nom_variable not in self.tablas:
            raise ValueError(f"La tabla {nom_variable} no existe.")
        
        headers = self.tablas[nom_variable]['headers']
        print("Encabezados:", ', '.join(headers))

    def todo(self, nom_variable, cant_lineas):
        """Muestra el contenido de una tabla por páginas."""
        if nom_variable not in self.tablas:
            raise ValueError(f"La tabla {nom_variable} no existe.")
        
        table = self.tablas[nom_variable]
        headers = table['headers']
        rows = table['rows']

        print("Encabezados:", ', '.join(headers))
        for i in range(0, len(rows), cant_lineas):
            print(f"Página {i // cant_lineas + 1}")
            for row in rows[i:i + cant_lineas]:
                print(', '.join(row))
            input("Presione Enter para continuar...")

    def procesar_instruccion(self, instruccion):
        """Procesa una instrucción del lenguaje Bari24."""
        partes = instruccion.strip().split()
        comando = partes[0]
        args = ' '.join(partes[1:]).split(',')

        if comando == "CARGA":
            self.cargar(args[0].strip(), args[1].strip(), args[2].strip() if len(args) > 2 else ',')
        elif comando == "GUARDA":
            self.guarda(args[0].strip(), args[1].strip(), args[2].strip() if len(args) > 2 else ',')
        elif comando == "SEPARA":
            columna = int(args[2]) if args[2].strip().isdigit() else args[2].strip()
            self.separa(args[0].strip(), args[1].strip(), columna)
        elif comando == "AGREGA":
            self.agrega(args[0].strip(), args[1].strip())
        elif comando == "ENCABEZADO":
            self.encabezado(args[0].strip())
        elif comando == "TODO":
            self.todo(args[0].strip(), int(args[1].strip()))
        else:
            raise ValueError(f"Comando desconocido: {comando}")

    def ejecutar_archivo(self, nombre_archivo):
        """Lee y ejecuta un archivo de comandos Bari24."""
        if not os.path.exists(nombre_archivo):
            raise FileNotFoundError(f"El archivo {nombre_archivo} no existe.")
        
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:  # Ignorar líneas vacías
                    self.procesar_instruccion(linea)
