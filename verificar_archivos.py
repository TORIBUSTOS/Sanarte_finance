import os

archivos = [
    r"C:\Users\mauri\OneDrive\Escritorio\PERSONALES, IA , AUTOS, DPTOS\1 - GPTS\SANARTE IA\Movimientos_Supervielle_003095775-002_2025_11_14_182045.xlsx",
    r"C:\Users\mauri\OneDrive\Escritorio\PERSONALES, IA , AUTOS, DPTOS\1 - GPTS\SANARTE IA\Extracto_CC661581991.xlsx"
]

for archivo in archivos:
    nombre = os.path.basename(archivo)
    existe = os.path.exists(archivo)
    print(f"{nombre}: {'EXISTE' if existe else 'NO EXISTE'}")
    if existe:
        print(f"  Tamaño: {os.path.getsize(archivo)} bytes")
