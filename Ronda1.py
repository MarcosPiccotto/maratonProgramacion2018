#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Inicio Ronda 2 - 2019

#importamos librerias para su posterior uso
import pygame
import random
import time

#Inicializamos la librería Pygame y demás variables
pygame.init()
pygame.font.init()
pygame.display.set_caption('Maraton 2019 - Inicio Ronda 1')
pantalla = pygame.display.set_mode((1152,648))

tipografiaDatos = pygame.font.Font('fuentes/RalewayFont.ttf', 18 )
tipografiaMenu = pygame.font.Font('fuentes/Pagadang.ttf', 100)
tipografia = pygame.font.SysFont('Comic Sans MS', 18)
tipografiaGanaste = pygame.font.SysFont('Comic Sans MS', 26)
tipografiaGrande = pygame.font.SysFont('Comic Sans MS', 24)

#cargamos la musica del menu
pygame.mixer.music.load('musica/musicaMenu.mp3')
pygame.mixer.music.play(loops=-1)

#cargamos el sonido del salto
global musicaSalto
musicaSalto = pygame.mixer.Sound('musica/jump.ogg')

#inicializamos variables globales para su posterior uso
global nivelCompletado
nivelCompletado = False

global zonaDeTransporte

global contadorMovimiento
contadorMovimiento = 0

global energia
energia = 7000

global puntaje
puntaje = 0

global posicionJugador
posicionJugador = [2,5]

global posicionVirus
posicionVirus = [(3,5),(4,5),(5,5),(6,5),(5,6)]

global salirJuego
salirJuego = False

global tiempoInicial
tiempoInicial = 0

global tiempoReinicio
tiempoReinicio = 0

global minutos
minutos = 0

global segundos
segundos = 0

global detenerJuego
detenerJuego = False

global repitiendoJuego
repitiendoJuego = True

global lstZonasProtegidas
lstZonasProtegidas = []

global lstZonasEliminadas
lstZonasEliminadas = ['ninguna']

global imgAmenaza

#Creamos un diccionario donde se van a guardar todos los datos que querramos utilizar para la mecanica de retroceder
global dicRegistro
dicRegistro = {'posPlayer':[(2,5)],
               'posVirus1':[(3,5)],
               'posVirus2':[(4,5)],
               'posVirus3':[(5,5)],
               'posVirus4':[(6,5)],
               'posVirus5':[(5,6)],
               'bateria' : [7000],
               'movimientos' :[0]
               }

#creamos otro diccionario donde se van guardar todos los datos para usarlos en la mecanica del replay
dicRepetirJuego = {'posPlayer':[(2,5)],
               'posVirus1':[(3,5)],
               'posVirus2':[(4,5)],
               'posVirus3':[(5,5)],
               'posVirus4':[(6,5)],
               'posVirus5':[(5,6)],
               'bateria' : [7000],
               'movimientos' :[0]
               }

#creamos colores y el tamaño de mi zona de juego
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja = (11,102,35),(0,0,255),(255,255,255),(0,0,0),(239,27,126)
cantidadDeCasillasPorLado = 8 
cantPixelesPorLadoCasilla = 72

#Cargamos las imágenes
imgPlayer = pygame.image.load('player/idle.png')

imgPared = pygame.image.load('imagenes/pared2.png')

listaAmenazas  = ['imagenes/troyanos.png','imagenes/virusvioleta.png','imagenes/virusrojo.png','imagenes/virusGusano.png']
imgAmenaza = pygame.image.load(str(random.choice(listaAmenazas)))

imgAreaProtegida = pygame.image.load('imagenes/seguridad.png')

