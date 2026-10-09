from pathlib import Path
root = Path(SPECPATH)
patch = root.parent
builders = [(str(patch / folder / file), 'runtime/' + folder) for folder, file in
            [('terrain', 'build_labels.py'), ('wizard', 'build_templates.py'),
             ('multiplayer', 'build_missions.py'), ('ui', 'build_addon.py')]]
a = Analysis([str(root / 'prepare.py')],
             pathex=[str(root), str(patch)], binaries=[], datas=builders,
             hiddenimports=['validate_campaign', 'validate_resistance', 'build_labels'],
             hookspath=[], hooksconfig={}, runtime_hooks=[],
             excludes=['tkinter', 'PyQt5', 'PyQt6', 'PySide6', 'opencc', 'numpy', 'scipy', 'PIL'],
             noarchive=False)
# Microsoft prerequisites must come from Microsoft's installer, not our payload.
a.binaries = [entry for entry in a.binaries if not Path(entry[0]).name.lower().startswith(('vcruntime', 'msvcp'))]
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='cwrc-prepare',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
          console=True, disable_windowed_traceback=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='cwrc-prepare')
