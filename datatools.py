# [---------------------------- Importaciones ---------------------------------]

import pandas as pd
from IPython.display import clear_output
from time import sleep
from tabulate import tabulate


# [------------------------------ Funciones -----------------------------------]

# ------------------------- Función 1: info_data -------------------------------

def info(df):
    '''
    Proporciona una visión detallada de un DataFrame de pandas, similar a df.info(),
    pero con información adicional como el porcentaje de valores nulos y el número de 
    valores únicos por columna.
    
    Parámetros:
    - df (pandas.DataFrame): DataFrame que se desea analizar.
    
    Salidas:
    - Imprime una tabla detallada con información sobre cada columna del DataFrame,
    incluyendo conteo de valores no nulos, nulos, porcentaje de nulos, tipo de dato
    y número de valores únicos.
 
    
    Ejemplo de uso:
    infodata(mi_dataframe)
    '''
    print("Pandas DataFrame")
    print(f"RangeIndex: {len(df)} entries, 0 to {len(df) - 1}")
    
    # Preparar datos para tabulate
    data = []
    for i, col in enumerate(df.columns):
      null_count = df[col].isnull().sum()
      pct_null = (null_count / len(df)) * 100
      unique_count = df[col].nunique()
      data.append([i, col, null_count, f"{pct_null:.2f}%", df[col].dtype, unique_count])
    
    # Imprimir tabla de columnas
    print(tabulate(data, headers=["#", "Column", "Null", "%Null", "Dtype", "Unique"], tablefmt="grid"))
    
    # Calcular el uso de memoria para cada columna
    memory_per_column = df.memory_usage(deep=True)
    
    # Sumar el uso de memoria de todas las columnas para obtener el total
    total_memory_usage = memory_per_column.sum()
    
    # Convertir de bytes a megabytes para comparar con df.info()
    total_memory_usage_mb = total_memory_usage / (1024 * 1024)
    
    print(f"Total memory usage (deep): {total_memory_usage_mb} MB")

    

# ------------------------- Función 3: dtype_converter -------------------------------

def unique(df, max_unique_values=12):
    '''
    Muestra los valores únicos y sus conteos para aquellas columnas cuyos 
    valores únicos sean iguales o menores al número especificado en 'max_unique_values'. 
    Útil para una rápida comprensión de las columnas con un bajo número 
    de valores únicos.

    Parámetros:
    - df (pandas.DataFrame): DataFrame que se desea analizar.
    - max_unique_values (int): Número máximo de valores únicos por columna para los que se desea imprimir información. 
      Por defecto es 12.

    Salidas: 
    - Imprime tablas detalladas para cada columna cuyos valores únicos son menores o iguales a 'max_unique_values', 
      mostrando los valores únicos, su conteo y su porcentaje de representación.

    Ejemplo de uso: 
    - unique(df) 
    - unique(df, max_unique_values=5)
    '''
    print(f"--> Conteo para cada valor único de columna con valores únicos menores o iguales a {max_unique_values}") 
    
    for col in df.columns:
        unique_count = df[col].nunique()  # Calcular el número de valores únicos para cada columna
        if unique_count <= max_unique_values and unique_count > 0:
            print(f"\nColumna: {col}")
            
            # Obtener conteos y porcentajes
            value_counts = df[col].value_counts()
            percentages = df[col].value_counts(normalize=True) * 100

            # Crear DataFrame con Value, Count, y Percentage
            data = pd.DataFrame({
                'Value': value_counts.index,
                'Count': value_counts.values,
                '%': percentages.values
            })

            try:
                # Dar formato con tabulate
                print(tabulate(data, headers=['Value', 'Count', '%'], tablefmt='grid', floatfmt=".2f"))

            except ModuleNotFoundError:
                print("Para una mejor visualización, instale 'tabulate': pip install tabulate")
                print("Se imprime DataFrame sin formatear como tabla")
                print(data.to_string(index=False))
                
            


# ------------------------- Función 3: dtype_converter -------------------------------
  
