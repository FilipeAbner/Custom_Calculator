# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['tkinter', 'tkinter.ttk']
hiddenimports += collect_submodules('src')
hiddenimports += collect_submodules('ui')
hiddenimports += collect_submodules('model')
hiddenimports += collect_submodules('util')


a = Analysis(
    ['/home/filipe-abner/Trabalhos/CienciadaComputacao/A_Personal_PRojects/Custom_Calculator/main.py'],
    pathex=['/home/filipe-abner/Trabalhos/CienciadaComputacao/A_Personal_PRojects/Custom_Calculator', '/home/filipe-abner/Trabalhos/CienciadaComputacao/A_Personal_PRojects/Custom_Calculator/src'],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Custom_Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
