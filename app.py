from flask import Flask, render_template, url_for, request, redirect
from marmiton_parser.data import filters
from marmiton_parser.marmitonparser import MarmitonParser

from bs4 import BeautifulSoup


app = Flask(__name__)

FILTRES_Liste = {filters.ingredientsblacklist:[], filters.tempsmax:None, 
filters.budget:None, filters.niveau:None, filters.ingredientswhitelist:[]}

FILTRES_Html = "" #Le programme ajoute des éléments dynamiquement (les filtres).
#↑↑ c'est leur code html

txtToFiltresTranslator = {"level":filters.niveau, "budget":filters.budget, 
"time":filters.tempsmax, "ingredientblacklist":filters.ingredientsblacklist,
"ingredientwhitelist":filters.ingredientswhitelist}


boutonDelMontré = False
bouton_del_arg = ""
boutonDelHtml = "<form action='/delete_last_filtre' method='GET'><input type='submit' style='margin-left: 50px;' id='deletefiltrebutton' name='deletefiltre' value='Supprimer le dernier filtre'></form>"


@app.route('/', methods=['POST', 'GET'])
def index():
    global FILTRES_Html, FILTRES_Liste, boutonDelHtml, boutonDelMontré, bouton_del_arg
    print(request)
    
    if len(request.args) > 0:
        #Valeurs du Form
        _filtre = request.args.get('filtre')
        print(_filtre)
        

        with open('templates/filtre-sample.html', 'r') as F:
            nfiltre = F.read() #le code html de l'élément qu'on va ajouter
            F.close()
        
        if _filtre == "level":
            _valeur = request.args.get('filtrediffinput')
            FILTRES_Liste[filters.niveau] = _valeur
            nfiltre += "se cuisine avec un niveau " + _valeur

        elif _filtre == "budget":
            _valeur = request.args.get('filtrebudgetinput')
            FILTRES_Liste[filters.budget] = _valeur
            nfiltre += "correspond à un budget " + _valeur
            
        elif _filtre in ['time', 'ingredientblacklist', 'ingredientwhitelist']:
            _valeur = request.args.get('inputTxt')
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

        nfiltre += "</p><div class=\"metadata\" hidden>" + _filtre + "</div><div class=\"metadata\" hidden>" + _valeur + "</div>"
        nfiltre += "</li><!--coucou-->"
        FILTRES_Html = nfiltre + FILTRES_Html

        if not boutonDelMontré:
            bouton_del_arg = boutonDelHtml
            boutonDelMontré = True

        print(FILTRES_Liste)
        return render_template('index.html', liste_filtres=FILTRES_Html, bouton_del=bouton_del_arg)
    
    else:
        print(FILTRES_Liste)
        return render_template('index.html', liste_filtres="<li>Pas de filtres</li>", bouton_del=bouton_del_arg)




@app.route('/delete_last_filtre', methods=['POST', 'GET'])
def DeleteLastFiltre():
    global FILTRES_Html, FILTRES_Liste, bouton_del_arg, boutonDelMontré
    #On enlève le dernier filtre

    print("FILTRES_Html :", FILTRES_Html)
    if FILTRES_Html == "":
        return render_template('index.html', liste_filtres="<li>Pas de filtres</li>", bouton_del=bouton_del_arg)

    fhtml = FILTRES_Html.split('<!--coucou-->')
    trucàsupprimer = fhtml[0]
    FILTRES_Html = ""
    for F in fhtml[1:]:
        FILTRES_Html += F

    #il faut aussi supprimer le filtre dans le dictionnaire.
    #Pour ça, les infos du filtre supprimé sont encodés subtilement dans le code
    #html du filtre, dans des div cachées de classe 'metadata'
    soup = BeautifulSoup(trucàsupprimer, 'html.parser')
    delfiltre, delval = soup.find_all('div', class_="metadata")

    FILTRES_Liste_ValeursParDéfaut(delfiltre.text, delval.text)

    if FILTRES_Html == "":
        bouton_del_arg = ""
        boutonDelMontré = False

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



@app.route('/find', methods=['POST'])
def TrouverRecette():
    """on approche du but"""
    print("On cherche une recette avec ces filtres :\n\t", FILTRES_Liste)

    M = MarmitonParser()
    recette = M.TrouverRecette(FILTRES_Liste)
    print(recette._ingredients)

    return redirect(recette._url)
    #return render_template('index.html', liste_filtres=FILTRES_Html, bouton_del=bouton_del_arg)




if __name__ == "__main__":
    app.run(debug=True)


# TODO :
#  - afficher la page marmiton sur la page
#  - faire en sorte que le prg oublie les filtres après avoir trouvé une recette



#...Je tiens à m'excuser d'avance pour le lecteur intrépide qui
#   se serait mis en tête de vouloir déchiffrer ces hiéroglyphes. Tout
#   ce bazarre sera vite commenté, qu'il ne s'inquiète pas.