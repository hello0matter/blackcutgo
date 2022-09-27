# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

dll_path="D:\Program Files\Python\Python37\Lib\site-packages\pyzbar"
a = Analysis(
    ['main.py','rc_obj.py'],
    pathex=['D:\\xxkjrj\\blackcutgo\\blackgo_gui\\qt__source'],
    binaries=[(dll_path+'\libiconv.dll','.'),(dll_path+'\libzbar-64.dll','.')],
    datas=[],
    hiddenimports=[],
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
    name='main',
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
	icon='D:\\xxkjrj\\blackcutgo\\blackgo_gui\\qt__source\\ma.ico'
)
