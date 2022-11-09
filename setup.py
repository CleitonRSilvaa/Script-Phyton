import sys
from cx_Freeze import setup, Executable

#Cria uma programa executável 

# As dependências são detectadas automaticamente, mas pode ser necessário um ajuste fino.
# "packages": ["os"] is used as example only

build_exe_options = {"packages": ["os"], "includes": ["requests"]}
build_exe_options = {"packages": ["os"], "includes": ["pyodbc"]}

# base="Win32GUI" deve ser usado apenas para o aplicativo Windows GUI

base="Win32GUI"
setup(
    name="Application_BlockCard 2.2.1",
    version="2.2.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable( script = "main.py",
    initScript = None,
    base = None,
    targetName = "Application_BlockCard 2.2.1.exe",
    icon = None)],
)