from marmiton_parser import marmitonparser, data

class PlatParser(marmitonparser.MarmitonParser): #TODO : mixer ça avec MarmitonParser, vu qu'il y a juste l'url qui change.
    _URL = ""

    def __init__(self, type_de_plat):
        """filter : parser.plat enum"""
        self._URL = data.PLAT_URL[type_de_plat]

        marmitonparser.MarmitonParser.__init__(self)
        #En fait, le processus est exactement le même que quand on regarde les recettes les mieux notées dans 
        #MarmitonParser.py, rien besoin de changer dans les algos, juste l'url.

        #C:\Users\damie\Documents\Lycée\NSI\Parmentier\Parmentier