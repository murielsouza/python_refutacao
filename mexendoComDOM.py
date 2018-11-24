from xml.dom.minidom import parse
import xml.dom.minidom

def escrevendoCondicional(no): #Colocando o condicional em listas
    if no.hasChildNodes():
        print("a")
        for filho in no.childNodes:
            escrevendoCondicional(filho)
    else:
        print(no.nodeValue)
        return no.nodeValue;
    #escrevendoCondicional(no.nextSibling)
    
    
DOMTree = xml.dom.minidom.parse("formula.xml")
formula = DOMTree.documentElement
premissas = formula.getElementsByTagName("PREMISSA")

cont  = 0;
for premissa in premissas:
    print(premissa.firstChild)
    for filhoDePremissa in premissa.childNodes:
        print("B")
        if filhoDePremissa.nodeName == "CONDICIONAL":
            escrevendoCondicional(filhoDePremissa)
    cont+=1
        
        
