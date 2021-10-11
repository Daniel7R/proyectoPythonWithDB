from Funciones import *

opcion = 0

m = True

while m:

    Menu()
    opcion = int(input("\tDigite su opción: "))

    if opcion ==1:

        res = ''
        nombre = input("\nDigite el nombre del nuevo usuario: ")
        apellido = input("Digite el apellido del nuevo usuario: ")
        print("\nVamos a Tomar Su Foto Para Agregarla Al Sistema")
        print("Digite la letra 'S' si está de acuerdo, de lo contrario "
        "presione cualquier letra para evitar el registro: ")
        res = input("\tOpcion: ")

        if res == 'S' or res =='s':
            
            AgregarDatos(nombre,apellido)

    elif opcion == 2:

        nombreL = input("\nDigite el nombre del libro: ")
        generoL = input("Digite el género del libro: ")
        autorL = input("Digite el autor del libro: ")

        AgregarLibro(nombreL,generoL,autorL)

        print("Libro Agregado Correctamente UwU")

    elif opcion == 3:
        
        print("\n\tMostrando Listado de Libros...\n\n")
        Mostrarlibros()
        print()

    elif opcion == 4:
        
        res = 0

        print("\nSacando Prestamo...\n")

        Mostrarlibros()

        codL = int(input("\tDigite el código del libro que desea sacar: "))

        sacarPrestamo(codL)

    elif opcion == 5:
        
        print("\nMostrando Prestamos... :3\n")
        mostrarPrestamos()
        print()

    elif opcion == 6:
        
        Mostrarlibros()
        codLibro = int(input("\n\tDigite el codigo del libro que desea regresar: "))

        regresarLibro(codLibro)

    elif opcion==7:
        
        m = False
        print("Ha decidido salir del sistema :(, Bye Bye")