def dtype_converter(df):
    """
    Convierte los tipos de datos de las columnas de un DataFrame de pandas.

    Parámetros:
    df (pandas.DataFrame): DataFrame cuyos tipos de datos se van a convertir.

    Ejemplo de uso: 
    df = dtype_convertor(df)
    """
    # Cheatsheet de tipos de datos que se mostrará
    data_types_info = [
        ["int64", "-/+ 9,223,372,036,854,775,807"],
        ["int32", "-/+ 2,147,483,647"],
        ["int16", "-/+ 32,767"],
        ["int8", "-128 a 127"],
        ["uint8", "Enteros positivos. También uint16/32/64"],
        ["float64", "Precisión doble"],
        ["float32", "Precisión simple"],
        ["string", "Nombres, direcciones, identificadores"],
        ["category", "Textos con número limitado de valores únicos"],
        ["bool", "Verdadero o Falso"],
        ["object", "Datos mixtos, listas/diccionarios, caracteres no estándar, personalizados"],
        ["datetime", "Fechas y horas. 64[ns] default"],
        ["timedelta", "Diferencias de tiempo. 64[ns] default"]
    ]
    
    # Diccionario de formatos de fecha
    date_formats = {
            "1": "%Y-%m-%d",
            "2": "%d/%m/%Y",
            "3": "%m-%d-%Y %H:%M:%S",
            "4": '%Y-%m-%d %H:%M:%S'
    }

    try:
        from tabulate import tabulate
        print("Data types cheatsheet")
        print(tabulate(data_types_info, headers=["Tipo de Dato", "Descripción"], tablefmt="grid"))
    except ImportError:
        print("Cheatsheet de data types disponible con tabulate. Instálela con 'pip install tabulate'")
        
    for col in df.columns:
        print(f"\nColumna #{df.columns.get_loc(col)}: {col}")
        print(f"\nDtype inferido: {df[col].dtype}")
        print(f"Num. de valores únicos: {df[col].nunique()}")
        print("\nEjemplos de registros:")
        print(df[col].sample(3).tolist())
        print()

        while True:
            new_dtype = input("Ingrese el nuevo tipo de dato (deje en blanco para mantener el actual): ")
            
            if not new_dtype:
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    break
                
            try:
                if new_dtype.lower() == 'datetime' or (not new_dtype and isinstance(df[col], pd.Series) and pd.api.types.is_datetime64_any_dtype(df[col])):
                    print("\nOpciones de formato de fecha:")
                    for key, value in date_formats.items():
                        print(f"{key}: {value.replace('%Y', 'yyyy').replace('%m', 'mm').replace('%d', 'dd').replace('%H', 'HH').replace('%M', 'MM').replace('%S', 'SS')}")
                    print("I: Ingresar manualmente formato")
                    
                    while True:
                        format_option = input("Seleccione una opción (deje en blanco para mantener el formato actual): ")
                        try:
                            if format_option in date_formats:
                                df[col] = pd.to_datetime(df[col], format=date_formats[format_option])
                                print(f"Tipo de dato de '{col}' convertido a datetime usando el formato {date_formats[format_option]}.")
                                break
                            elif format_option.lower() == 'i':
                                print("Ingrese el formato (ejemplos: '%Y-%m-%d', '%d/%m/%Y %H:%M:%S')")
                                custom_format = input("Formato: ")
                                df[col] = pd.to_datetime(df[col], format=custom_format)
                                print(f"Tipo de dato de '{col}' convertido a datetime usando el formato personalizado.")
                                break
                            elif not format_option:
                                print(f"Se mantiene el formato actual de '{col}'.")
                                break
                            else:
                                print("Opción no válida. Por favor, seleccione una opción válida.")
                        except ValueError as ve:
                            print(f"Estructura de formato incorrecto: {ve}")
                            input("Presione Enter para re-ingresar formato...")
        
                else:
                    df[col] = df[col].astype(new_dtype)
                print(f"Tipo de dato de '{col}' convertido a {new_dtype}.")
                break
                
            except ValueError as ve:
                print(f"Error de valor: {ve}")
                input("Presione Enter para re-ingresar dtype deseado...") 
            except TypeError as te:
                print(f"Error de tipo: {te}")
                input("Presione Enter para re-ingresar dtype deseado...") 
            except Exception as e:
                print(f"Otro error en la conversión: {e}")
                input("Presione Enter para re-ingresar dtype deseado...") 

    
        clear_output()
        sleep(0.02)
    
    clear_output()
    df.info()
    print("Conversión finalizada.")
    return df

