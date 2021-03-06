DOCUMENTATION

# Bibliothèques requises :
flask
flask-sqlalchemy
bs4
requests
enum


# BeautifulSoup (BS)
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

BS est capable de transformer un texte html en un objet appelé Soup, qui permet de le parcourir rapidement. 
Je récupère les codes html des pages avec le module requests, comme ceci :

html = requests.get(url).content

##      BeautifulSoup(html, 'html.parser')
    Instancie un objet Soup avec un code html. Une soup correspond à au contenu d'une balise. Avec cette instanciation, c'est le contenu du <html> ... <html/> qui est encapsulé. Un objet Soup peut très bien correspondre simplement à l'intérieur d'une <div>, etc...

##      Soup.find_all(...)
    Trouve toutes les occurences selon les filtres.
    Exemples :
        Soup.find_all('div')
        retourne toutes les Soup qui correspondent à une balise <div>

        Soup.find_all('span', class_="recipe", id="header")
        retourne toutes les Soup qui correspondent à une balise <span>, dont la classe est "recipe" et l'id "header". On écrit _class car class est déjà un mot clef réservé en pyhon :/

##      Soup.find()
    Comme Soup.find_all, mais au lieu de retourner une liste, retourne la première occurence.

##      Soup['attribut']
    Retourne l'attribut de l'objet soup.
    Exemple :
        soup['class'] retournera "recipe" si soup est un objet Soup instancié avec ce code html :
        <span class="recipe" id="header">...<span/>

##      Soup.parent
    Retourne la Soup qui correspond à l'élement parent de celui représenté par l'instance dans l'arborescence html.

##      Soup.contents
    Retourne tous les enfants de l'élement représenté par l'instance dans l'arborescence html. Attention, les sauts de ligne (\n) sont aussi comptés dans les enfants.


# ENUM
Un enum est type de variable customisé qui peut prendre un certain nombre de voiture. C'est pas très utilisé en python, mais partout si.
exemple :

from enum import Enum

class véhicule(Enum):
    moto = 1
    voiture = 2
    avion = 3
    bicyclette = 4

montypedevéhicule = véhicule.moto

C'est très utile pour classifier des types ou tout ce qui doit tenir dans un panel de valeurs prédéfini.

On pourrait utiliser juste une string :
montypedevéhicule = "moto"
Mais, si vous faites une faute de frappe par exemple, alors votre programme va bugger. Si vous faites une faute de frappe avec un enum, le programme va faire un erreur.
Je trouve les enum plus simples à utiliser et bien pratiques pour avoir un programme un minimum rangé