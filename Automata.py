class Simbolo:

    def __init__(self,token,lexema,linea,columna):
        self.token = token 
        self.lexema = lexema 
        self.linea = linea
        self.columna = columna 

class Atributo:
    def __init__(self,id,valor):
        self.id = id
        self.valor = valor

tablaSimbolos = []
tablaAtributos = []
fila = 0
columna = 0
flagExpresionId = False
flagExpresionCadena = False
flagExpresionNumero = False
flagExpresionSeccion = False
valor = ""
estado = 0
traduccion = ""

temp = None

flagAutomataAsignacion = False
flagAutomataObjeto = False

def mostrarError(simbolo,expectativa,linea,columna):
    print("Error, no se reconoce el simbolo: " + simbolo + ", se esperaba: " + expectativa + " linea: " + str(linea) + ", columna: " + str(columna) )

def isLetter(c):
    return (ord(c) >= 65 and ord(c) <= 90) or  (ord(c) >= 97 and ord(c) <= 122)

def isNumber(c):
    return (ord(c) >= 48 and ord(c) <= 57)

def isUnderScore(c):
    return (ord(c) == 95)

def expresionRegularId(c):
    global valor,columna,fila,flagExpresionId
    
    if isLetter(c) or isNumber(c) or isUnderScore(c):
        valor += c
        columna += 1
        return
    elif ord(c) == 32: #espacio
        valor += c
        columna += 1
        tablaSimbolos.append(Simbolo("ID",valor,fila,(columna - 1 - len(valor))))
        valor = ""
        flagExpresionId = False
    elif ord(c) == 61: #igual
        tablaSimbolos.append(Simbolo("ID",valor,fila,(columna  - len(valor))))
        columna += 1
        tablaSimbolos.append(Simbolo("simbolo_igual","=",fila,(columna - 2)))
        valor = ""
        flagExpresionId = False
    else:
        mostrarError(c,"",fila,columna)

""" def expresionRegularSeccion(c):
    global valor,columna,fila,flagExpresionSeccion
    if ord(c) == 39:
        columna += 1
        valor += c 
        return
    elif ord(c) == 32: #espacio
        valor += c
        columna += 1
        tablaSimbolos.append(Simbolo("SECCION",valor,fila,(columna - 1 - len(valor))))
        valor = ""
        flagExpresionSeccion = False
    elif ord(c) == 58: #dos puntos
        tablaSimbolos.append(Simbolo("SECCION",valor,fila,(columna  - len(valor))))
        columna += 1
        tablaSimbolos.append(Simbolo("dos_puntos",":",fila,(columna - 2)))
        valor = ""
        flagExpresionSeccion = False
    else:
        print('Entro al else')
        mostrarError(c,"",fila,columna)
    columna += 1
    valor += c """

def expresionRegularCadena(c):
    global valor,columna,fila,flagExpresionCadena 

    if ord(c) == 39:
        columna += 1
        valor += c 
        tablaSimbolos.append(Simbolo("CADENA",valor,fila,(columna - 1 - len(valor))))
        valor = ""
        flagExpresionCadena = False
        return; 
    
    columna += 1
    valor += c

def expresionRegularNumero(c):
    global columna,fila,flagExpresionNumero,valor
    if isNumber(c):
        columna += 1
        valor += c
        return 

    columna += 1
    tablaSimbolos.append(Simbolo("NUMERO",valor,fila,(columna - 1 - len(valor))))
    valor = ""
    flagExpresionNumero = False


