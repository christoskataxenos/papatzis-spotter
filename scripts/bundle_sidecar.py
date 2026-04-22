import os
import shutil
import subprocess
import sys

def get_target_triple():
    import platform
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "x86_64-pc-windows-msvc"
    elif system == "darwin":
        return "x86_64-apple-darwin" if machine == "x86_64" else "aarch64-apple-darwin"
    elif system == "linux":
        return "x86_64-unknown-linux-gnu"
    return "x86_64-pc-windows-msvc" # Fallback

def bundle():
    # 1. Config
    analyzer_dir = os.path.join(os.getcwd(), 'analyzer')
    target_dir = os.path.join(os.getcwd(), 'src-tauri', 'binaries')
    triple = get_target_triple()
    binary_name = f"slop-engine-{triple}"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 2. Run PyInstaller
    # We use --onefile for a clean sidecar
    # We need to make sure tree-sitter-language-pack data is included
    print("Running PyInstaller...")
    cmd = [
        os.path.join(analyzer_dir, 'venv', 'Scripts', 'pyinstaller'),
        '--onefile',
        '--name', 'PapatzisEngine',
        '--clean',
        '--workpath', 'build',
        '--distpath', 'dist',
        'slop_engine.py'
    ]

    # Run from analyzer directory
    subprocess.run(cmd, cwd=analyzer_dir, check=True)

    # 3. Handle Binary
    source_exe = os.path.join(analyzer_dir, 'dist', 'PapatzisEngine.exe')
    target_exe = os.path.join(target_dir, f"{binary_name}.exe")
    print(f"Moving {source_exe} to {target_exe}...")
    shutil.copy2(source_exe, target_exe)
    print("Bundle complete! ✅")

if __name__ == "__main__":
    bundle()
