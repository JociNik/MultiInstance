from colorama import init
import os
import subprocess
import json
from configparser import ConfigParser

from config.juegos import listaJuegos

def ConsoleLog(string):
     print(f'\033[0m{string}')

class Instancia:
    def __init__(self, parent, id = "", cargada = False):
        self.parent = parent
        self.id = id
        self.cargada = cargada

    
settings = ConfigParser()
settings.read("./config/settings.ini")

cargar = True
rutaLibreria = settings.get("General","libraryDir")

with open("./cache.json") as archivo:
    cache = json.load(archivo)

def DumpCache():
    with open("./cache.json", "w") as archivo:
        archivo.write(json.dumps(cache))

def RegistrarInstancia(a, b = "", c = False):
    caracteresMalos = "'}{"
    listaInstancias.append(Instancia(a, str(b).strip(caracteresMalos), c))

def CargarDirectorio():
    global listaDir
    listaDir = []
    try: listaDir = os.listdir(rutaLibreria)
    except: ConsoleLog("\033[31mNo se encontró la ruta, terminando programa\n\033[0m"); exit()
    else: listaDir.sort()

def OrdenarJuegos():
    listaJuegos.sort(key=lambda x: x.path)

def OrdenarInstancias():
    listaInstancias.sort(key=lambda x: x.parent.path)

def CargarInstancias():
    global listaInstancias
    global cache
    listaInstancias = []
    OrdenarJuegos()
    for i in listaDir:
        for n in listaJuegos:
            if i.startswith(n.path):
                if i == n.path:
                    try: cache[i]
                    except:
                        #ConsoleLog(f"Se encontró una instancia cargada de {n.display}, pero no se pudo identificar")
                        cache[i] = "[Sin nombre]"
                        DumpCache()
                        RegistrarInstancia(n, {cache[i]}, True)
                        n.instancias += 1
                    else:
                        #ConsoleLog(f"Se encontró una instancia cargada de {n.display} con la etiqueta {cache[i]}")
                        RegistrarInstancia(n, {cache[i]}, True)
                        n.instancias += 1
                    break
                elif i.startswith(f"{n.path} - "):
                    #ConsoleLog(f"Se encontró una instancia de {n.display} con la etiqueta {str.split(i, '- ')[1]}")
                    RegistrarInstancia(n, {str.split(i, '- ')[1]})
                    n.instancias += 1
                    break
    OrdenarInstancias()

def ReturnCode(code):
    if code == 1:
        ConsoleLog("\033[31mArgumento no válido\n\033[0m")
    if code == 2:
        ConsoleLog("\033[32m¡Hecho!\n\033[0m")
    if type(code) == str:
        ConsoleLog(f"\033[31m{code}\n\033[0m")


mode = 0
error = 0
seleccion = "-1"
highlight = "-1"

