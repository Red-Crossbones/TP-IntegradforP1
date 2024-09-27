import re

#Expresion regulares

lexemas = {
    'nomVariables': r
}

#Codigo para que verifique si es un nombre de variable. Los nombres deberian cambiar en la implementacion final
def es_nom_variable(t):
    ret = false

    if len(t)<=10 and not t[0].islower():
        ret = es_nom_valido(t[1:])
    return ret


def es_nom_valido(t):
    ret = true
    for caracter in t:
        if (not caracter.islower()) and (not caracter.isNumeric()):
            ret = false
            break
    return ret