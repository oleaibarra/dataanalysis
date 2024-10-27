import pandas as pd
from IPython.display import clear_output
from time import sleep

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
        print("Ejemplos de registros:", df[col].sample(3).tolist())
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
    print("Revisión finalizada.")
    return df