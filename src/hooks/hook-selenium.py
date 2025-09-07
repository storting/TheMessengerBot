from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('selenium')

datas += collect_all('selenium')[0]
binaries += collect_all('selenium')[1]
hiddenimports += collect_all('selenium')[2]