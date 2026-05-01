# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['analyzer/slop_engine.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tree_sitter', 
        'tree_sitter_language_pack', 
        'pydantic',
        'analyzer.logic_analyzer',
        'analyzer.naming_analyzer',
        'analyzer.similarity_analyzer',
        'analyzer.structural_analyzer',
        'analyzer.comment_analyzer',
        'analyzer.redundancy_analyzer',
        'analyzer.statistical_analyzer',
        'analyzer.semantic_analyzer',
        'analyzer.scoring_engine',
        'analyzer.suspicion_analyzer',
        'analyzer.integrity_analyzer',
        'analyzer.models',
        'analyzer.base'
    ],
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
    name='PapatzisEngine',
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