imgPlayer = pygame.transform.scale(imgPlayer, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgPared=pygame.transform.scale(imgPared, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgAmenaza=pygame.transform.scale(imgAmenaza, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgAreaProtegida=pygame.transform.scale(imgAreaProtegida, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

#Creamos el mapa del nivel y algunas operaciones para los elementos que se encuentran dentro de la zona de transporte
def crearZonaDeTransporte():
    global lstZonasProtegidas
    
    zonaDeTransporte = [[0 for x in range(cantidadDeCasillasPorLado+1)] for y in range(cantidadDeCasillasPorLado+1)]

    zonaDeTransporte[1][3] = 'pared'
    zonaDeTransporte[2][3] = 'pared'
    zonaDeTransporte[3][3] = 'pared'
    zonaDeTransporte[4][3] = 'pared'
    zonaDeTransporte[5][3] = 'pared'
    zonaDeTransporte[6][3] = 'pared'
    zonaDeTransporte[7][3] = 'pared'
    zonaDeTransporte[8][3] = 'pared'

    zonaDeTransporte[1][7] = 'pared'
    zonaDeTransporte[2][7] = 'pared'
    zonaDeTransporte[3][7] = 'pared'
    zonaDeTransporte[4][7] = 'pared'
    zonaDeTransporte[5][7] = 'pared'
    zonaDeTransporte[6][7] = 'pared'
    zonaDeTransporte[7][7] = 'pared'
    zonaDeTransporte[8][7] = 'pared'

    zonaDeTransporte[1][4] = 'pared'
    zonaDeTransporte[1][5] = 'pared'
    zonaDeTransporte[1][6] = 'pared'
    zonaDeTransporte[8][4] = 'pared'
    zonaDeTransporte[8][5] = 'pared'
    zonaDeTransporte[8][6] = 'pared'

    zonaDeTransporte[2][5] = 'jugador'

    #decidimos que cada virus lleve como un tag diferente
    zonaDeTransporte[3][5] = 'virus1'      
    zonaDeTransporte[4][5] = 'virus2'    
    zonaDeTransporte[5][5] = 'virus3'    
    zonaDeTransporte[6][5] = 'virus4' 
    zonaDeTransporte[5][6] = 'virus5'

    lstZonasProtegidas.append((2,4))
    lstZonasProtegidas.append((2,6))
    lstZonasProtegidas.append((7,4))
    lstZonasProtegidas.append((7,6))
    lstZonasProtegidas.append((4,6))
    

    return zonaDeTransporte


zonaDeTransporte = crearZonaDeTransporte()

#Funcion que nos devuelve si en las cordenadas recibidas hay o no una zona protegida
def hayZonaProtegidaEn(x,y):
    punto = (x,y)
    return lstZonasProtegidas.__contains__(punto)

#posiciona un elemento en las cordenadas indicadas
def posicionarElemento(elemento,x,y):
    zonaDeTransporte[x][y] = elemento

#borra un elemento en las cordenadas indicadas
def borrarElemento(x,y):
    zonaDeTransporte[x][y] = 0

#Dibujamos la zona de transporte, fondo y reglas
def dibujarZonaDeTransporte():
    cnt = 0
    for i in range(1,cantidadDeCasillasPorLado+1):
        for j in range(1,cantidadDeCasillasPorLado+1):

            if cnt % 2 == 0:
                pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])

            else:
                pygame.draw.rect(pantalla, colorVerde, [cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])

            if hayZonaProtegidaEn(j,i) == True:
                pantalla.blit(imgAreaProtegida, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))

            if zonaDeTransporte[j][i] == 'jugador':
               pantalla.blit(imgPlayer, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))

            if zonaDeTransporte[j][i] == 'pared':
               pantalla.blit(imgPared, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))

            if zonaDeTransporte[j][i] == 'virus1' or zonaDeTransporte[j][i] == 'virus2' or zonaDeTransporte[j][i] == 'virus3' or zonaDeTransporte[j][i] == 'virus4' or zonaDeTransporte[j][i] == 'virus5' :
               pantalla.blit(imgAmenaza, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))
            cnt +=1
        cnt-=1
        
    pygame.draw.rect(pantalla,colorBlanco,[cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)
    pygame.display.update()

#coloca el fondo de cuando estamos jugando
def dibujarFondo():
    fondo = pygame.image.load('imagenes/fondoJugando.jpg')
    pantalla.blit(fondo, (0, 0))

#dibuja los datos que el usuario puede ver
def dibujarReglas():
    textoReglas = tipografiaDatos.render('Te podes mover con las flechas, si presionas R se reinicia el juego y si apretas X volves un paso en el tiempo', False, colorBlanco)

    ancho=930
    alto=46
    x=220
    y=0
    pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
    pantalla.blit(textoReglas,(x+5,y,ancho,alto))
    pygame.display.update()

#dibuja el estado del juego
def dibujarFelicitacion():
    global nivelCompletado

    x=0
    y=0
    ancho=190
    alto=46

    if nivelCompletado==True:
        textoFelicitacion = tipografiaDatos.render('Ganaste', False, colorBlanco)

    else:
        textoFelicitacion = tipografiaGanaste.render('Juego en curso', False, colorBlanco)

    pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    pygame.display.update()

#dibujamos en la pantalla un rectangulo y el contador de movimiento
def dibujarMovimiento():
    global contadorMovimiento
    textoMovimiento = tipografiaDatos.render('contador de movimiento ' + str(contadorMovimiento), False, colorBlanco)
    ancho=510
    alto=30
    x=650
    y=600
    pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
    pantalla.blit(textoMovimiento,(x+5,y,ancho,alto))
    pygame.display.update()

#dibuja el escenario y todo lo visual para el usuario
def dibujarTodo():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('musica/musicaJugando.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
    
    dibujarFondo()
    dibujarZonaDeTransporte()
    dibujarReglas()
    actualizarContadorDeElectricidad(0)
    dibujarMovimiento()
    pygame.display.update()

#Creamos una operación que indique si el nivel fue solucionado
def estaSolucionado():
    global nivelCompletado
    global imgAmenaza
    global puntaje
    global energia
    global minutos
    global segundos
    global lstZonasProtegidas
    global lstZonasEliminadas
    
    cantvirusesSobreTomas = 0

    for punto in lstZonasProtegidas:
        
        x=punto[0]
        y=punto[1]
        
        if zonaDeTransporte[x][y]=='virus1' or zonaDeTransporte[x][y]=='virus2' or zonaDeTransporte[x][y]=='virus3' or zonaDeTransporte[x][y]=='virus4' or zonaDeTransporte[x][y]=='virus5':
            cantvirusesSobreTomas += 1
            borrarElemento(x,y)
            lstZonasEliminadas.pop()
            lstZonasEliminadas.append(punto)
            lstZonasProtegidas.pop(lstZonasProtegidas.index(punto))
            
        if len(lstZonasProtegidas) == 0:
            puntaje = int(energia / ((minutos * 60) + segundos))
            pygame.mixer.music.stop()
            menuGanaste()
            nivelCompletado = True
           
        else:
            nivelCompletado=False

    dibujarFelicitacion()
    dibujarReglas()

#actualizamos el texto de la bateria
def actualizarContadorDeElectricidad(decremento):
    global energia
    ancho=550
    alto=40
    
    if energia > 0:
        x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
        y=cantPixelesPorLadoCasilla*6
        pygame.draw.rect(pantalla,colorAzul,(x,y,ancho,alto))
        energia -= decremento
        textoEnergia = tipografiaDatos.render('Bateria disponible: ' + str(energia) + 'mA', False, colorBlanco)
        pantalla.blit(textoEnergia,(x+5,y,ancho,alto))
        pygame.display.update()
        
    else:
        resetearJuego()

#cargamos la imagen del player     
def actualizarImgPlayer(x):
    global imgPlayer
    imgPlayer = pygame.image.load('player/' + x + '.png')
    imgPlayer = pygame.transform.scale(imgPlayer, (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

#modificamos la posicion del jugador
def actualizarPosJugador(posX,posY):
    global posicionJugador
    posicionJugador = [posX,posY]
    
#modificamos la posicion de un determinado virus
def actualizarPosVirus(virusId,posX,posY):
    global posicionVirus
    #Seteamos la nueva posicion del virus correspondiente en la lista de tuplas de posiciones de los virus    
    posicionVirus[(int)(virusId[5]) - 1] = [posX, posY]

#nos preguntamos si en X direccion y distancia hay un virus en caso afirmativo devuelve el nro del mismo
def encontrarVirus(direccion, distancia):
    global zonaDeTransporte
    global posicionJugador
    resultadoID = -1
    
    if(direccion == 'E'):      
        resultadoID = zonaDeTransporte[posicionJugador[0] + distancia][posicionJugador[1]]
    
    elif(direccion == 'O'):
        resultadoID = zonaDeTransporte[posicionJugador[0] - distancia][posicionJugador[1]]
    
    elif(direccion == 'N'):
        resultadoID = zonaDeTransporte[posicionJugador[0]][posicionJugador[1] - distancia]
    
    elif(direccion == 'S'):
        resultadoID = zonaDeTransporte[posicionJugador[0]][posicionJugador[1] + distancia]

    if(resultadoID == 'pared' or resultadoID == 0):
        resultadoID = -1

    return resultadoID

#Creamos operaciones para mover al player en las direccione de izquierda,derecha,arriba y abajo
def irALaDerecha():
    global contadorMovimiento
    global dicRegistro
    global posicionJugador
    global posicionVirus
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):

            #nos preguntamos si a la derecha nuestra no hay nada
            if zonaDeTransporte[j][i]=='jugador':
                if zonaDeTransporte[j+1][i]== 0:
                    posicionarElemento('jugador',j+1,i)
                    actualizarPosJugador(j+1,i)
                    actualizarContadorDeElectricidad(10)
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarImgPlayer('walkDer')
                    borrarElemento(j,i)
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break

                #nos preguntamos si al lado nuestro hay un virus para moverlo
                if (encontrarVirus('E', 1) != -1 and (zonaDeTransporte[j+2][i] == 0)): 
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('E', 1),j+2,i)
                    if(hayZonaProtegidaEn(j+2,i)):
                        actualizarPosVirus(encontrarVirus('E', 1),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('E', 1),j+2,i)
                        
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeElectricidad(15)
                    actualizarImgPlayer('kickDer')
                    actualizarPosJugador(j+1,i)
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break

                #nos preguntamos si al lado nuestro hay un dos virus para moverlos
                if (encontrarVirus('E', 1) != -1) and (encontrarVirus('E', 2) != -1) and (zonaDeTransporte[j+3][i] == 0):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('E', 2),j+3,i)
                    if(hayZonaProtegidaEn(j+3,i)):
                        actualizarPosVirus(encontrarVirus('E', 2),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('E', 2),j+3,i)

                    posicionarElemento(encontrarVirus('E', 1),j+2,i)
                    actualizarPosVirus(encontrarVirus('E', 1),j+2,i)
                    posicionarElemento('jugador',j+1,i)
                    actualizarPosJugador(j+1,i)                 
                    actualizarContadorDeElectricidad(200)
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
                
def irALaIzquierda():
    global contadorMovimiento
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            
            if zonaDeTransporte[j][i]=='jugador':
                if zonaDeTransporte[j-1][i] == 0:
                    posicionarElemento('jugador',j-1,i)
                    actualizarPosJugador(j-1,i)
                    actualizarContadorDeElectricidad(10)
                    borrarElemento(j,i)
                    actualizarImgPlayer('walkIzq')
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
                if (encontrarVirus('O', 1) != -1 and (zonaDeTransporte[j-2][i] == 0)):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('O', 1),j-2,i)
                    if(hayZonaProtegidaEn(j-2,i)):
                        actualizarPosVirus(encontrarVirus('O', 1),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('O', 1),j-2,i)
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeElectricidad(15)
                    actualizarImgPlayer('kickDer')
                    actualizarPosJugador(j-1,i)                    
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break

                if(encontrarVirus('O', 1) != -1) and (encontrarVirus('O', 2) != -1) and (zonaDeTransporte[j-3][i] == 0):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('O', 1),j-2,i)
                    actualizarPosVirus(encontrarVirus('O', 1),j-2,i)
                    posicionarElemento(encontrarVirus('O', 2),j-3,i)
                    if(hayZonaProtegidaEn(j-3,i)):
                        actualizarPosVirus(encontrarVirus('O', 2),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('O', 2),j-3,i)
                    
                    posicionarElemento('jugador',j-1,i)
                    actualizarPosJugador(j-1,i)                 
                    actualizarContadorDeElectricidad(200)
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
def irArriba():
    global contadorMovimiento
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            
            if zonaDeTransporte[j][i]=='jugador':              
                if zonaDeTransporte[j][i-1]==0:
                    posicionarElemento('jugador',j,i-1)
                    actualizarPosJugador(j,i-1)
                    actualizarContadorDeElectricidad(10)
                    borrarElemento(j,i)
                    actualizarImgPlayer('jump')
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
      
                if (encontrarVirus('N', 1) != -1 and (zonaDeTransporte[j][i-2] == 0)):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('N', 1),j,i-2)

                    if(hayZonaProtegidaEn(j,i-2)):
                        actualizarPosVirus(encontrarVirus('N', 1),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('N', 1),j,i-2)
                        
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeElectricidad(15)
                    actualizarImgPlayer('kickDer')
                    actualizarPosJugador(j,i-1)
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break

                if(encontrarVirus('N', 1) != -1) and (encontrarVirus('N', 2) != -1) and (zonaDeTransporte[j][i - 3] == 0):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('N', 2),j,i-3)
                    if(hayZonaProtegidaEn(j,i-3)):
                        actualizarPosVirus(encontrarVirus('N', 2),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('N', 2),j,i-3)
                        
                    posicionarElemento(encontrarVirus('N', 1),j,i-2)
                    actualizarPosVirus(encontrarVirus('N', 1),j,i-2)
                    
                    posicionarElemento('jugador',j,i-1)
                    actualizarPosJugador(j,i-1)                 
                    actualizarContadorDeElectricidad(200)
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
#lo mismo que los otros solo que el for esta cambiado por que necesitamos que el break se produzca en el eje Y
def irAbajo():
    global contadorMovimiento
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            
            if zonaDeTransporte[j][i]=='jugador':
                if zonaDeTransporte[j][i+1]== 0:
                    posicionarElemento('jugador',j,i+1)
                    actualizarPosJugador(j,i+1)
                    actualizarContadorDeElectricidad(10)
                    borrarElemento(j,i)
                    actualizarImgPlayer('down')
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
                if (encontrarVirus('S', 1) != -1 and (zonaDeTransporte[j][i+2] == 0)):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('S', 1),j,i+2)
                    
                    if(hayZonaProtegidaEn(j,i+2)):
                        actualizarPosVirus(encontrarVirus('S', 1),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('S', 1),j,i+2)
                        
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeElectricidad(15)
                    actualizarImgPlayer('kickDer')
                    actualizarPosJugador(j,i+1)
                    contadorMovimiento += 1
                    dibujarMovimiento()
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break
                
                if(encontrarVirus('S', 1) != -1) and (encontrarVirus('S', 2) != -1) and (zonaDeTransporte[j][i+3] == 0):
                    borrarElemento(j,i)
                    posicionarElemento(encontrarVirus('S', 2),j,i+3)

                    if(hayZonaProtegidaEn(j,i+3)):
                        actualizarPosVirus(encontrarVirus('S', 2),0,0) 
                    else:
                        actualizarPosVirus(encontrarVirus('S', 2),j,i+3)

                    posicionarElemento(encontrarVirus('S', 1),j,i+2)
                    actualizarPosVirus(encontrarVirus('S', 1),j,i+2)
                    
                    posicionarElemento('jugador',j,i+1)
                    actualizarPosJugador(j,i+1)                 
                    actualizarContadorDeElectricidad(200)
                    actualizarRegistro()
                    musicaSalto.play()
                    musicaSalto.set_volume(0.2)
                    break

