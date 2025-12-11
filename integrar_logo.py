"""
Script para integrar el logo TORO en el dashboard HTML
Convierte la imagen a base64 y la embede en el generador de dashboard
"""
import base64
import os

def convertir_imagen_a_base64(ruta_imagen):
    """Convierte una imagen a base64 para embedderla en HTML"""
    with open(ruta_imagen, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def obtener_mime_type(ruta_imagen):
    """Obtiene el MIME type de la imagen"""
    ext = os.path.splitext(ruta_imagen)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
    }
    return mime_types.get(ext, 'image/png')

def integrar_logo(ruta_imagen):
    """Integra el logo en dashboard_generator.py"""

    # Verificar que la imagen existe
    if not os.path.exists(ruta_imagen):
        print(f"❌ Error: No se encontró la imagen en {ruta_imagen}")
        print("\nColoca tu imagen (logo_toro.png) en la carpeta /home/user/Sanarte_finance/data/")
        return False

    print(f"✅ Imagen encontrada: {ruta_imagen}")

    # Convertir a base64
    print("🔄 Convirtiendo imagen a base64...")
    imagen_base64 = convertir_imagen_a_base64(ruta_imagen)
    mime_type = obtener_mime_type(ruta_imagen)

    print(f"✅ Conversión completada ({len(imagen_base64)} caracteres)")

    # Leer el archivo dashboard_generator.py
    dashboard_path = '/home/user/Sanarte_finance/src/reports/dashboard_generator.py'
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Crear el nuevo HTML con imagen base64
    nuevo_logo_html = f'''            <div class="logo-container">
                <img class="toro-logo" src="data:{mime_type};base64,{imagen_base64}" alt="Logo TORO">
            </div>'''

    # Buscar y reemplazar el SVG actual
    inicio_logo = contenido.find('            <div class="logo-container">')
    fin_logo = contenido.find('            </div>\n            <h1>TORO · Resumen de Cuentas</h1>')

    if inicio_logo == -1 or fin_logo == -1:
        print("❌ Error: No se encontró el bloque del logo en dashboard_generator.py")
        return False

    # Reemplazar
    nuevo_contenido = (
        contenido[:inicio_logo] +
        nuevo_logo_html + '\n' +
        contenido[fin_logo:]
    )

    # Guardar
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)

    print(f"✅ Logo integrado exitosamente en {dashboard_path}")
    print("\n📊 Ahora puedes generar el dashboard con:")
    print("   python src/main.py --reportes --sin-abrir")

    return True

if __name__ == "__main__":
    # Ruta de la imagen
    ruta_logo = '/home/user/Sanarte_finance/data/logo_toro.png'

    print("="*60)
    print("TORO - Integrador de Logo para Dashboard")
    print("="*60)
    print()

    integrar_logo(ruta_logo)
