from flask import Flask, render_template, url_for, request
from marmiton_parser.data import filters

from bs4 import BeautifulSoup


app = Flask(__name__)

FILTRES_Liste = {filters.ingredientsblacklist:[], filters.tempsmax:None, 
filters.budget:None, filters.niveau:None, filters.ingredientswhitelist:[]}

FILTRES_Html = ""

txtToFiltresTranslator = {"level":filters.niveau, "budget":filters.budget, 
"time":filters.tempsmax, "ingredientblacklist":filters.ingredientsblacklist,
"ingredientwhitelist":filters.ingredientswhitelist}



@app.route('/', methods=['POST', 'GET'])
def index():
    global FILTRES_Html, FILTRES_Liste
    print(request)
    
    print(len(request.args))
    if len(request.args) > 0:
        if "deletefiltre" in request.args:
            #On enlève le dernier filtre
            fhtml = FILTRES_Html.split('<!--coucou-->')
            trucàsupprimer = fhtml[0]
            FILTRES_Html = ""
            for F in fhtml[1:]:
                FILTRES_Html += F

            soup = BeautifulSoup(trucàsupprimer, 'html.parser')
            delfiltre, delval = soup.find_all('div', class_="metadata")

            FILTRES_Liste_ValeursParDéfaut(delfiltre.text, delval.text)

            print(FILTRES_Liste)
            return render_template('index.html', liste_filtres=FILTRES_Html)

        #Valeurs du Form
        _filtre = request.args.get('filtre')
        print(_filtre)

        

        with open('templates/filtre-sample.html', 'r') as F:
            nfiltre = F.read()
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

        nfiltre += "<div class=\"metadata\" hidden>" + _filtre + "</div><div class=\"metadata\" hidden>" + _valeur + "</div>"
        nfiltre += "</p></li><!--coucou-->"
        FILTRES_Html = nfiltre + FILTRES_Html
        #print(FILTRES_Html)

        print(FILTRES_Liste)
        return render_template('index.html', liste_filtres=FILTRES_Html)
    
    else:
        print(FILTRES_Liste)
        return render_template('index.html', liste_filtres="<li>Pas de filtres</li>")


def FILTRES_Liste_ValeursParDéfaut(filtre, valeur):
    """Supprime la valeur de la clef correspondant au filtre donné"""
    global FILTRES_Liste

    if filtre in ['ingredientblacklist', 'ingredientwhitelist']:
        FILTRES_Liste[txtToFiltresTranslator[filtre]].remove(valeur)
        #ces filtres sont stockés sous forme de liste
    else:
        FILTRES_Liste[txtToFiltresTranslator[filtre]] = None




if __name__ == "__main__":
    app.run(debug=True)


#...Je tiens à m'excuser d'avance pour le lecteur intrépide qui
#   se serait mis en tête de vouloir déchiffrer ces hiéroglyphes. Tout
#   ce bazarre sera vite commenté, qu'il ne s'inquiète pas.