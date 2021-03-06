# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
print(collect_data_files('aiohttp_xmlrpc'))

block_cipher = None

a = Analysis(['hamlog-agent.py'],
             binaries=[],
             datas=[('res', 'res')] + collect_data_files('aiohttp_xmlrpc'),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='HAMLOG Agent',
          icon='icon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='HAMLOG Agent')
app = BUNDLE(coll,
             name='HAMLOG Agent.app',
             icon='icon.icns',
             bundle_identifier='com.hamlog.agent',
             info_plist={
                 'LSUIElement': '1',
                 'CFBundleURLTypes': [
                     {
                         'CFBundleURLName': 'com.hamlog.agent',
                         'CFBundleURLSchemes': [ 'hamlogagent' ]
                     }
                 ]
             })
