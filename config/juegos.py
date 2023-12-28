class Juego:
    def __init__(self, path = "", display = "", appID = "", instancias = 0):
        self.path = path
        self.display = display
        self.appID = appID
        self.instancias = instancias

listaJuegos = []
def Instantiate(a,b,c):
    listaJuegos.append(Juego(a,b,c))

#Instantiate(
#    "Directory Route",
#    "Game Name",
#    "appID"
#    )

Instantiate(
    "Grand Theft Auto 3",
    "\033[1mGrand Theft Auto \033[34mIII",
    "12100"
    )
Instantiate(
    "Grand Theft Auto Vice City",
    "\033[1mGrand Theft Auto: \033[35mVice City",
    "12110"
    )
Instantiate(
    "Grand Theft Auto San Andreas",
    "\033[1mGrand Theft Auto: \033[33mSan Andreas",
    "12120"
    )