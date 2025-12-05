# -*- mode: python ; coding: utf-8 -*-
# Archivo de configuración PyInstaller para SANARTE
# Uso: pyinstaller sanarte.spec

block_cipher = None

a = Analysis(
    ['menu_principal.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),  # Incluir todo el código fuente
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'datetime',
        'glob',
        'argparse',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SANARTE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir ejecutable
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True = muestra consola, False = sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='sanarte_icon.ico' if os.path.exists('sanarte_icon.ico') else None,
)
