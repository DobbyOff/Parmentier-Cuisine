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
 
 #pour éviter les erreur, j'ai classé tous les filtres dans un type énuméré (enum, voir doc)


def ConvertPrepTimeToInt(a):
    if a is None:
        return 10**6 #on souhaite avoir le plus petit quand on compare les budgets
        #alors si on a pas mis de budget, il est le plus grand possible, on a pas mis de limite 
        #donc il faut qu'il soit plus grand que n'importe quoi qu'on compare.

    #la suite, c'est du traitement string pour enlever les espaces et les virgules
    preptime = a.replace(' ', '')
    if preptime.endswith("min"):
        preptime = preptime[:-3]

    #on récupère le nombre de minutes, d'heures, etc, on multiplie, on additionne et le tour est joué
    minutes = 0
    if len(preptime.split('h')) > 1:
        minutes = int(preptime.split('h')[0])*60

        if len(preptime.split('h')[1]) > 0:
            minutes += int(preptime.split('h')[1])
    else:
        minutes = int(preptime)

    return int(minutes)


PREPINFO_TRANSLATOR = {"tres_facile":1, "très facile":1, "facile":2, "moyenne":3, "moyen":1, "bon_marche":0, "bon marché":0}
#vous pouvez voir qu'on traduit les chaines de caractère qui correspondent aux budgets et aux difficultés
#en nombres.
#J'ai mis la difficulté et le budget ensemble, ça ne pose pas problème puisqu'on ne compare jamais des budgets à des difficultés