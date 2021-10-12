import datetime
from face_recognition.api import face_locations
import pandas as pd
from pandas.io.sql import read_sql_query
import pyodbc as db
import cv2
import shutil
import face_recognition
from PIL import Image,ImageDraw,ImageFont
from os import remove

def Menu():

    print("\tBookstore")

    print("\n1) Ingresar Nuevo Usuario")
    print("2) Agregar Libro ")
    print("3) Mostrar Libros")
    print("4) Sacar Prestamo Libro")
    print("5) Mostrar Prestamos")
    print("6) Devolver Libro")
    print("7) Salir")

def Conexion():
    #Creo la conexión  a la base de datos
    conexion = db.connect('Driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-3NMGU88;database=proyectoFinalPython;Trusted_Connection=yes')

    return conexion

def AgregarDatos(nombre,apellido):

    con = Conexion()
    cur = con.cursor()

    camara = cv2.VideoCapture(0,cv2.CAP_DSHOW)


    for i in range(10):

        valor,imagen = camara.read()
        cv2.imwrite('./CarpetaBasura/{}_{}{}.png'.format(nombre,apellido,i+1),imagen)

    del(camara)

    nombreArchivo = '{}_{}5.png'.format(nombre,apellido)
    rutaArchivo = './Imagenes/{}'.format(nombreArchivo)
    
    #para Comprobar si se puede reconocer una cara en la foto tomada

    comprobarCara = face_recognition.load_image_file('./CarpetaBasura/{}'.format(nombreArchivo))

    faceLocation = face_recognition.face_locations(comprobarCara)

    if faceLocation:
        
        shutil.copy('./CarpetaBasura/{}'.format(nombreArchivo),'./Imagenes/{}'.format(nombreArchivo))

        consulta = 'spAgregarDatos ?, ?, ?'

        parametros = (nombre,apellido,rutaArchivo)

        cur.execute(consulta,parametros)

        cur.close()
        con.commit()

        print("\nDatos Insertados Correctamente En La Base de Datos UwU")
        print()
    
    else:

        print("\nNo Se Identificar La Cara, Intente Nuevamente :)")

    con.close()

def AgregarLibro(nombreL, GeneroL, AutorL):

    con = Conexion()
    cur = con.cursor()

    consulta = "spAgregarLibro ?,?,?"

    cur.execute(consulta,(nombreL,GeneroL,AutorL))

    cur.close()
    con.commit()
    con.close()

def Mostrarlibros():

    con = Conexion()

    df = pd.read_sql_query("select codLibro as Codigo, nombreLibro as Nombre, generoLibro as Genero,"
     "Autor from tblLibros",con)
    
    print(df)
    con.close()

def sacarPrestamo(cod):

    con = Conexion()

    camara = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    for i in range(10):

        valor, imagen = camara.read()

        cv2.imwrite("./CarpetaBasura/usuario"+str(i+1)+".png",imagen)
    
    del(camara)

    rutaUKF = "./CarpetaBasura/usuario5.png"
    
    fotoCaraPrestamo = face_recognition.load_image_file(rutaUKF)
    comprobarCaraExistente = face_recognition.face_locations(fotoCaraPrestamo)

    usuarios = []
    usuariosEncode = []

    if comprobarCaraExistente:

        codificarCaraPrestamo = face_recognition.face_encodings(fotoCaraPrestamo)[0] 

        df = pd.read_sql_query("select * from tblDatos",con)

        codUser = df['codigo'].tolist()
        nomUser = df['nombre'].tolist()
        apUser = df['apellido'].tolist()
        fotoUser = df['rutaFoto'].tolist()

        cantidad = len(codUser)

        #Cargo las imagenes conocidas
        for i in range(cantidad):
        
            usuarios.append(face_recognition.load_image_file(fotoUser[i]))
            usuariosEncode.append(face_recognition.face_encodings(usuarios[i])[0])
        
        comparacion = face_recognition.compare_faces(usuariosEncode,codificarCaraPrestamo,tolerance=0.5)

        for i in range(cantidad):
            
            if comparacion[i]:

                cur = con.cursor()

                query = "spAgregarPrestamo ?, ?, ?"
                
                fecha = datetime.datetime.now()

                parametros = (codUser[i],cod,fecha)

                dfLibros = read_sql_query("select * from tblLibros",con)

                codLibros = dfLibros['codLibro'].tolist()

                if cod in codLibros:

                    cur.execute(query,parametros)

                    
                    fnt = ImageFont.truetype("arial.ttf",54)

                    objImagen = Image.fromarray(fotoCaraPrestamo)
                    drawFoto = ImageDraw.Draw(objImagen)
                
                    texto = "{} {}".format(nomUser[i],apUser[i])

                    drawFoto.text((100,100),texto,font=fnt,fill=(58, 93, 207))

                    objImagen.show()
                    cur.close()
                    con.commit()

                    print("Prestamo realizado correctamente 7u7 \n")


                else:

                    print("\nEl codigo de libro ingresado no existe </3 \n")

    else:
        print("\nNo se pudo detectar la cara, por favor intente todo nuevamente :b")

    con.close()
    borrarFotosPrestamo()


