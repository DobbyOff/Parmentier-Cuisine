# Parmentier
 Your future favorite cooking dude !

/!\ vous trouverez la documentation dans DOC.md.
/!\ Flask tourne, vous trouverez le programme dans la branche 'flask-ing', lancez le fichier app.py

## architecture :
Le programme va se diviser en 3 dossiers :
    ./marmiton_parser/ pour l'exploration du site de marmiton et le tri des recettes
    ./web_host/ pour l'interface utilisateur avec Flask
    ./SQL/ pour la gestion des comptes et des données utilisateurs

###     marmiton_parser
        Cette partie se charge de disséquer des pages web du site de Marmiton pour en extraire des recettes et leurs informations.

        MarmitonParser.py : 
            contient la classe MarmitonParser qui retourne l'url des 100 recettes les mieux notées de marmiton
            
            contient la fonction IsRecette qui prend une soup représentant le contenu d'une balise <div> (voir doc)  en paramètre et détermine si il s'agit d'une recette.

        parsers.py :
            contient la classe PlatParser, fille de MarmitonParser. Elle fait exactement comme sa classe mère, mais se concentre sur différentes pages web selon le paramètre donné au constructeur, en triant selon les plats (voir data.py).

        data.py :
            contient l'enum (voir doc) plat qui classe les différents types de plats, et un dictionnaire qui mets tous ces plats en relation avec des URLs du site de Marmiton

        recipe.py :
            contient la classe Recipe, qui prend une url en constructeur (une page recette de marmiton) et qui en extrait toutes les informations utiles.

###    
    Fonctionnement :
        A chaque fois qu'on voudra aller chercher une recette :
        - on choisi des filtres, le programme en déduit quelle rubrique marmiton il faut aller voir selon les plats désiré
        - le programme va chercher l'html de la webpage en question et la dissèque. Il en trouve plein de recettes.
        - Le programme choisi une URL de recette au hasard, l'utilise pour instancier un objet de la classe Recipe
        - selon les infos dans Recipe, le programme vérifie si elle correspond aux filtres
        - et on trouve une recette !


###     web_host :
        TODO
        /!\ du fait de l'architecture d'un projet Flask, certains fichiers doivent se trouver directement dans l'arborescence du projet, d'autres dans \templates, etc... Avoir un dossier web_host ne fait donc plus beaucoup de sens.
        
        /!\ Pour actualiser la page, toujours bien faire Ctrl + Shift + R, sinon le navigateur conserve la feuille de style css en cache et elle n'est pas actualisée si on a fait des changemens dessus !


###     SQL :
        TODO

