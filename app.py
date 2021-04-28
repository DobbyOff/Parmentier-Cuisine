from flask import Flask, render_template, url_for, request, redirect
from marmiton_parser.data import filters
from marmiton_parser.marmitonparser import MarmitonParser

from bs4 import BeautifulSoup

#autant prévenir, ce programme est costaud

app = Flask(__name__)

#Ici, c'est le dico des filtres, il sera complété au fur et a mesure par les requêtes
FILTRES_Liste = {filters.ingredientsblacklist:[], filters.tempsmax:None, 
filters.budget:None, filters.niveau:None, filters.ingredientswhitelist:[]}

FILTRES_Html = "" #Le programme ajoute des éléments dynamiquement (les filtres).
#↑↑ c'est leur code html

txtToFiltresTranslator = {"level":filters.niveau, "budget":filters.budget, 
"time":filters.tempsmax, "ingredientblacklist":filters.ingredientsblacklist,
"ingredientwhitelist":filters.ingredientswhitelist}
#Vous vous rappelez peut-être que j'ai enregistré les filtres sous forme d'un enum. Il me fallait
#pouvoir convertir un filtre-txt en filtre-enum.
#J'aime bien utiliser les dico pour traduire comme ça, ça marche bien et ça évite de faire des grattes-ciel
#de if/elif/else

#Lorsque vous ajoutez un premier filtre, le bouton pour supprimer le dernier filtre s'affiche
boutonDelMontré = False
bouton_del_arg = ""
boutonDelHtml = "<form action='/delete_last_filtre' method='GET'><input type='submit' style='margin-left: 50px;' id='deletefiltrebutton' name='deletefiltre' value='Supprimer le dernier filtre'></form>"
#↑↑ le code html du bouton



@app.route('/', methods=['POST', 'GET'])
def index():
    global FILTRES_Html, FILTRES_Liste, boutonDelHtml, boutonDelMontré, bouton_del_arg
    print(request)
    FILTRES_Html = ""
    
    #deux cas de figure possibles :
    #il n'y a aucun argument dans la requête, on charge la page html index sans rien
    #ou alors il y a un ou plus arguments, ça veut dire qu'on ajoute des filtres
    #et donc ↓↓↓
    if len(request.args) > 0:
        #Valeurs du Form
        _filtre = request.args.get('filtre')
        print(_filtre)
        #_filtre, c'est le filtre sélectionné
        

        with open('templates/filtre-sample.html', 'r') as F:
            nfiltre = F.read() #le code html de l'élément qu'on va ajouter
            F.close()
            #j'ai créé un fichier html pour contient une base pour le code html d'un filtre 
        
        #tout ce bazar en bas regarde quel filtre a été sélectionné, et agit en conséquences.
        #l'html du filtre est composé de 2-3 mots introducteurs, et de la valeur du filtre
        if _filtre == "level":
            _valeur = request.args.get('filtrediffinput') #←le nom des args de la requete, allez voir index.html pour plus de clarté
            FILTRES_Liste[filters.niveau] = _valeur #on met à jour le gros dictionnaire avec tous les filtres
            nfiltre += "se cuisine avec un niveau " + _valeur #petit mot introducteur suivi de la valeur du filtre

        elif _filtre == "budget": #même idée
            _valeur = request.args.get('filtrebudgetinput')
            FILTRES_Liste[filters.budget] = _valeur
            nfiltre += "correspond à un budget " + _valeur
            
        elif _filtre in ['time', 'ingredientblacklist', 'ingredientwhitelist']:
            _valeur = request.args.get('inputTxt') #pour le temps, ingredientblacklist ou ingredientwhitelist, le champ d'entrée est le même
            if _filtre == 'time':
                FILTRES_Liste[filters.tempsmax] = _valeur
                nfiltre += "sera prête en " + _valeur

            elif _filtre == 'ingredientblacklist':
                FILTRES_Liste[filters.ingredientsblacklist].append(_valeur)
                nfiltre += "ne contient pas l'ingrédient " + _valeur

            else:
                FILTRES_Liste[filters.ingredientswhitelist].append(_valeur)
                nfiltre += "doit contenir l'ingrédient " + _valeur
        else:
            return "404 : arrête de faire joujou avec les url >:("
            #problème d'url

        nfiltre += "</p><div class=\"metadata\" hidden>" + _filtre + "</div><div class=\"metadata\" hidden>" + _valeur + "</div>"
        nfiltre += "</li><!--coucou-->"
        #ici on assemble l'html de l'élement filtre.
        #en plus du filtre en lui même, j'ajoute deux élements div cachés, qui contiennent en clair le nom du filtre et sa valeur,
        #on s'en sert pour les supprimer
        FILTRES_Html = nfiltre + FILTRES_Html
        #On ajoute l'élement nouvellement créé à tous les autres

        #si le bouton pour supprimer un filtre n'est pas montré, on l'affiche
        if not boutonDelMontré:
            bouton_del_arg = boutonDelHtml
            boutonDelMontré = True

        print(FILTRES_Liste)
        #Et on retourne enfin la page en belle forme
        return render_template('index.html', liste_filtres=FILTRES_Html, bouton_del=bouton_del_arg)
    
    else:
        print(FILTRES_Liste)
        return render_template('index.html', liste_filtres="<li>Pas de filtres</li>", bouton_del=bouton_del_arg)



