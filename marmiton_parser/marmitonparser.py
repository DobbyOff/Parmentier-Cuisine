import requests as RQ
from bs4 import BeautifulSoup
from random import randint

from marmiton_parser.data import ConvertPrepTimeToInt, filters, PREPINFO_TRANSLATOR
from marmiton_parser.recipe import Recipe

class MarmitonParser:
    """base-class for the MarmitonParsers. Filters by top ranked."""
    _URL = "https://www.marmiton.org/recettes/top-internautes.aspx"
    _recipeListUrl = [] #c'est ici que vont aller les URLs des recettes trouvées, pour ne pas avoir à aller les chercher
                        #tout le temps.
    

    def __init__(self):
        htmlcontent = RQ.get(self._URL).content
        self.soup = BeautifulSoup(htmlcontent, "html.parser")
        self._recipeListUrl = self.__ParseHTML()


    def TrouverRecette(self, filterDico):
        """exemple d'argument filterDico : \n\t{filters.ingredientsblacklist:['pates'], filters.tempsmax:"30 min", 
        filters.regime:[], filters.budget:"bon marché", filters.niveau:None, filters.ingredientswhitelist:[]}"""
        recipes = self._recipeListUrl[:]

        while len(recipes) > 0:
            print("du coup oui")
            url = recipes.pop(randint(0, len(recipes)-1)) 
            R = Recipe(url)
            recettebonne = True
            
            print('argument passé au marmitonparser :', filterDico[filters.ingredientsblacklist])
            for ingr in filterDico[filters.ingredientsblacklist]:
                if R.Contains(ingr):
                    print("R contient l'ingrédient")
                    recettebonne = False
            print('du coup non')
            
            for ingr in filterDico[filters.ingredientswhitelist]:
                if not R.Contains(ingr):
                    recettebonne = False
                    continue
            
            if not recettebonne:
                continue
            
            if R._preparationdata['time'] != None:
                if  ConvertPrepTimeToInt(R._preparationdata['time']) > ConvertPrepTimeToInt(filterDico[filters.tempsmax]):
                    continue

            # for regimes in filterDico[filters.regime]:
            #     if not regime in R._regimes:
            #         continue

            _fniveau = filterDico[filters.niveau]
            if not _fniveau == None:
                _rniveau = R._preparationdata['level']
                _rniveaucomparable = PREPINFO_TRANSLATOR[_rniveau]
                _fniveaucomparable = PREPINFO_TRANSLATOR[_fniveau]
                # print("filtre", _fniveau, _fniveaucomparable, "\trecette", _rniveau, _rniveaucomparable)
                if _rniveaucomparable > _fniveaucomparable:
                    print("non, passée")
                    continue

            _fbudget = filterDico[filters.budget]
            if not _fbudget == None:
                _rbudget = R._preparationdata['budget']
                _rbudgetcomparable = PREPINFO_TRANSLATOR[_rbudget]
                _fbudgetcomparable = PREPINFO_TRANSLATOR[_fbudget]
                if _rbudgetcomparable > _fbudgetcomparable:
                    continue

            return R
            




    def __ParseHTML(self): #TODO: changer le nom de ce truc
        """analyse le code HTML pour y trouver toutes les recettes"""
        print("\t\tparsing \'", self.soup.title.string, "\'")
        Divs = self.soup.find_all('div')
        PropperRecipe = []

        for div in Divs:
            #Pour chaque div, on regarde si elle correspond à une recette. 
            #Si oui, on va chercher l'url de cette recette et on l'enregistre.
            if IsRecette(div):
                recipe_url = div.find('a')['href']
                PropperRecipe.append(recipe_url) 

        if len(PropperRecipe) == 0:
            raise Exception("[Erreur] : aucune recette trouvée dans", self._URL)

        print("\t\t", len(PropperRecipe), "recettes trouvées !")  
        #Il en trouve 100 pour les mieux classées, 30 quand on trie selon les plats
        #Ces nombres correspondent aux nombre de recette sur les premières pages des différentes catégories sur le site, allez voir !
        return PropperRecipe
        


def IsRecette(div):
    """returns true if the content encapsulated in <div>...<div/> looks like a proper recipe"""
    try:
        classe = div['class']
    except KeyError: #Le tag n'a pas de class, ce n'est pas une recette
        return False

    if 'recipe-card' in classe:
        #Toutes les divs de recette sont de la forme <div []...] class="[...]recipe-card[...]"> [...] <div/>
        return True
    else:
        return False

        