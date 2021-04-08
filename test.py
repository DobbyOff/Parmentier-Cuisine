from marmiton_parser import marmitonparser, recipe, parsers, data
from bs4 import BeautifulSoup

from marmiton_parser.data import filters, ConvertPrepTimeToInt

M = marmitonparser.MarmitonParser()
#print(M._recipeListUrl)
i = 0
for url in M._recipeListUrl:
    i += 1
    print(i)
    R = recipe.Recipe(url)
   
    level = R._preparationdata['level'] 
    with open("data/levels.txt", 'r', encoding='utf8') as F:
        truc = F.read()
        if not level in truc:
            F2 = open("data/levels.txt", 'a', encoding='utf8')
            F2.write(level + '\n')
            F2.close()
        F.close()
    

# F = {filters.ingredientsblacklist:['pates'], filters.tempsmax:"30 min", filters.regime:[], filters.budget:"bon marché", filters.niveau:None, filters.ingredientswhitelist:[]}
# M = marmitonparser.MarmitonParser()
# recette = M.TrouverRecette(F)

# print(recette)