def analizadorLexico(c):
    global fila,columna,flagExpresionId,valor,flagExpresionCadena,flagExpresionNumero,flagExpresionSeccion,valor
    if flagExpresionId:
        expresionRegularId(c)
    elif flagExpresionCadena:
        expresionRegularCadena(c)
    elif flagExpresionNumero:
        expresionRegularNumero(c)
    #elif flagExpresionSeccion:
        #expresionRegularSeccion(c)
    elif isLetter(c):
        columna += 1
        flagExpresionId = True
        valor = c
    elif isNumber(c):
        columna += 1 
        valor = c
        flagExpresionNumero = True
    elif ord(c) == 61: #=
        columna += 1
        valor = c
        tablaSimbolos.append(Simbolo("simbolo_igual","=",fila,(columna - 2)))
        valor = ""
    elif ord(c) == 39: #''
        flagExpresionCadena = True
        valor = c
        columna += 1
    elif ord(c) == 58: #dos puntos
        columna += 1
        valor = c
        tablaSimbolos.append(Simbolo("dos_puntos",c,fila,(columna - 2)))
    elif ord(c) == 91: #[
        columna += 1
        valor = c
        tablaSimbolos.append(Simbolo("simbolo_llave_abre",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 93: #]
        columna += 1
        valor = c
        tablaSimbolos.append(Simbolo("simbolo_llave_cierra",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 44: #,
        columna += 1
        valor = c
        tablaSimbolos.append(Simbolo("simbolo_coma",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 10: #salto de linea
        fila += 1
        columna = 0
        valor = ""
    elif ord(c) == 32: #espacio
        columna += 1
        valor = ""
    else: 
        mostrarError(c,"",fila,columna)

def automataAsignacion(s):
    global estado, traduccion,flagAutomataAsignacion,columna,fila
    if estado == 0:
        if s.token == "simbolo_igual":
            traduccion += " = "
            estado = 1
        else:
            mostrarError(s.lexema,"=",s.fila,s.columna)
            estado = -1
            flagAutomataAsignacion = False
    elif estado == 1:
        if s.token == "CADENA" or s.token == "NUMERO":
            traduccion += s.lexema
            estado = 0
            flagAutomataAsignacion = False
        else:
            mostrarError(s.lexema,"una expresión",s.fila,s.columna)
            estado = -1
            flagAutomataAsignacion = False

def automataObjeto(s):
    global temp,tablaAtributos,estado,flagAutomataObjeto
    if estado == 0:
        if s.token == "simbolo_llave_abre":
            estado = 1
        else:
            estado = -1
            flagAutomataObjeto = False
            mostrarError(s.lexema,"[",s.linea,s.columna)
    elif estado == 1:
        if s.token == "ID":
            temp = Atributo(s.lexema,"")
            estado = 2
        else:
            estado = -1
            flagAutomataObjeto = False
            mostrarError(s.lexema,"ID",s.linea,s.columna) 
    elif estado == 2:
        if s.token == "simbolo_igual":
            estado = 3
        else:
            estado = -1
            flagAutomataObjeto = False
            mostrarError(s.lexema,"=",s.linea,s.columna)
    elif estado == 3:
        if s.token == "CADENA":
            estado = 4
            temp.valor = s.lexema
            tablaAtributos.append(temp)
            temp = None
        else:
            estado = -1
            flagAutomataObjeto = False
            mostrarError(s.lexema,"CADENA",s.linea,s.columna)
    elif estado == 4:
        if s.token == "simbolo_coma":
            estado = 0
        elif s.token == "simbolo_llave_cierra": #estado de aceptacion
            estado = 0
            flagAutomataObjeto = False
        else:
            estado = -1
            flagAutomataObjeto = False
            mostrarError(s.lexema,"] o ,",s.linea,s.columna)


tablaSimbolos = []
fila = 0
columna = 0

with open('menup.lfp', 'r', encoding='utf-8') as f:
    contenido_archivo = f.read()
contenido_archivo = contenido_archivo + " "

#cadena = "[id1 =\"valor1\", id2 = \"valor2\"] \n [ id3 = \"valor3\", id4 = \"valor4\"]"
#cadena = "hola2_=\"Como estas\""
caracteres = list(contenido_archivo)
print(caracteres)

for c in caracteres:
    analizadorLexico(c)

for s in tablaSimbolos:
    if flagAutomataAsignacion:
        automataAsignacion(s)
    elif s.token == "ID":
        estado = 0
        flagAutomataAsignacion = True
        traduccion += "\n let " + s.lexema
    elif flagAutomataObjeto:
        automataObjeto(s)
    elif s.token == "dos_puntos":
        estado = 0
        flagAutomataObjeto = True
        flagAutomataAsignacion = False
    else:
        mostrarError(s.lexema,":",s.linea,s.columna)

""" for a in tablaAtributos:
    print(a.id + ": " + a.valor) """
print(traduccion)

    

