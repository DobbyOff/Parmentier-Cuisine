from enum import Enum

class plat(Enum):
    """classe les différents types de plats"""
    apero = 0
    entree = 1
    plat = 2
    dessert = 3
    boisson = 4

#En clef : un plat, en donnée : l'url du site
PLAT_URL = {plat.plat: "https://www.marmiton.org/recettes/index/categorie/plat-principal?rcp=0",
            plat.apero:"https://www.marmiton.org/recettes/index/categorie/aperitif-ou-buffet?rcp=0",
            plat.entree:"https://www.marmiton.org/recettes/index/categorie/entree?rcp=0",
            plat.dessert:"https://www.marmiton.org/recettes/index/categorie/dessert?rcp=0",
            plat.boisson:"https://www.marmiton.org/recettes/?type=boisson"}


class filters(Enum):
    """Permet de filtrer les recettes"""
    ingredientsblacklist=0
    tempsmax=1
    regime=2
    budget=3
    niveau=4
    ingredientswhitelist=5
 

def ConvertPrepTimeToInt(a):
    preptime = a.replace(' ', '')
    if preptime.endswith("min"):
        preptime = preptime[:-3]

    minutes = 0
    if len(preptime.split('h')) > 1:
        minutes = int(preptime.split('h')[0])*60

        if len(preptime.split('h')[1]) > 0:
            minutes += int(preptime.split('h')[1])
    else:
        minutes = int(preptime)

    return int(minutes)

PREPINFO_TRANSLATOR = {"très facile":1, "facile":2, "moyenne":3, "moyen":1, "bon marché":0}