def mostrarPrestamos():

    con = Conexion()

    datos = pd.read_sql_query("exec spListarPrestamos",con)

    datos.to_html(index=False)

    print(datos)
    con.close()

def regresarLibro(codLibro):

    camara = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    for i in range(10):

        valor,imagen = camara.read()
        cv2.imwrite("./CarpetaBasura/Usuario" + str(i+1) + "devolucion.png",imagen)

    del(camara)
    
    caraDevolucion = face_recognition.load_image_file("./CarpetaBasura/usuario5devolucion.png")

    comprobarCara = face_recognition.face_locations(caraDevolucion)

    if comprobarCara:

        con = Conexion()
        codificarCaraDevolucion = face_recognition.face_encodings(caraDevolucion)[0]

        datosUser = pd.read_sql_query("select * from tblDatos",con)

        codigos = datosUser['codigo'].tolist()
        nombres = datosUser['nombre'].tolist()
        apellidos = datosUser['apellido'].tolist()
        rutaFoto = datosUser['rutaFoto'].tolist()

        cantidad = len(codigos)

        usuarios = []
        usuariosCodificado = []

        for i in range(cantidad):

            usuarios.append(face_recognition.load_image_file(rutaFoto[i]))
            usuariosCodificado.append(face_recognition.face_encodings(usuarios[i])[0])
        
        comprobar = face_recognition.compare_faces(usuariosCodificado,codificarCaraDevolucion,tolerance=0.5)

        Prestamos = pd.read_sql_query("select * from tblPrestamosLibros",con)
        codigosLibros = Prestamos['codLibro'].tolist()


        cur = con.cursor()
        consultaCorrecta = 0

        for i in range(cantidad):

            if comprobar[i] and codLibro in codigosLibros:
                
                fnt = ImageFont.truetype("arial.ttf",55)

                objImagen = Image.fromarray(caraDevolucion)
                drawImagen = ImageDraw.Draw(objImagen)

                texto = "{} {}".format(nombres[i],apellidos[i])

                drawImagen.text((100,100),texto,font=fnt,fill=(58, 93, 207))

                consulta ="spDevolverPrestamo ?, ?"

                cur.execute(consulta,codLibro,codigos[i])
                
                consultaCorrecta = cur.rowcount
                objImagen.show()

        if consultaCorrecta > 0:

            print("\nLibro devuelto correctamente 7u7\n")

        else:

            print("\nFijate bien en el codigo del libro ;-;\n")
                
        cur.close()
        con.commit()
        con.close()
     
    else:

        print("\nNo fue posible completar la operación, por favor intenta nuevamente ;)")
    
    borrarFotosDevolucion()

    
def borrarFotosPrestamo():
    
    Ruta = './CarpetaBasura/Usuario'

    for i in range(10):

        remove('{}{}.png'.format(Ruta,str(i+1)))

def borrarFotosDevolucion():

    ruta = './CarpetaBasura/Usuario'

    for i in range(10):

        remove('{}{}devolucion.png'.format(ruta,str(i+1)))