def Menu():

    global cargar
    global mode
    global error
    global seleccion
    global highlight
    exitMode = mode
    exitError = 1

    selectedInstance = listaInstancias[int(highlight)-1]
    ruta = f'{rutaLibreria}/{selectedInstance.parent.path}'
    rutaInstancia = f'{ruta} - {selectedInstance.id}'

    def DecodeAccessMethod(str):
        str = str.replace(r"%ruta%",ruta)
        str = str.replace(r"%appID%",selectedInstance.parent.appID)
        return str

    if mode == 0:
        ConsoleLog("[0]  Salir\n\n")
        ConsoleLog("Ingresá el número de instancia que querés seleccionar\n")

    if mode == 1:
        if selectedInstance.cargada:
            ConsoleLog("[1]  Iniciar  [2]  Descargar  [3]  Renombrar  [4]  Volver\n\n")
        else:
            ConsoleLog("[1]  -------  [2]  Cargar  [3]  Renombrar  [4]  Volver\n\n")
        ConsoleLog("¿Qué querés hacer?\n")

    if mode == 2:
        ConsoleLog("Ingresa el nuevo nombre para esta instancia\n")

    ReturnCode(error)


    try: seleccion = input()
    except: ConsoleLog("\033[36mPrograma terminado por el usuario!\n\033[0m"); exit()


    if mode == 0:
        if seleccion == "0":
            ConsoleLog("\033[36mPrograma terminado por el usuario!\033[0m\n")
            exit()
        for i in listaInstancias:
            if seleccion == str(listaInstancias.index(i)+1):
                exitMode = 1
                exitError = 0
                highlight = seleccion

    if mode == 1:

        if seleccion == "1":
            if selectedInstance.cargada:
                try: accessMethod = settings.get("AccessMethods", f"{selectedInstance.parent.path} - {selectedInstance.id}", raw=True)
                except: accessMethod = settings.get("AccessMethods", "Default", raw=True)
                accessMethod = DecodeAccessMethod(accessMethod)
                subprocess.Popen(f'cmd.exe /c {accessMethod}')
                exitMode = 0
                exitError = 2
                highlight = "-1"

        if seleccion == "2":
            halt = 0
            if selectedInstance.cargada:
                #Descargar
                os.rename(ruta, f'{ruta} - {cache[selectedInstance.parent.path]}')
                del cache[selectedInstance.parent.path]
                DumpCache()
                selectedInstance.cargada = False
                cargar = True
            else:
                #Cargar
                for i in listaInstancias:
                    if selectedInstance.parent == i.parent:
                        if i.cargada:
                            halt = 1
                            exitMode = 0
                            exitError = "No se pudo cargar. ¿Ya hay otra instancia cargada?"
                            highlight = "-1"
                            break
                if halt == 0:
                    os.rename(f'{rutaInstancia}', ruta)
                    cache[selectedInstance.parent.path] = selectedInstance.id
                    DumpCache()
                    selectedInstance.cargada = True
            if halt == 0:
                cargar = True
                exitMode = 0
                exitError = 2
                highlight = "-1"

        if seleccion == "3":
                exitMode = 2
                exitError = 0

        if seleccion == "4":
            exitMode = 0
            exitError = 0
            highlight = "-1"

    if mode == 2:
        halt = 0
        for i in listaInstancias:
            if selectedInstance.parent == i.parent:
                if seleccion == i.id:
                    halt = 1
                    exitMode = 0
                    exitError = "No se pudo cambiar el nombre"
                    highlight = "-1"
                    break
        if halt == 0:
            if selectedInstance.cargada:
                cache[selectedInstance.parent.path] = seleccion
                DumpCache()
            else:
                os.rename(f'{rutaInstancia}', f'{ruta} - {seleccion}')
            cargar = True
            exitMode = 0
            exitError = 2
            highlight = "-1"

    mode = exitMode
    error = exitError

    Main()


def Main():

    os.system("cls")
    ConsoleLog("\nBienvenid@!\n")
    ConsoleLog("---------------------------------------------------------------------------------------------\n")

    global cargar
    if cargar:
        CargarDirectorio()
        CargarInstancias()
        cargar = False

    totalInstancias = 0

    for i in listaJuegos:
        totalInstancias += i.instancias
        if i.instancias >= 1:
            ConsoleLog(f"Instancias de {i.display}\033[0m:\n")
            for x in listaInstancias:
                if x.parent == i:
                    if str(listaInstancias.index(x)+1) == highlight:
                        numerin = f"\033[30;47m[{listaInstancias.index(x)+1}]\033[0m"
                    else: numerin = f"[{listaInstancias.index(x)+1}]"
                    if x.cargada: stringCompuesto = f'{numerin}  {i.display} \033[0m- {x.id} \033[32m[Cargada]'
                    else: stringCompuesto = f'{numerin}  {i.display} \033[0m- {x.id}'
                    ConsoleLog(stringCompuesto)
                    continue
            ConsoleLog("\n")
    if totalInstancias <= 0:
        ConsoleLog(f"\033[31mNo se encontraron instancias\n")

    ConsoleLog("---------------------------------------------------------------------------------------------\n")

    Menu()


Main()