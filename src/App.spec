# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\stort\\Documents\\MobileMonsters\\TheMessengerBot\\src\\App.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\stort\\Documents\\MobileMonsters\\TheMessengerBot\\src\\MainAppModul', 'MainAppModul/'), ('C:\\Users\\stort\\Documents\\MobileMonsters\\TheMessengerBot\\Datas', 'Datas/'), ('C:\\Users\\stort\\Documents\\MobileMonsters\\TheMessengerBot\\src\\venv', 'Venv/')],
    hiddenimports=['MainAppModul.SupportAppModule.MessageCraft', 'MainAppModul.SupportAppModule.SendMessage', 'tkinter.ttk', 'selenium.webdriver.chrome.options', 'selenium.webdriver.common.keys', 'google.oauth2.credentials', 'googleapiclient.discovery', 'selenium', 'oauth2client.client', 'webdriver_manager', 'googleapiclient'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='App',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='App',
)
