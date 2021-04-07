from flask import Flask, render_template, url_for, request
from marmiton_parser.data import filters


app = Flask(__name__)

FILTRES_Liste = {filters.ingredientsblacklist:[], filters.tempsmax:None, 
filters.budget:None, filters.niveau:None, filters.ingredientswhitelist:[]}


@app.route('/', methods=['POST', 'GET'])
def index():
    print(request)
    
    print(len(request.args))
    if len(request.args) > 0:
        #Valeurs du Form
        _filtre = request.args.get('filtre')
        print(_filtre)
        
        if _filtre == "level":
            _valeur = request.agrs.get('filtrediffinput')
            FILTRES_Liste[filters.niveau] = _valeur
        elif _filtre == "budget":
            _valeur = request.args.get('filtrebudgetinput')
            FILTRES_Liste[filters.budget] = _valeur
        elif _filtre in ['time', 'ingredientblacklist', 'ingredientwhitelist']:
            _valeur = request.args.get('inputTxt')
            if _filtre == 'time':
                FILTRES_Liste[filters.tempsmax] = _valeur
            elif _filtre == 'ingredientblacklist':
                FILTRES_Liste[filters.ingredientsblacklist].append(_valeur)
            else:
                FILTRES_Liste[filters.ingredientswhitelist].append(_valeur)
        else:
            return "404 : arrête de faire joujou avec les url >:("
    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)