#pour supprimer le dernier filtre
@app.route('/delete_last_filtre', methods=['POST', 'GET'])
def DeleteLastFiltre():
    global FILTRES_Html, FILTRES_Liste, bouton_del_arg, boutonDelMontré
    #On enlève le dernier filtre

    print("FILTRES_Html :", FILTRES_Html)
    if FILTRES_Html == "":
        #si jamais il n'y a pas encore de filtre, on retourne la page vierge
        return render_template('index.html', liste_filtres="<li>Pas de filtres</li>", bouton_del=bouton_del_arg)

    #le <!--coucou--> en commentaire sert en fait à séparer les différents filtres via split() !
    fhtml = FILTRES_Html.split('<!--coucou-->')
    trucàsupprimer = fhtml[0]
    FILTRES_Html = ""
    for F in fhtml[1:]:
        FILTRES_Html += F #on recréé l'html de tous les filtres, en oubliant le premier (celui qu'on supprime)

    #il faut aussi supprimer le filtre dans le dictionnaire.
    #Pour ça, les infos du filtre supprimé sont encodés subtilement dans le code
    #html du filtre, dans des div cachées de classe 'metadata'
    soup = BeautifulSoup(trucàsupprimer, 'html.parser')
    delfiltre, delval = soup.find_all('div', class_="metadata")

    FILTRES_Liste_ValeursParDéfaut(delfiltre.text, delval.text)

    if FILTRES_Html == "":
        bouton_del_arg = ""
        boutonDelMontré = False
        #si FILTRES_Html est vide, c'est qu'il n'y a plus de filtres, on cache alors le bouton pour les supprimer

    print(FILTRES_Liste)
    return render_template('index.html', liste_filtres=FILTRES_Html, bouton_del=bouton_del_arg)








def FILTRES_Liste_ValeursParDéfaut(filtre, valeur):
    """Supprime la valeur de la clef correspondant au filtre donné"""
    global FILTRES_Liste

    if filtre in ['ingredientblacklist', 'ingredientwhitelist']:
        FILTRES_Liste[txtToFiltresTranslator[filtre]].remove(valeur)
        #ces filtres sont stockés sous forme de liste
    else:
        FILTRES_Liste[txtToFiltresTranslator[filtre]] = None


M = MarmitonParser()


#La requête pour trouver une recette
@app.route('/find', methods=['POST'])
def TrouverRecette():
    """on approche du but"""
    global M

    print("On cherche une recette avec ces filtres :\n\t", FILTRES_Liste)

    #si le parser n'est pas initialisé, il faut l'initialiser.
    #Si il est déjà initialisé, ça veut dire que la requête a déjà été appelée dans l'exécution du programme
    #en clair, c'est quand on veut une autre recette que celle affichée
    if not M.isInit:
        M.InitRecherche(FILTRES_Liste)

    #on laisse faire l'algo, il se débrouille comme un chef
    recette = M.TrouverRecette()

    #maintenant il faut afficher les résultats !
    #On récupère les infos qu'on va afficher à l'utilisateur, on les fait rentrer dans une string
    titre = recette._title
    data = f"{recette._preparationdata['budget']}, {recette._preparationdata['level']}, {recette._preparationdata['time']} de préparation"
    url = recette._url
    imageurl = recette._thumbnailurl

    #voir index.html pour plus de clarté
    return render_template('index.html', 
    liste_filtres=FILTRES_Html, bouton_del=bouton_del_arg, 
    show_result="oui", _nom_recette=titre, _data_recette=data, _image_recette=imageurl, _recette_url = url)




if __name__ == "__main__":
    app.run(debug=True)


# TODO :
#  - faire en sorte que le prg oublie les filtres après avoir trouvé une recette