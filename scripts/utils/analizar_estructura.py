"""
Script temporal para analizar la estructura de los archivos Excel
"""
import pandas as pd
import sys

def analizar_excel(ruta):
    print(f"\n{'='*80}")
    print(f"ANALIZANDO: {ruta}")
    print(f"{'='*80}\n")

    try:
        # Leer Excel
        df = pd.read_excel(ruta)

        print(f"INFORMACION GENERAL:")
        print(f"   - Total de filas: {len(df)}")
        print(f"   - Total de columnas: {len(df.columns)}")

        print(f"\nCOLUMNAS ENCONTRADAS:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. '{col}'")

        print(f"\nPRIMERAS 3 FILAS:")
        print(df.head(3).to_string())

        print(f"\nTIPOS DE DATOS:")
        print(df.dtypes)

        print(f"\nVALORES NO NULOS:")
        print(df.count())

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Analizar archivo Supervielle
    supervielle = r"C:\Users\mauri\OneDrive\Escritorio\PERSONALES, IA , AUTOS, DPTOS\1 - GPTS\SANARTE IA\Movimientos_Supervielle_003095775-002_2025_11_14_182045.xlsx"
    analizar_excel(supervielle)

    # Analizar archivo Galicia
    galicia = r"C:\Users\mauri\OneDrive\Escritorio\PERSONALES, IA , AUTOS, DPTOS\1 - GPTS\SANARTE IA\Extracto_CC661581991.xlsx"
    analizar_excel(galicia)
