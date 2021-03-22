#Creacion de Automata que reconoce los simbolos del sistema provenientes del sistema
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import webbrowser
from datetime import datetime
import AutomataMenu

class Simbol:
    def __init__(self,ID,ID2,token,lexema,linea,columna):
        self.ID = ID
        self.ID2 = ID2
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna


def esLetra(text): 
    return ((ord(text) >= 65 and ord(text) <= 90) 
    or (ord(text) >= 97 and ord(text) <= 122) 
    or text == 'á' or text== 'é' or text == 'í' or text == 'ó' or text == 'ú'
    or text == 'Á' or text== 'É' or text == 'Í' or text == 'Ó' or text == 'Ú')

def esNumero(text): 
    return (ord(text) >= 48 and ord(text) <= 57)

def esDelimitador(text): 
    return ((ord(text) == 59) or (ord(text) == 58) or (ord(text) == 91) or (ord(text) == 93) or (ord(text) == 61) or (ord(text)==44))

def sonLlaves(text):
    return (ord(text) == 91)
    
def cEspecial(text):  
    return (ord(text) == 95) or (ord(text) == 35) or (ord(text) == 46) or (ord(text) ==32 or (ord(text) ==37) or ( ord(text) == 45))

def sonComillas(text):
    return (ord(text) ==39)

def isState(option,text):
    if option == 1:
        return (esLetra(text) or esNumero(text) or cEspecial(text))
    elif option == 2:
        return esDelimitador(text) or  (text == '\n')
    elif option == 3:
        return sonComillas(text)

space = [' ', ' \t','\n','\r']

lexem = []
bug = []
i=0
temp = None
t_Atributos = []
t_Simbolos = []
t_Objeto = False
state2 =0
domin=0


