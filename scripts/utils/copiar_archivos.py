import shutil
import os
from glob import glob

origen = r"C:\Users\mauri\OneDrive\Escritorio\PERSONALES, IA , AUTOS, DPTOS\1 - GPTS\SANARTE IA"
destino = r"C:\Users\mauri\OneDrive\Escritorio\CLAUDE\sanarte_financiero\input"

archivos = glob(os.path.join(origen, "*.xlsx"))

for archivo in archivos:
    nombre = os.path.basename(archivo)
    destino_completo = os.path.join(destino, nombre)
    shutil.copy2(archivo, destino_completo)
    print(f"Copiado: {nombre}")

print(f"\nTotal: {len(archivos)} archivos copiados")
