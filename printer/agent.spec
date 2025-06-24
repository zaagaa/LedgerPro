# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['agent.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('D:\\BusinessApp\\.venv\\Lib\\site-packages\\escpos\\capabilities.json', 'escpos'),
    ],
    hiddenimports=[
        'win32print',
        'win32api',
        'win32con',
        'win32file',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['escpos.printer.usb'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
