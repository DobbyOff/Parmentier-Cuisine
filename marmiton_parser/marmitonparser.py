import requests as RQ
from bs4 import BeautifulSoup
from random import randint

from marmiton_parser.data import ConvertPrepTimeToInt, filters, PREPINFO_TRANSLATOR
from marmiton_parser.recipe import Recipe

class MarmitonParser:
    """Classe mère des parsers, elle analyse les 100 recettes les mieux notées"""
    _URL = "https://www.marmiton.org/recettes/top-internautes.aspx"
    _recipeListUrl = [] #c'est ici que vont aller les URLs des recettes trouvées, pour ne pas avoir à aller les chercher
                        #tout le temps.
    isInit = False
    #L'idée : Vous demandez à initialiser la recherche avec InitRecherche(filtre)
    #Ensuite, vous appelez TrouverRecette pour trouver une recette qui correspond au filtre

    def __init__(self):
        htmlcontent = RQ.get(self._URL).content
        self.soup = BeautifulSoup(htmlcontent, "html.parser")
        self._recipeListUrl = self.__ParseHTML()
        #__ParseHTML() cherche dans la page d'accueil de Marmiton les 100 premières recettes


    def InitRecherche(self, filterDico):
        """exemple d'argument filterDico : \n\t{filters.ingredientsblacklist:['pates'], filters.tempsmax:"30 min", 
        filters.regime:[], filters.budget:"bon marché", filters.niveau:None, filters.ingredientswhitelist:[]}"""
        self.isInit = True
        self.filterDico = filterDico
        self.searchlist = self._recipeListUrl[:] #on met toutes les url de recettes là dedans et on les enlève au fur et ç mesure
        #Je fais ça en deux fonction pour qu'on puisse demander plusieurs résultats : si la recette
        #qui sort ne vous plait pas, vous pouvez rappeler TrouverRecette sans remettre le filtre et sans
        #possibilité d'avoir deux fois la même recette


    def TrouverRecette(self):
        while len(self.searchlist) > 0:
            url = self.searchlist.pop(randint(0, len(self.searchlist)-1))
            #On choisit une url au pif dans searchlist, et on la transforme en objet Recipe
            R = Recipe(url)
            recettebonne = True
            
            #FILTRAGE
            #ici, c'est pour les ingredients qu'on veut pas
            print('argument passé au marmitonparser :', self.filterDico[filters.ingredientsblacklist])
            for ingr in self.filterDico[filters.ingredientsblacklist]:
                if R.Contains(ingr):
                    print("R contient l'ingrédient")
                    recettebonne = False
            
            #et ici, les ingrédients qu'on veut absolument
            for ingr in self.filterDico[filters.ingredientswhitelist]:
                if not R.Contains(ingr):
                    recettebonne = False
            
            if not recettebonne:
                continue #l'instruction continue oublie tout ce qui est après et refait un tour de boucle
            #Donc autrement dit, on arrête tout, on reprend une nouvelle recette et on voit si elle passe
            #On continue jusqu'à ce qu'on en trouve une sympa
            
            #le temps de préparation
            if R._preparationdata['time'] != None:
                if  ConvertPrepTimeToInt(R._preparationdata['time']) > ConvertPrepTimeToInt(self.filterDico[filters.tempsmax]):
                    continue
                #J'ai fais une fonction qui convertit 1h, 40 min, 1h30 etc... en nombre de minutes poour
                #pouvoir convertir les temps de préparation efficacement.
                #Elle est dans marmiton_parser/data.py


            #votre talent de cuistot
            _fniveau = self.filterDico[filters.niveau]
            if not _fniveau == None:
                _rniveau = R._preparationdata['level']
                _rniveaucomparable = PREPINFO_TRANSLATOR[_rniveau]
                _fniveaucomparable = PREPINFO_TRANSLATOR[_fniveau]
                #selon l'endroit du programme où on est, le niveau et le budget peut être un nombre, 
                #une chaine de caractère ou une instance d'un enum. J'ai fais une fonction pour les 
                #uniformiser et pouvoir les comparer → marmiton_parser/data.py

                if _rniveaucomparable > _fniveaucomparable:
                    print("niveau trop élevé, passée")
                    continue

            #enfin, le budget
            _fbudget = self.filterDico[filters.budget]
            if not _fbudget == None:
                _rbudget = R._preparationdata['budget']
                _rbudgetcomparable = PREPINFO_TRANSLATOR[_rbudget]
                _fbudgetcomparable = PREPINFO_TRANSLATOR[_fbudget]
                #même idée, on convertit et on compare

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
    """retourne true si le contenu encapsulé dans la div passée en para ressemble à une recette"""
    try:
        classe = div['class']
    except KeyError: #Le tag n'a pas de class, ce n'est pas une recette
        return False

    if 'recipe-card' in classe:
        #Toutes les divs de recette sont de la forme <div []...] class="[...]recipe-card[...]"> [...] <div/>
        return True
    else:
        return False

        