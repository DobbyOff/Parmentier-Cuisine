import requests as RQ
from bs4 import BeautifulSoup

class Recipe:
    _url = ""
    _metadata = {} #étoiles, likes
    _preparationdata = {} #temps de prep, budget, difficulté
    _regimes = [] #ne marche pas, je crois que Marmiton ont retiré cette info des pages
    _thumbnailurl = "" #Adresse URL de l'image de la recette 
    _ingredients = {} #dictionnaire avec tous les ingrédients
    _title = "" #...le titre de la recette

    def __init__(self, url):
        self._url = url

        htmlcontent = RQ.get(self._url).content #va chercher l'html de la page recette
        self.soup = BeautifulSoup(htmlcontent, "html.parser")

        self.__ExtractData()
        self._ingredients = self.__GetIngredients()
        #ces deux méthodes remplissent les champs çi-dessus

        print(self._title, "instanciation terminée !")


    def __ExtractData(self): #TODO : make this async
        """lis l'html de la page et s'en sert pour remplir tous les champs de la classe"""

            #thumbnailurl : l'url de la photo de la recette
        tbnls = self.soup.find_all('img', id="recipe-media-viewer-thumbnail-0")
        try:
            self._thumbnailurl = tbnls[0]['data-src']
        except IndexError:
            #Il se peut qu'il n'y ait qu'une image, que marmiton place à la place de la vidéo de préparation. 
            #Je vais donc chercher la photo de la recette à un autre endroit dans ces cas là, 
            #quand il n'y a rien dans la liste des images possibles (la liste tbnls).
            try: 
                tbnls = self.soup.find_all('img', id="recipe-media-viewer-main-picture")
                self._thumbnailurl = tbnls[0]['data-src']
            except IndexError: #Des fois y'a vraiment pas d'images. Je mets une icone à la place, suivez le liens
                self._thumbnailurl = "https://cdn2.iconfinder.com/data/icons/warning-solid-icons-2/48/78-512.png"
                
        #metadata : le nombre de likes, le score utilisateur
        score = self.soup.find('span', class_="recipe-header__rating-text")
        self._metadata['score'] = score.string

        nlikes = self.soup.find_all('span', class_="recipe-infos-users__value")
        for value in nlikes:
            #Il y a plein de span qui ont comme classe 'recipe-info-users__value', il faut choisir celle qui a comme
            #parent un truc de la classe 'recipe-info-users__notebook'
            if value.parent['class'] == ["recipe-infos-users__notebook"]:
                self._metadata['likes'] = value.string #marmiton ont mis à jour leur site et ne font plus apparaître le 
                                                        #nombre de likes, donc je devrais enlever ce bout de code.

        #preparationdata : le temps, le budget et la difficulté de la préparation
        metadata = self.soup.find_all('div', class_="recipe-primary__item")
        #ces infos sont toutes rangées dans une div, qu'on trouve ↑ ici ↑
        #Puis on se ballade dans le contenu de la div et on trouve ce qu'on veux.
        time = metadata[0].contents[3]
        self._preparationdata['time'] = time.string

        cost = metadata[2].contents[3]
        self._preparationdata['budget'] = cost.string

        level = metadata[1].contents[3]
        self._preparationdata['level'] = level.string #c'est la difficulité ici

        #title : le nom de la recette
        self._title = self.soup.find('h1', class_="main-title show-more").string


    def __GetIngredients(self):
        """lis l'html et en retourne un dictionnaire avec les ingrédients.
        Similaire à __ExtractData, séparé pour des questions de lisibilité."""

        ingrlist = self.soup.find('div', class_="ingredient-list__ingredient-group").find('ul', class_="item-list").find_all('li')
        #c'est long, c'est imcompréhensible, mais ça marche
        Ingredients = {}

        for ingr in ingrlist:
            if ingr == '\n':
                continue

            ingrType = ingr.find('div', class_='ingredient-data')['data-singular']
            ingrQuantite = ( ingr.find('div', class_='unit-data')['data-plural'], 
            ingr.find('div', class_='quantity-data')['data-base-qt'] )
            Ingredients[ingrType] = ingrQuantite

        return Ingredients

    
    def Contains(self, ingr):
        """retourne True si l'ingrédient passé en commentaire (str) est contenu dans la recette"""
        print("recipe :", ingr)
        for e in self._ingredients:
            if ingr.capitalize() in e.capitalize():
                return True


#        Petit aperçu de l'intérieur d'une instance de Recipe après exécution du constructeur :
#        (obtenu empiriquement)


# _ingredients = {'coulis de tomate': ('petits pots', '1'), 
#                 'fromage de chèvre': ('', '1'), 
#                 'gruyère râpé': ('sachets', '1'), 
#                 'mozzarella': ('petits sachets', '1'), 
#                 'poivre': ('', ''), 'pâte à pizza': ('', '1'), 
#                 'roquefort': ('', '1'), 
#                 'sel': ('', '')}
#
# _metadata = {'score': '4.5/5'}
#
# _preparationdata = {'budget': 'bon marché', 'level': 'très facile', 'time': '40 min'}
#
# _regimes = []
#
# _thumbnailurl = 'https://assets.afcdn.com/recipe/20160926/5624_w157h157c1.jpg'
#
# _title = 'Pizza aux 3 fromages'
#
# _url = 'https://www.marmiton.org/recettes/recette_pizza-aux-3-fromages_31450.aspx'
#