def Automata(texto):
    global lexem,bug,i,temp,t_Atributos,t_Simbolos,domin
    caracteres = texto

    state = None
    assistant = ""
    inspace = 0
    bug2 = []

    
    for j,k in enumerate(texto):
        #Obtencion de tokens
        #Analisis Lexico
        if(isState(1,k)):
            if (state == 3):
                if(ord(k) == 32):
                    if (len(assistant) > 0):
                        assistant += k
                else:
                    assistant += k
            else:
                if(ord(k) == 32):
                    pass
                else:
                    assistant += k
        ##Verficando delimitadores
        elif(isState(2,k)):

            if(len(assistant) > 0):
                lexema = None
                if ((assistant.isdigit()) or (("." in assistant) and (not '%' in assistant) and (not '-' in assistant))):
                    lexema = {
                        'token': 'numero',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                elif ((assistant.isdigit()) or (("." in assistant)) or ('%' in assistant)):
                    lexema = {
                        'token': 'Porcentaje',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                elif ((assistant.isdigit()) or ('-' in assistant)):
                    lexema = {
                        'token': 'NIT',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                elif (domin == 2):
                    lexema = {
                        'token': 'Pais',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                elif ((assistant.istitle()) and domin == 0):
                     lexema = {
                        'token': 'Nombre',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                else:
                    lexema = {
                        'token': 'ID',
                        'valor': assistant,
                        'linea': i+1,
                        'columna': j - len(assistant) -inspace
                    }
                lexem.append(lexema)
                assistant = ""
                domin +=1
            lexema = {
                'token': 'delimitador',
                'valor': k,
                'linea': i+1,
                'columna': j - inspace + 1
            }
            lexem.append(lexema)
        elif  (isState(3,k)):
            if (state == 3):
                state = None
            else:
                state = 3
            lexema = {
                'token': 'delimitador',
                'valor': k,
                'linea': i+1,
                'columna': j - inspace + 1
            }
            lexem.append(lexema)

        else:
            if k in space:
                pass
            else:
                bug2 = {
                    'token' : 'Desconocido',
                    'value':k,
                    'line': i+1,
                    'columna': j - inspace + 1
                }
                bug.append(bug2)
    i +=1


def comprobadorNombre(nombre):
    nombrevalido = True
    for x in nombre:
        if ((x.isalpha()==True) or (x == ".")):
            pass
        else:
            nombrevalido = False
    return nombrevalido



def crearReporte():
    global cuentaFac,lexem
    f = open('Factura.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<title>Lenguajes Formales</title>\n')
    f.write('<link href="Hojas de estilos/menu pagina principal.css" rel="stylesheet" type="text/css" />\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<div class="container">\n')
    f.write('<article>\n')

    f.write('<pre><code>\n')
    f.write('<center><h3>Restaurante LFP </h2></center>\n')
    f.write('<center><h3>Factura Consumo</h2></center>\n')
    for lexems in lexem:
        if( lexems ['token'] == 'Nombre'):
            f.write('<h4>NOMBRE:  '+lexems['valor'] +'</h4></center>\n')
        elif(lexems ['token'] == 'NIT'):
            f.write('<h4>NIT:  '+lexems['valor'] +' </h4></center>\n')
        elif(lexems ['token'] == 'Pais'):
            f.write('<h4>Direccion:  '+lexems['valor'] +' </h4></center>\n')
    f.write('<center><table></center>\n')
    f.write('<thead>\n')
    f.write(' <tr> \n')
    f.write('<th><h3><strong>Cantidad.</strong></h3></th>  \n')
    f.write('<th><h3><strong>Concepto</strong></h3></th>  \n')
    f.write('<th><h3><strong>Precio</strong></h3></th>  \n')
    f.write('<th><h3><strong>Total</strong></h3></th>  \n')
    f.write('</tr>  \n')
    f.write('</thead>  \n')
    f.write('<tbody>  \n')
    cont = 0
    Totaltot = []
    for lexems in lexem:
        if(not lexems ['token'] == 'delimitador'):
            if (not ( lexems ['token'] == 'Nombre') and not ( lexems ['token'] == 'NIT') and not ( lexems ['token'] == 'Pais') and not ( lexems ['token'] == 'Porcentaje') ):
                cont+=1

    for i in range(int(cont/2)):
        f.write('<tr> \n')
        f.write('<td><h4>'+ cant(i)  +'</h4></td>  \n')
        f.write('<td><h4>'+ qId(i)    +'</h4></td> \n')
        f.write('<td><h4>'+' Q '+ AutomataMenu.Search(qId(i))   +'</h4></td>\n')
        f.write('<td><h4>'+' Q '+ str(Total(cant(i),AutomataMenu.Search(qId(i))))   +'</h4></td>\n')
        Totaltot.append(Total(cant(i),AutomataMenu.Search(qId(i))))
        f.write('</tr>  \n')

    f.write('</tbody>  \n')
    f.write('</table>  \n')

    f.write(' <hr>\n')
    
    f.write('<h4>'+str('Sub Total                                                                                                          Q {} '.format( subTotal(Totaltot) ) + '</h4>\n'))
    propina = 0
    for lexems in lexem:
        if(not lexems ['token'] == 'delimitador'):
            if( lexems['token'] == 'Porcentaje'):
                f.write('<h4>'+str('Propina                                                                                                             Q {} '.format( str(lexems['valor']) ) + '</h4>\n'))
                propina = lexems['valor']
    f.write(' <hr>\n')
    f.write('<h4>'+str('Total                                                                                                               Q {} '.format( str(Total2(subTotal(Totaltot),propina)) ) + '</h4>\n'))
    
    
    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()
    webbrowser.open_new_tab('Factura.html')

def cant(Pos):
    Cant = []
    for lexems in lexem:
        if(not lexems ['token'] == 'delimitador'):
            if (not ( lexems ['token'] == 'Nombre') and not ( lexems ['token'] == 'NIT') and not ( lexems ['token'] == 'Pais') and not ( lexems ['token'] == 'Porcentaje') ):
                if (lexems['token'] == 'numero'):
                    Cant.append(lexems['valor'])
    return(Cant[int(Pos)])

def qId(Pos):
    QId = []
    for lexems in lexem:
        if(not lexems ['token'] == 'delimitador'):
            if (not ( lexems ['token'] == 'Nombre') and not ( lexems ['token'] == 'NIT') and not ( lexems ['token'] == 'Pais') and not ( lexems ['token'] == 'Porcentaje') ):
                if (lexems['token'] == 'ID'):
                    QId.append(lexems['valor'])
    return(QId[int(Pos)])

def subTotal(tot):
    sub = 0
    for i in tot:
        sub +=i
    return sub

def Total2(subTot, Propina):
    propina = Propina
    keyword = propina.split('%')
    prop = keyword[0]
    quitar = (float(prop)/ 100)
    descuento = (subTot * quitar)
    TotalT = subTot + descuento
    return TotalT

def Total(cant,price):
    precio = float(price)
    cuantos = int(cant)
    total = cuantos * precio
    return  total


def crearTablas():
    crearTablaTokens()
    crearTablaErrors()


def crearTablaTokens():
    global lexem
    f = open('TokensOrden.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<title>Lenguajes Formales</title>\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
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
    #Datos.-------------------
    cont = 1
    for lexems in lexem:
        if(not lexems ['token'] == 'delimitador'):
            f.write('<tr> \n')
            f.write('<td><h4>'+ str(cont)  +'</h4></td>  \n')
            f.write('<td><h4>'+ lexems['token']  +'</h4></td> \n')
            f.write('<td><h4>'+ str(lexems['valor'])  +'</h4></td>\n')
            f.write('<td><h4>'+ str(lexems['linea'])  +' </h4></td> \n')
            f.write('<td><h4>'+ str(lexems['columna'])  +' </h4></td> \n')
            f.write('</tr>  \n')
            cont += 1

    #Fin datos------------------
    f.write('</tbody>  \n')
    f.write('</table>  \n')



    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()

def crearTablaErrors():
    f = open('ErroresOrden.html', 'w')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n')
    f.write('<title>Lenguajes Formales</title>\n')
    f.write('<link rel="stylesheet" href="assets/css/main.css" />\n')
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
    #Datos.-------------------
    cont = 1
    for bugs in bug:
        f.write('<tr> \n')
        f.write('<td><h4>'+ str(cont)  +'</h4></td>  \n')
        f.write('<td><h4>'+ bugs['token']  +'</h4></td> \n')
        f.write('<td><h4>'+ str(bugs['value'])  +'</h4></td>\n')
        f.write('<td><h4>'+ str(bugs['line'])  +' </h4></td> \n')
        f.write('<td><h4>'+ str(bugs['columna'])  +' </h4></td> \n')
        f.write('</tr>  \n')
        cont += 1

    #Fin datos------------------
    f.write('</tbody>  \n')
    f.write('</table>  \n')



    f.write('</code></pre>\n')
    f.write('</article>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>>\n')
    f.close()
