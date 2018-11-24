from xml.dom.minidom import parse
import xml.dom.minidom


class Tree:

    def __init__(self):
        self.raiz = None
        global listaBifurca, listaNotBifurca

    def insere(self, valor):
        if self.raiz == None:
            self.raiz = No(valor)
        else:
            self.raiz.insere(valor)

    def preOrdem(self):
        if self.raiz != None:
            self.raiz.preOrdem()

    def fragmentarOrNot(self):
        if self.raiz !=None:
            self.raiz.fragmentarOrNot()

    def nósFolhas(self):
        if self.raiz !=None:
            self.raiz.nosFolhas()

    def enfileirando(self):
        return "OI"

class No:

    def __init__(self, valor):

        if(valor.nodeName != 'LPRED'):
            self.info = valor
            self.notProcessed = True;
            self.esq = None
            self.dir = None
        else:
            self.info = valor
            self.notProcessed = False;
            self.esq = None
            self.dir = None

    def insere(self, valor): #mudar nome da função para insereEsquerda() ---> quando não bifurca ou vc quer inserir do lado esquerdo da bifuracação
        if self.esq == None:
            self.esq = No(valor)
        else:
            self.esq.insere(valor)

    def insereDireita(self, valor): #para Bifurcação
        if self.dir == None:
            self.dir = No(valor)

    def preOrdem(self):
        print(self.info.nodeName, end=" ")
        if self.esq != None:
            self.esq.preOrdem()
        if self.dir != None:
            self.dir.preOrdem()

    def fragmentarOrNot(self): #Até dia 12 montar essa estrutura
        global listaBifurca
        global listaNotBifurca
        if(self.notProcessed):
            if(self.info.nodeName == "CONDICIONAL"): #futuramente adicionar validação de negado ou não
                self.info.firstChild.setAttribute('NEG', '~') #negando antecedente
                listaBifurca.append(self.info)
                #self.notProcessed = (self.nósFolhas(self.info, True)); #True se a funcao bifurca, False se não
            if(self.info.nodeName == "ANTECEDENTE"):
                if(self.info.nodeName == "LPRED"):
                    listaNotBifurca.append(self.info)
                   #self.notProcessed = (self.nósFolhas(self.info, False));
                elif(self.info.nodeName in ["CONJUNCAO"]):
                    listaNotBifurca.append(self.info)
                    #self.notProcessed = (self.nósFolhas(self.info, False));
                else:
                    listaBifurca.append(self.info)
                    #self.notProcessed = (self.nósFolhas(self.info, True));
            if (self.info.nodeName == "CONSEQUENTE"):  # VALIDAR INSERCAO DE LETRA PREDICATIVA
                if (self.info.nodeName == "LPRED"):
                    self.notProcessed = (
                        self.nósFolhas(self.info, False));  # INSERIR ESTRUTURA DE IF-ELSE PARA BIFURCACAO
                elif (self.info.nodeName in ["CONJUNCAO"]):
                    self.notProcessed = (self.nósFolhas(self.info, False));
                else:
                    self.notProcessed = (self.nósFolhas(self.info, True));
        if (self.esq != None):
            self.esq.fragmentarOrNot()
        if(self.dir != None):
            self.dir.fragmentarOrNot()
        else:
            self.processarListas()

    def verificarElemento (node):
        global listaBifurca
        global listaNotBifurca
        if (node == "LPRED"):
            listaNotBifurca.append(node.info)
            # self.notProcessed = (self.nósFolhas(self.info, False));
        elif (node.info.nodeName in ["CONJUNCAO"]):
            listaNotBifurca.append(node.info)
            # self.notProcessed = (self.nósFolhas(self.info, False));
        else:
            listaBifurca.append(node.info)
            # self.notProcessed = (self.nósFolhas(self.info, True));
        return "Yelp!"

    def processarListas(self):
        global listaBifurca
        global listaNotBifurca
        cont = 1
        while(cont == 1) :
            if (listaNotBifurca): #verifica se ela tem elementos
                for elemento in listaNotBifurca:
                    elemento.notProcessed = (elemento.nósFolhas(elemento.info, False));
                    listaNotBifurca.remove(elemento)
            if (listaBifurca):
                for elemente in listaBifurca:
                    if(not listaBifurca):
                        elemento.notProcessed = (elemento.nósFolhas(elemento.info, True));
                        listaNotBifurca.remove(elemento)
                    else:
                        break;
            if listaBifurca == [] and listaNotBifurca == []:
                cont = 0

    def nósFolhas(self, valor, bifurca):
        if self.esq == None and self.dir == None:
            if(bifurca):
                self.insere(valor.firstChild)
                self.insereDireita(valor.lastChild)
                return False #verificar loops de inserção...
            elif (valor.firstChild).nodeName == "LPRED":
                self.insere(valor.firstChild)
            else:
                self.insere(valor.firstChild)
                self.insere(valor.lastChild)
                return False;
        if self.esq != None:
            return self.esq.nósFolhas(valor, bifurca)
        if self.dir != None:
            return self.dir.nósFolhas(valor, bifurca)

DOMTree = xml.dom.minidom.parse("formula.xml")
formula = DOMTree.documentElement
MyTree = Tree()

premissas = formula.getElementsByTagName("PREMISSA")
conclusoes = formula.getElementsByTagName("CONCLUSAO")

listaBifurca = []
listaNotBifurca = []



for premissa in premissas:
    MyTree.insere(premissa.firstChild)

for conclusao in conclusoes:
    if((conclusao.firstChild).hasAttribute("NEG")):
        conclusao.firstChild.removeAttribute("NEG")#futuramente verificar casos de Atributos NEG com + de uma ~
        MyTree.insere(conclusao.firstChild)
    else:
        conclusao.firstChild.setAttribute('NEG', '~')
        MyTree.insere(conclusao.firstChild) #insere a negação em uma conclusão não-negada


MyTree.fragmentarOrNot()
MyTree.preOrdem()
print("XXXXXXXXXX")
print(listaBifurca)
print(("_____--"))
print(listaNotBifurca)