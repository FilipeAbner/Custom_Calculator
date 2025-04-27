import sys, os, subprocess

script_dir   = os.path.dirname(os.path.realpath(__file__))
# Project root (where main.py and the src/ folder are)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Paths
main_py   = os.path.join(project_root, 'main.py')
src_dir   = os.path.join(project_root, 'src')
dist_dir  = os.path.join(
    project_root, 'dist',
    'distLinux'  if sys.platform.startswith('linux') else
    'distWindows'
)
build_dir = os.path.join(
    project_root, 'build',
    'buildLinux' if sys.platform.startswith('linux') else
    'buildWindows'
)
exe_name  = 'Custom_Calculator' + ('.exe' if sys.platform.startswith('win32') else '')

# Mount the PyInstaller command
command = [
    'pyinstaller',
    '--onefile',
    '--clean',           
    '--noconfirm',       
    # MAKE SURE PYINSTALLER LOOKS FOR ALL MODULES(I HATE THAT, MANY ATTEMPTS UNTIL DISCOVERING THIS):
    # - project_root (to resolve import src.ui.app)
    # - src_dir (to resolve import ui.*, model.*, util.*)
    '--paths', project_root,
    '--paths', src_dir,

    # EMBEDDING ALL SOURCE CODE as PYTHON, not as “data”:
    '--collect-submodules', 'src',
    '--collect-submodules', 'ui',
    '--collect-submodules', 'model',
    '--collect-submodules', 'util',

    # for external imports works
    '--hidden-import', 'tkinter',
    '--hidden-import', 'tkinter.ttk',

    # exe name and output directories
    '--name', exe_name,
    '--distpath', dist_dir,
    '--workpath', build_dir,
    '--specpath', project_root, 

    main_py  # entry script
]

# Run
subprocess.run(command)