#creamos una funcion que abra e imprima los archivos de puntaje por la terminal
def leerArchivo():
    flag = False
    recorrido = False
    y = 180
    if flag == False:
        archivoPuntuaciones = open('puntos.txt', 'r')
        flag = True
        pygame.draw.rect(pantalla,colorAzul,(100,150,950,300))
        for i, linea in enumerate(archivoPuntuaciones):
            if recorrido == False:
                recorrido == True
                puntos = tipografiaDatos.render(str(i) + ': ' + str(linea), False, colorBlanco)        
                pantalla.blit(puntos,(150, y))
                pygame.display.update()
                y += 20
                time.sleep(0.6)  
    archivoPuntuaciones.close()
        
#una funcion que pida nuestro nombres y guarde el mismo con los puntajes en un archivo
def modArchivo():
    global puntaje
    global minuto
    global segundos
    global energia
    archivoPuntuaciones = open('puntos.txt', 'a')
    flag = False 
    if flag == False:
        flag = True
        nombre = raw_input('ingrese el nombre por favor: ')
        textoPuntos = archivoPuntuaciones.write('\n' + nombre + ' puntos: ' + str(puntaje) + ' bateria: ' + str(energia) + ' tiempo transcurrido ' + str((minutos * 60) + segundos))        
        archivoPuntuaciones.close()
        print('Puntaje guardado correctamente')
        print('los puntajes se guardan en el archivo puntajes.txt')
        
