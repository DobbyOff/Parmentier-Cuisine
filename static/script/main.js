//Ce script sert à gérer ce qu'il se passe quand on change la sélection d'un filtre.

var inputTxt = document.getElementById('inputTxt');
var inputDiff = document.getElementById('filtrediffinput');
var inputBudget = document.getElementById('filtrebudgetinput');

repliques = {
    "ingredientwhitelist": {
        txt:"Ingrédient :",
        field:inputTxt
    },

    "ingredientblacklist": {
        txt:"Ingrédient :",
        field:inputTxt
    },

    "time": {
        txt:"Temps de préparation (ex: 2h15, 20 min...) :",
        field:inputTxt
    },

    "budget":{
        txt:"Budget :",
        field:inputBudget
    },

    "level":{
        txt:"Votre niveau (ne soyez pas si dûrs avec vous même :D ) :",
        field:inputDiff
    }
}


var filtreSelect = document.getElementById('filtre'),
    dispMiddle = document.getElementById('filtre-middle-txt');

var inputWrapper = document.getElementById('valuefield');

var updateDispMiddle = function (e) {
    hidefiltres();

    r = repliques[filtreSelect.value];
    dispMiddle.innerText = r.txt;

    displayer = r.field;

    displayer.style.visibility = "visible";
    inputWrapper.appendChild(displayer);
};

var hidefiltres = function (e) {
    inputBudget.style.visibility = 'hidden';
    inputDiff.style.visibility = 'hidden';
    inputTxt.style.visibility = 'hidden';
    inputTxt.innerText = "";
}
 
filtreSelect.addEventListener('change', updateDispMiddle);
hidefiltres();