from CargarArchivo import cargarArchivo
import AutomataMenu
import AutomataOrden

def verificarNumero():

    correcto = False
    num = 0
    while(not correcto):
        try:
            num = int(input("Seleccione una opción: "))
            correcto = True
        except ValueError:
            print('Error, introduzca un número entero')

    return num

def menuPrincipal():

    salir = False
    opcion = 0

    while not salir:
        print()
        print('1. Cargar menú')
        print('2. Cargar orden')
        print('3. Generar menú')
        print('4. Generar factura')
        print('5. Generar arbol')
        print('6. Salir')

        opcion = verificarNumero()

        if opcion == 1:
            
            ruta = cargarArchivo()
            #ruta = 'menu.lfp'
            archivo = open(ruta, 'r', encoding="utf-8")
            for linea in archivo.readlines():
                print(linea)
                AutomataMenu.Automata(linea)
            AutomataMenu.crearTablas()
        elif opcion == 2:
            ruta = cargarArchivo()
            archivo = open(ruta, 'r', encoding="utf-8")
            for linea in archivo.readlines():
                AutomataOrden.Automata(linea)
            AutomataOrden.crearTablas()
        elif opcion == 3:
            AutomataMenu.crearReporte()
        elif opcion == 4:
            AutomataOrden.crearReporte()
        elif opcion == 6:
            salir = True