#una clase que crea un objeto cursor con un rectangulo en su posicion
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,0,0)
    def update(self):
        self.left,self.top = pygame.mouse.get_pos()
        
#una clase que crea un objeto boton el #terminar
class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1, imagen2, x, y):
        self.boton_normal = imagen1
        self.boton_selec = imagen2
        self.boton_actual = imagen1
        self.rect = self.boton_actual.get_rect()
        self.rect.left,self.rect.top = (x,y)
    def update(self,pantalla,cursor,mensaje):
        if cursor.colliderect(self.rect):
            self.boton_actual = self.boton_selec
            textoMenu = tipografiaDatos.render(mensaje, False, colorBlanco)
            pantalla.blit(textoMenu,(430,600,0,0))
        else:
            self.boton_actual = self.boton_normal
        pantalla.blit(self.boton_actual,self.rect)

#creamos el menu con sus textos y botones
def menu():
    menuActivado = True
    #decidimos hacer que cada imagen del boton tenga integrado su texto
    img_jugar = pygame.image.load('botones/boton_play.png')
    img_jugarSelec = pygame.image.load('botones/boton_playSelec.png')
    img_salir = pygame.image.load('botones/boton_quit.png')
    img_salirSelec = pygame.image.load('botones/boton_quitSelec.png')
    img_puntaje = pygame.image.load('botones/boton_puntaje.png')
    img_puntajeSelec = pygame.image.load('botones/boton_puntajeSelec.png')
    fondo = pygame.image.load('imagenes/fondoMenu.jpg')
    
    
    #creamos los botones utilizando la funcion 'Boton'
    botonJugar = Boton(img_jugar,img_jugarSelec, 400, 350)
    botonSalir = Boton(img_salir,img_salirSelec, 600,350)
    botonPuntaje = Boton(img_puntaje,img_puntajeSelec, 500, 450)

    cursor1 = Cursor()
    reloj = pygame.time.Clock()

    textoMenu = tipografiaMenu.render('CiberAtaque', False, colorBlanco)

    x = 330
    y = 100

    while menuActivado == True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #Al tocar el boton Jugar inicia el propio juego   
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if cursor1.colliderect(botonJugar.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    menuActivado = False
                    pantalla.fill(colorNegro)
                    dibujarTodo()
                    loopJuego(salirJuego)
                    
                #Al tocar el boton salir se cierra el juego     
                elif cursor1.colliderect(botonSalir.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    menuActivado = False
                    pygame.quit()
                    quit()

                #Al tocar el boton puntaje se abre un menu donde podemos ver nuestros puntajes      
                elif cursor1.colliderect(botonPuntaje.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    menuActivado = False
                    pantalla.fill(colorNegro)
                    menuPuntaje()
                    
        reloj.tick(20)
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(textoMenu,(x,y,0,0))
        cursor1.update()
        botonJugar.update(pantalla,cursor1,'')
        botonSalir.update(pantalla,cursor1,'')
        botonPuntaje.update(pantalla,cursor1,'')
        pygame.display.update()

#creamos un menu para que el juego pueda ser pausado
def menuPausa():
    global detenerJuego
    enPausa = True
    detenerJuego = True
    pygame.mixer.music.stop()
    img_jugar = pygame.image.load('botones/boton_play.png')
    img_jugarSelec = pygame.image.load('botones/boton_playSelec.png')
    img_salir = pygame.image.load('botones/boton_quit.png')
    img_salirSelec = pygame.image.load('botones/boton_quitSelec.png')
    
    botonJugar = Boton(img_jugar,img_jugarSelec, 400, 350)
    botonSalir = Boton(img_salir,img_salirSelec, 600,350)

    cursor1 = Cursor()
    reloj = pygame.time.Clock()

    textoMenuPausa = tipografiaMenu.render('Pausa', False, colorNegro)

    x = 470
    y = 200

    while enPausa:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(botonJugar.rect):
                    enPausa = False
                    
                elif cursor1.colliderect(botonSalir.rect):
                    enPausa = False
                    menuGameOver()

        reloj.tick(20)
        pantalla.fill(colorBlanco)
        pantalla.blit(textoMenuPausa,(x,y,0,0))
        cursor1.update()
        botonJugar.update(pantalla,cursor1,'')
        botonSalir.update(pantalla,cursor1,'')
        if enPausa == False:
            dibujarTodo()
            detenerJuego = True
        pygame.display.update()

#menu donde el usuario puede ver los diferentes puntajes que fue guardando 
def menuPuntaje():
    enPausa = True
    pygame.mixer.music.stop()
    
    cursor1 = Cursor()
    reloj = pygame.time.Clock()
    

    textoPuntaje = tipografiaMenu.render('Puntajes' , False, colorBlanco)
    textoVolver = tipografiaDatos.render('Para volver atras podes usar el boton ESC, apretar cuando se termine de mostrar todo(hasta 10)', False, colorBlanco)
    
    x = 455
    y = 30

    while enPausa:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enPausa = False
                    menu()     

        reloj.tick(20)
        pantalla.fill(colorNegro)
        pantalla.blit(textoPuntaje,(x,y,0,0))
        pantalla.blit(textoVolver,(x-250,y+500,0,0))
        leerArchivo()
        cursor1.update()
        pygame.display.update()

#Menu donde nos permite guardar nuestros puntos, ver la repeticion de nuestra partida e volver a jugar
def menuGanaste():
    enMenuGanaste= True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('musica/musicaVictoria.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    img_volverJugar = pygame.image.load('botones/boton_play.png')
    img_volverJugarSelec = pygame.image.load('botones/boton_playSelec.png')
    img_puntaje = pygame.image.load('botones/boton_puntajeGO.png')
    img_puntajeSelec = pygame.image.load('botones/boton_puntajeGOSelec.png')
    img_repeticion = pygame.image.load('botones/boton_repeticion.png')
    img_repeticionSelec = pygame.image.load('botones/boton_repeticionSelec.png')
    
    botonVolverJugar = Boton(img_volverJugar,img_volverJugarSelec, 400, 350)
    botonPuntaje = Boton(img_puntaje,img_puntajeSelec,600,350)
    botonRepetirJuego = Boton(img_repeticion,img_repeticionSelec, 500, 450)
    
    cursor1 = Cursor()
    reloj = pygame.time.Clock()
    
    textoMenuGO = tipografiaMenu.render('Ganaste bien hecho', False, colorNegro)

    x = 280
    y = 100

    while enMenuGanaste:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(botonVolverJugar.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    menu()
                    enMenuGanaste = False
                    
                if cursor1.colliderect(botonPuntaje.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    modArchivo()
                    menuGanaste()

                if cursor1.colliderect(botonRepetirJuego.rect):
                    pygame.mixer.music.load('musica/sonidoBoton.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    time.sleep(0.4)
                    repetirJuegoFinal()
                    enMenuGanaste = False
    
        reloj.tick(20)
        pantalla.fill(colorBlanco)
        pantalla.blit(textoMenuGO,(x,y,0,0))
        cursor1.update()
        botonVolverJugar.update(pantalla, cursor1,'')
        botonPuntaje.update(pantalla, cursor1,'')
        botonRepetirJuego.update(pantalla, cursor1,'')
        pygame.display.update()
    
#seteamos el tiempo como al inicio del juego
def resetearTiempo():
    global tiempoInicial
    global tiempoReinicio
    tiempoReinicio = pygame.time.get_ticks() - tiempoInicial

#seteamos los puntos como al inicio del juego
def resetearPuntos():
    global puntos
    puntos = 0

#seteamos la energia como al inicio del juego
def resetearEnergia():
    global energia
    energia = 7000
    actualizarContadorDeElectricidad(0)

#seteamos la cantidad de movimientos como al inicio del juego
def resetearContMovimientos():
    global contadorMovimiento
    contadorMovimiento = 0
    dibujarMovimiento()

#seteamos el juego como al inicio
def resetearJuego():
    global posicionVirus
    global posicionJugador
    global lstZonasProtegidas

    borrarElemento(posicionJugador[0], posicionJugador[1])

    for virus in posicionVirus:
        borrarElemento(virus[0], virus[1])
    
    zonaDeTransporte[2][5] = 'jugador'
    zonaDeTransporte[3][5] = 'virus1'
    zonaDeTransporte[4][5] = 'virus2'
    zonaDeTransporte[5][5] = 'virus3'
    zonaDeTransporte[6][5] = 'virus4'
    zonaDeTransporte[5][6] = 'virus5'
    lstZonasProtegidas = [(2,4),(2,6),(7,4),(7,6),(4,6)]
    
    resetearTiempo()
    resetearPuntos()
    resetearEnergia()
    resetearContMovimientos()

#Mostramos el tiempo transcurrido de la partida para el usuario
def mostrarTiempo():
    global tiempoInicial
    global minutos
    global segundos
    global tiempoReinicio
    tiempoActual = pygame.time.get_ticks() - tiempoInicial - tiempoReinicio
    segundos = (tiempoActual/ 1000) % 60
    minutos = (tiempoActual/ 1000) / 60
    pygame.draw.rect(pantalla,colorAzul,(650,500,510,30))
    contadorTiempo = tipografiaDatos.render('tiempo transcurrido: ' + str(minutos) +' minutos' + ' '+ str(segundos) + ' segundos', False, colorBlanco)
    pantalla.blit(contadorTiempo,(655,500))
    pygame.display.update()

#En esta funcion modificamos el diccionario donde se guardan las posiciones anteriores del jugador, virus, bateria y cant de movimientos 
def actualizarRegistro():
    global dicRegistro
    global posicionJugador
    global posicionVirus
    global energia
    global contadorMovimiento

    #guardamos los determinados datos que pide la key del diccionario
    dicRegistro['posPlayer'].append(posicionJugador)
    dicRepetirJuego['posPlayer'].append(posicionJugador)
    
    dicRegistro['posVirus1'].append(posicionVirus[0])
    dicRepetirJuego['posVirus1'].append(posicionVirus[0])
    
    dicRegistro['posVirus2'].append(posicionVirus[1])
    dicRepetirJuego['posVirus2'].append(posicionVirus[1])
    
    dicRegistro['posVirus3'].append(posicionVirus[2])
    dicRepetirJuego['posVirus3'].append(posicionVirus[2])
    
    dicRegistro['posVirus4'].append(posicionVirus[3])
    dicRepetirJuego['posVirus4'].append(posicionVirus[3])
    
    dicRegistro['posVirus5'].append(posicionVirus[4])
    dicRepetirJuego['posVirus5'].append(posicionVirus[4])
    
    dicRegistro['bateria'].append(energia)
    dicRepetirJuego['bateria'].append(energia)
    
    dicRegistro['movimientos'].append(contadorMovimiento)
    dicRepetirJuego['movimientos'].append(contadorMovimiento)

#Mecanica nueva la cual permite que el player, la bateria, la cantidad de pasos y los virus vuelven un momento hacia atras    
def retrocederTiempo():
    global dicRegistro
    global posicionJugador
    global posicionVirus
    global energia
    global contadorMovimiento
    global lstZonasProtegidas

    #vuelve en el tiempo el player, los movimientos y la bateria
    if len(dicRegistro['posPlayer']) > 1 and len(dicRegistro['bateria']) > 1 and len(dicRegistro['movimientos']) > 1:
        borrarElemento(posicionJugador[0],posicionJugador[1])
        dicRegistro['posPlayer'].pop()
        dicRegistro['movimientos'].pop()
        dicRegistro['bateria'].pop()
        posicionJugador = dicRegistro['posPlayer'][len(dicRegistro['posPlayer']) - 1]
        contadorMovimiento = dicRegistro['movimientos'][len(dicRegistro['movimientos']) - 1]
        energia = dicRegistro['bateria'][len(dicRegistro['bateria']) - 1]
        posicionarElemento('jugador', posicionJugador[0], posicionJugador[1])
        dibujarMovimiento()
        actualizarContadorDeElectricidad(0)
    
    #vuelve ene el tiempo el virus        
    if len(dicRegistro['posVirus1']) > 1:
        virus1Pos = dicRegistro['posVirus1'][len(dicRegistro['posVirus1'])-1]
        borrarElemento(virus1Pos[0],virus1Pos[1])
        dicRegistro['posVirus1'].pop()
        posicionVirus[0] = dicRegistro['posVirus1'][len(dicRegistro['posVirus1']) - 1]
        posicionarElemento('virus1', posicionVirus[0][0],posicionVirus[0][1])
        
    if len(dicRegistro['posVirus2']) > 1:
        virus2Pos = dicRegistro['posVirus2'][len(dicRegistro['posVirus2'])-1]
        borrarElemento(virus2Pos[0],virus2Pos[1])
        dicRegistro['posVirus2'].pop()
        posicionVirus[1] = dicRegistro['posVirus2'][len(dicRegistro['posVirus2']) - 1]
        posicionarElemento('virus2', posicionVirus[1][0],posicionVirus[1][1])

    if len(dicRegistro['posVirus3']) > 1:
        virus3Pos = dicRegistro['posVirus3'][len(dicRegistro['posVirus3'])-1]
        borrarElemento(virus3Pos[0],virus3Pos[1])
        dicRegistro['posVirus3'].pop()
        posicionVirus[2] = dicRegistro['posVirus3'][len(dicRegistro['posVirus3']) - 1]
        posicionarElemento('virus3', posicionVirus[2][0],posicionVirus[2][1])
    
    if len(dicRegistro['posVirus4']) > 1:
        virus4Pos = dicRegistro['posVirus4'][len(dicRegistro['posVirus4'])-1]
        borrarElemento(virus4Pos[0],virus4Pos[1])
        dicRegistro['posVirus4'].pop()
        posicionVirus[3] = dicRegistro['posVirus4'][len(dicRegistro['posVirus4']) - 1]
        posicionarElemento('virus4', posicionVirus[3][0],posicionVirus[3][1])

    if len(dicRegistro['posVirus5']) > 1:
        virus5Pos = dicRegistro['posVirus5'][len(dicRegistro['posVirus5'])-1]
        borrarElemento(virus5Pos[0],virus5Pos[1])
        dicRegistro['posVirus5'].pop()
        posicionVirus[4] = dicRegistro['posVirus5'][len(dicRegistro['posVirus5']) - 1]
        posicionarElemento('virus5', posicionVirus[4][0],posicionVirus[4][1])

    #En caso que se haya borrado una zona protegida la volvemos a poner
    if(lstZonasEliminadas[len(dicRegistro['posPlayer'])] != 'ninguna'):
        lstZonasProtegidas.append(lstZonasEliminadas[len(dicRegistro['posPlayer'])])
        lstZonasEliminadas.pop()
    
#Mecanica nueva la cual permite ver toda nuestra partida completa
def repetirJuegoFinal():
    global dicRepetirJuego
    global posicionJugador
    global posicionVirus
    global energia
    global contadorMovimiento
    global repitiendoJuego
    global lstZonasProtegidas
    lstZonasProtegidas = [(2,4),(2,6),(7,4),(7,6),(4,6)]
    flagMenu = True
    
    resetearTiempo()
    dibujarFondo()
    
    while flagMenu == True:
        if len(dicRepetirJuego['posPlayer']) > 0:
            borrarElemento(posicionJugador[0],posicionJugador[1])
            if repitiendoJuego == True:
                #damos vuelta la lista ya que necesitamos literlmente lo contrario a retroceder al nivel de diccionario
                dicRepetirJuego['posPlayer'].reverse()
                dicRepetirJuego['bateria'].reverse()
                dicRepetirJuego['movimientos'].reverse()

                #ponemos todos las cosas a como estan al comiendo, pero sin perder los datos de la partida
                borrarElemento(dicRepetirJuego['posVirus1'][len(dicRepetirJuego['posVirus1'])-1][0],dicRepetirJuego['posVirus1'][len(dicRepetirJuego['posVirus1'])-1][1])    
                borrarElemento(dicRepetirJuego['posVirus2'][len(dicRepetirJuego['posVirus2'])-1][0],dicRepetirJuego['posVirus2'][len(dicRepetirJuego['posVirus2'])-1][1])
                borrarElemento(dicRepetirJuego['posVirus3'][len(dicRepetirJuego['posVirus3'])-1][0],dicRepetirJuego['posVirus3'][len(dicRepetirJuego['posVirus3'])-1][1])    
                borrarElemento(dicRepetirJuego['posVirus4'][len(dicRepetirJuego['posVirus4'])-1][0],dicRepetirJuego['posVirus4'][len(dicRepetirJuego['posVirus4'])-1][1])
                borrarElemento(dicRepetirJuego['posVirus5'][len(dicRepetirJuego['posVirus5'])-1][0],dicRepetirJuego['posVirus5'][len(dicRepetirJuego['posVirus5'])-1][1])

                dicRepetirJuego['posVirus1'].reverse()
                dicRepetirJuego['posVirus2'].reverse()
                dicRepetirJuego['posVirus3'].reverse()
                dicRepetirJuego['posVirus4'].reverse()
                dicRepetirJuego['posVirus5'].reverse()

                posicionVirus[0] = dicRepetirJuego['posVirus1'][len(dicRepetirJuego['posVirus1']) - 1]
                posicionarElemento('virus1', posicionVirus[0][0],posicionVirus[0][1])

                posicionVirus[1] = dicRepetirJuego['posVirus2'][len(dicRepetirJuego['posVirus2']) - 1]
                posicionarElemento('virus2', posicionVirus[1][0],posicionVirus[1][1])

                posicionVirus[2] = dicRepetirJuego['posVirus3'][len(dicRepetirJuego['posVirus3']) - 1]
                posicionarElemento('virus3', posicionVirus[2][0],posicionVirus[2][1])

                posicionVirus[3] = dicRepetirJuego['posVirus4'][len(dicRepetirJuego['posVirus4']) - 1]
                posicionarElemento('virus2', posicionVirus[3][0],posicionVirus[3][1])

                posicionVirus[4] = dicRepetirJuego['posVirus5'][len(dicRepetirJuego['posVirus5']) - 1]
                posicionarElemento('virus2', posicionVirus[4][0],posicionVirus[4][1])

                pygame.mixer.music.load('musica/musicaJugando.mp3')
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(0.1)
                
                dibujarZonaDeTransporte()
                repitiendoJuego = False

            posicionJugador = dicRepetirJuego['posPlayer'][len(dicRepetirJuego['posPlayer']) - 1]
            posicionarElemento('jugador', posicionJugador[0], posicionJugador[1])
            dibujarZonaDeTransporte()
            
            energia = dicRepetirJuego['bateria'][len(dicRepetirJuego['bateria']) - 1]
            actualizarContadorDeElectricidad(0)
            
            contadorMovimiento = dicRepetirJuego['movimientos'][len(dicRepetirJuego['movimientos']) - 1]
            dibujarMovimiento()
            
            dicRepetirJuego['posPlayer'].pop()
            dicRepetirJuego['bateria'].pop()
            dicRepetirJuego['movimientos'].pop()

            #posicionamos el player a sus determinadas cordenadas 
            if len(dicRepetirJuego['posVirus1']) > 1:
                virus1Pos = dicRepetirJuego['posVirus1'][len(dicRepetirJuego['posVirus1'])-1]
                borrarElemento(virus1Pos[0],virus1Pos[1])
                dicRepetirJuego['posVirus1'].pop()
                posicionVirus[0] = dicRepetirJuego['posVirus1'][len(dicRepetirJuego['posVirus1']) - 1]
                posicionarElemento('virus1', posicionVirus[0][0],posicionVirus[0][1])

            #posicionamos los virus a sus determinadas cordenadas 
            if len(dicRepetirJuego['posVirus2']) > 1:
                virus2Pos = dicRepetirJuego['posVirus2'][len(dicRepetirJuego['posVirus2'])-1]
                borrarElemento(virus2Pos[0],virus2Pos[1])
                dicRepetirJuego['posVirus2'].pop()
                posicionVirus[1] = dicRepetirJuego['posVirus2'][len(dicRepetirJuego['posVirus2']) - 1]
                posicionarElemento('virus2', posicionVirus[1][0],posicionVirus[1][1])

            if len(dicRepetirJuego['posVirus3']) > 1:
                virus3Pos = dicRepetirJuego['posVirus3'][len(dicRepetirJuego['posVirus3'])-1]
                borrarElemento(virus3Pos[0],virus3Pos[1])
                dicRepetirJuego['posVirus3'].pop()
                posicionVirus[2] = dicRepetirJuego['posVirus3'][len(dicRepetirJuego['posVirus3']) - 1]
                posicionarElemento('virus3', posicionVirus[2][0],posicionVirus[2][1])

            if len(dicRepetirJuego['posVirus4']) > 1:
                virus4Pos = dicRepetirJuego['posVirus4'][len(dicRepetirJuego['posVirus4'])-1]
                borrarElemento(virus4Pos[0],virus4Pos[1])
                dicRepetirJuego['posVirus4'].pop()
                posicionVirus[3] = dicRepetirJuego['posVirus4'][len(dicRepetirJuego['posVirus4']) - 1]
                posicionarElemento('virus4', posicionVirus[3][0],posicionVirus[3][1])

            if len(dicRepetirJuego['posVirus5']) > 1:
                virus5Pos = dicRepetirJuego['posVirus5'][len(dicRepetirJuego['posVirus5'])-1]
                borrarElemento(virus5Pos[0],virus5Pos[1])
                dicRepetirJuego['posVirus5'].pop()
                posicionVirus[4] = dicRepetirJuego['posVirus5'][len(dicRepetirJuego['posVirus5']) - 1]
                posicionarElemento('virus5', posicionVirus[4][0],posicionVirus[4][1])
                
            textoMenuGO = tipografiaMenu.render('Repeticion', False, colorNegro)
            pantalla.blit(textoMenuGO,(200,100,0,0))
            estaSolucionado()
            time.sleep(0.3)
            #hacemos que sea una funcion recursiva para que parezca como una animacion aparte de ser autonoma
            repetirJuegoFinal()
        flagMenu = False
        
    time.sleep(1.3)
    pygame.mixer.music.stop()
    menu()

#Creamos el loop del juego
def loopJuego(salirJuego):
    global posicionJugador
    global actualizarPosVirus
    global tiempoInicial
    global detenerJuego
    menuActivado = True
    global musicaSalto
    if detenerJuego == False:
        while not salirJuego:
            if(menuActivado):
                tiempoInicial = pygame.time.get_ticks()
                menuActivado = False
            mostrarTiempo()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salirJuego = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        irALaDerecha()
                        lstZonasEliminadas.append('ninguna')
                    elif event.key == pygame.K_LEFT:
                        irALaIzquierda()
                        lstZonasEliminadas.append('ninguna')
                    elif event.key == pygame.K_UP:
                        irArriba()
                        lstZonasEliminadas.append('ninguna')
                    elif event.key == pygame.K_DOWN:
                        irAbajo()
                        lstZonasEliminadas.append('ninguna')
                    if event.key == pygame.K_ESCAPE:
                        menuPausa()
                    if event.key == pygame.K_r:
                        resetearJuego()
                    if event.key == pygame.K_x:
                        retrocederTiempo()
                dibujarZonaDeTransporte()
                estaSolucionado() 

menu()
pygame.quit()
quit()
