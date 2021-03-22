from datetime import time
import webbrowser

class Simbolo:
    def __init__(self,token,lexema,linea,columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna


class Atributo:
    def __init__(self,token,valor):
        self.token = token
        self.valor = valor

class Error:
    def __init__(self,token,lexema,linea,columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

lexem = []
bug = []
i=0
temp = None
t_Atributos = []
t_Simbolos = []
t_Errors = []
t_Objeto = False
state2 =0
space = [' ', ' \t','\n','\r']

def esLetra(text):#analisis de letras
    return ((ord(text) >= 65 and ord(text) <= 90) 
    or (ord(text) >= 97 and ord(text) <= 122) 
    or text == 'á' or text== 'é' or text == 'í' or text == 'ó' or text == 'ú'
    or text == 'Á' or text== 'É' or text == 'Í' or text == 'Ó' or text == 'Ú')

def esNumero(text): # análisis de numeros
    return (ord(text) >= 48 and ord(text) <= 57)

def esDelimitador(text):  #Delimitadores                           [                        ]
    return ((ord(text) == 59) or (ord(text) == 58) or (ord(text) == 91) or (ord(text) == 93) or (ord(text) == 61))

def sonLlaves(text):
    return (ord(text) == 91)
    
def cEspecial(text):
    return (ord(text) == 95) or (ord(text) == 35) or (ord(text) == 46) or (ord(text) == 32)

def sonComillas(text):
    return (ord(text) == 39)

def isState(option,text):
    if option == 1:
        return (esLetra(text) or esNumero(text) or cEspecial(text))
    elif option == 2:
        return esDelimitador(text) or  (text == '\n')
    elif option == 3:
        return sonComillas(text)


def mostrarError(simbolo,expectativa,linea,columna):
    global bug
    print("Error no se reconoce el simbolo: " + simbolo+", se esperaba: "+ expectativa+ "linea: " + str(linea) + ", columna: " + str(columna))


def Automata(texto):
    global lexem,bug,i,temp,t_Atributos,t_Simbolos

    #Flags
    contains_keys = False
    contains_keys2 = False
    state = None
    assistant = ""
    inspace = 0
    bug2 = []
    s = 0
    #Analizador léxico
    for j,k in enumerate(texto):
        #OBTENIENDO TOKENS
        if(isState(1,k)):
            if (state == 3):
                if(ord(k) == 32):
                    if  (len(assistant) > 0):
                        assistant += k
                else:
                    assistant += k
            else:
                if(ord(k) == 32):
                    pass
                else:
                    assistant += k
        #DELIMITADORES
        elif(isState(2,k)):
            #Evaluando caracteres especiales:
            if (ord(k) ==  91):
                contains_keys = True
            elif(ord(k) == 93):
                contains_keys2= True

            #Evaluar el contenido y colocar tokens
            if(len(assistant) > 0):
                token=""
                if (i == 0 ):
                    token = 'NombreRestaurante'
                else:
                    if (contains_keys == True):
                        if (s == 0):
                            token = 'ID'
                        elif ( s == 1):
                            token = 'Nombre'
                        elif ( s == 2):
                            token = 'Precio'
                        elif(s == 3):
                            token = 'Descripcion'
                        s += 1
                    elif(contains_keys2 == True):
                        contains_keys = False
                    else:
                        token ="CARACTER"
                print(token + ' ' + assistant)
                t_Simbolos.append(Simbolo(token,assistant,i+1,(j - len(assistant) - inspace)))
                assistant = ""
            t_Simbolos.append(Simbolo("DELIMITADOR",k,i+1,(j - inspace + 1)))
        elif  (isState(3,k)):   
            if (state == 3):
                state = None
            else:
                state = 3
            
            t_Simbolos.append(Simbolo("DELIMITADOR",k,i+1,(j - len(assistant) - inspace + 1)))
        else:
            if k in space:
                pass
            else:
                bug2 = {
                    'token' : 'Caracter',
                    'valor':k,
                    'linea': i+1,
                    'posicion': j - inspace + 1
                }
                bug.append(bug2)
                t_Errors.append(Error('Simbolo',k,i+1,j - inspace + 1))
    i+=1




def Search(busca):
    global lexem,t_Atributos,t_Objeto
    precio = None
    cont = 0
    for i,s in enumerate(t_Simbolos):
        if (not s.token =='DELIMITADOR'):
            if (s.token == 'ID'):
                if(s.lexema == str(busca)):
                    precio = Price(cont)
                    return(precio)
                cont+=1


def Price(Pos):
    Prices = []
    for i,s in enumerate(t_Simbolos):
        if (not s.token =='DELIMITADOR'):
            if (s.token =='Precio'):
                Prices.append(s.lexema)

    return(Prices[int(Pos)])

def crearTablas():

    crearTablaTokens()
    crearTablaErrors()

"""
def crearReporte():
    f = open('Menu.html', 'w', encoding="utf-8")
    f.write('<!DOCTYPE HTML>\n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<title>Menu Restaurante</title>\n')
    f.write('<meta charset="utf-8" />\n')
    f.write('<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
    f.write('</head>\n')
    f.write('<body class="homepage is-preload">\n')
    f.write('<div id="page-wrapper">\n')
    f.write('<section id="header">\n')
    f.write('<div class="container">\n')
    for t in (t_Simbolos):
        if(not t.token == 'DELIMITADOR'):
            if(t.token == 'NombreRestaurante'):
                if('restaurante' in t.lexema):
                    pass
                else:
                    f.write(str(f'<h1 id="logo"><a href="index.html">{t.lexema}</a></h1>\n'))
                    f.write('<p>¡Opciones deliciosas para todos!</p>\n')
                    f.write('</div>\n')
                    f.write('</section>\n')
                    f.write('<section id="features">\n')
                    f.write('<div class="container">\n')
                    f.write('<header>\n')
            else:
                if(t.token == 'CARACTER'):
                    f.write(f'<h2>{t.lexema}</h2>\n')
                    f.write('</header>\n')
                    f.write('<div class="row aln-center">\n')
                    f.write('<div class="col-4 col-6-medium col-12-small">\n')
                    f.write('<section>\n')
                    f.write('<header>\n')
                elif(t.token == 'Nombre'):
                    nombre = t.lexema
                elif (t.token == 'Precio'):
                    f.write(f'<h3>{nombre}           Q. {t.lexema}</h3>\n')
                    f.write('</header>\n')
                elif (t.token == 'Descripcion'):
                    f.write(f'<p>{t.lexema}</p>\n')
                f.write('</section>\n')


    f.write('</div>\n')
    f.write('</div>\n')
    f.write('</div>\n')
    f.write('</section>\n')
    f.write('<section id="banner">\n')
    f.write('<div class="container">\n')
    f.write('<p>Gracias por leer nuestro menú<br /></p>\n')
    f.write('</div>\n')
    f.write('</section>\n')
    f.write('<section id="footer">\n')
    f.write('<div class="container">\n')
    f.write('<div id="copyright" class="container">\n')
    f.write('<ul class="links">\n')
    f.write('<li>Lenguajes Formales y de Programacion</li><li>Rodrigo Antonio Poron De Leon 201902781</li>\n')
    f.write('</ul>\n')
    f.write('</div>\n')
    f.write('</section>\n')
    f.write('</div>\n')
    f.write('<script src="assets/js/jquery.min.js"></script>\n')
    f.write('<script src="assets/js/jquery.dropotron.min.js"></script>\n')
    f.write('<script src="assets/js/browser.min.js"></script>\n')
    f.write('<script src="assets/js/breakpoints.min.js"></script>\n')
    f.write('<script src="assets/js/util.js"></script>\n')
    f.write('<script src="assets/js/main.js"></script>\n')
    f.write('</body>\n')
    f.write('</html>\n')
   
   
    webbrowser.open_new_tab('Menu.html')"""

def crearReporte():
    f = open('Menu.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<title>Menu Restaurante</title>\n')
    f.write('<link href="prac.css" rel="stylesheet" type="text/css" />\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<div class="container">\n')
    f.write('<article>\n')
    f.write('<pre><code>\n')

    for s in t_Simbolos:
        if (not s.token =='DELIMITADOR'):
            if (s.token == 'NombreRestaurante'):
                if ('restaurante' in s.lexema):
                    pass
                else:
                    f.write(str(f'<center><h2><strong>{s.lexema}</strong><h2></center> \n'))
            else:
                if (s.token == 'CARACTER'):
                    f.write(str(f'<h3> + {s.lexema} </h3>\n'))
                elif(s.token == 'Nombre'):
                    nombre = s.lexema
                elif (s.token == 'Precio'):
                    f.write(str(f'<h3> \t *{nombre}   Q. {s.lexema} </h3>\n'))
                elif (s.token == 'Descripcion'):
                    f.write(str(f'\t -> {s.lexema} \n'))


    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()
    webbrowser.open_new_tab('Menu.html')

def crearTablaTokens():
    f = open('TokensMenu.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
    f.write('<title>Restaurante</title>\n')
    f.write('<link href="prac.css" rel="stylesheet" type="text/css" />\n')
    f.write('<link href="Hojas de estilos/menu pagina principal.css" rel="stylesheet" type="text/css" />\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<div class="container">\n')
    f.write('<article>\n')
    f.write('<pre><code>\n')
    
    f.write('<center><h2> Tabla de Tokens </h2></center>')
    f.write('<center><table></center>\n')
    f.write('<thead>\n')
    f.write(' <tr> \n')
    f.write('<th><h3><strong>NO.</strong></h3></th>  \n')
    f.write('<th><h3><strong>Token</strong></h3></th>  \n')
    f.write('<th><h3><strong>lexema</strong></h3></th>  \n')
    f.write('<th><h3><strong>Fila</strong></h3></th>  \n')
    f.write('<th><h3><strong>Columna</strong></h3></th>  \n')
    f.write('</tr>  \n')
    f.write('</thead>  \n')
    f.write('<tbody>  \n')
    cont = 1
    for s in t_Simbolos:
        if (not s.token =='DELIMITADOR'):
            f.write('<tr> \n')
            f.write('<td><h4>'+ str(cont)  +'</h4></td>  \n')
            f.write('<td><h4>'+ s.token    +'</h4></td> \n')
            f.write('<td><h4>'+ s.lexema   +'</h4></td>\n')
            f.write('<td><h4>'+ str(s.linea)   +' </h4></td> \n')
            f.write('<td><h4>'+ str(s.columna)  +' </h4></td> \n')
            f.write('</tr>  \n')
            cont += 1
    f.write('</tbody>  \n')
    f.write('</table>  \n')
    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()

def crearTablaErrors():
    f = open('ErroresMenu.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
    f.write('<title>Lenguajes Formales</title>\n')
    f.write('<link href="prac.css" rel="stylesheet" type="text/css" />\n')
    f.write('<link href="Hojas de estilos/menu pagina principal.css" rel="stylesheet" type="text/css" />\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<div class="container">\n')
    f.write('<article>\n')
    f.write('<pre><code>\n')
    
    f.write('<center><h2> Tabla de Errores </h2></center>')
    f.write('<center><table></center>\n')
    f.write('<thead>\n')
    f.write(' <tr> \n')
    f.write('<th><h3><strong>NO.</strong></h3></th>  \n')
    f.write('<th><h3><strong>Token</strong></h3></th>  \n')
    f.write('<th><h3><strong>lexema</strong></h3></th>  \n')
    f.write('<th><h3><strong>Fila</strong></h3></th>  \n')
    f.write('<th><h3><strong>Columna</strong></h3></th>  \n')
    f.write('</tr>  \n')
    f.write('</thead>  \n')
    f.write('<tbody>  \n')
    cont = 1
    for s in t_Errors:
        f.write('<tr> \n')
        f.write('<td><h4>'+ str(cont)  +'</h4></td>  \n')
        f.write('<td><h4>'+ s.token    +'</h4></td> \n')
        f.write('<td><h4>'+ s.lexema   +'</h4></td>\n')
        f.write('<td><h4>'+ str(s.linea)   +' </h4></td> \n')
        f.write('<td><h4>'+ str(s.columna)  +' </h4></td> \n')
        f.write('</tr>  \n')
        cont += 1

    f.write('</tbody>  \n')
    f.write('</table>  \n')



    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()