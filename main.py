#pgzero

""" NOTA 1: El código de este proyecto está publicado en el repo:
            > https://github.com/rodrigovittori/Alien-Atleta-4499/
    
    NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
            pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
            y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  
    
---------------------------------------------------------------------------------------------------

    [M7.L1] - Actividad Nº 5: "Puntuación"
    Objetivo: Implementar un sistema de puntuación que registre la cant. de enemigos esquivados

    Nota: El ejercicio 4 ya estaba resuelto.
    Nota 2: Podríamos implementar un aumento progresivo de la velocidad de nuestros enemigos

    Paso Nº 1) Creamos una variable (global) que almacene nuestra puntuación
    Paso Nº 2) Modifico el draw() para que muestre la puntuación
                > NOTA: También cambia en modo "game over"
    Paso Nº 3) Modifico el reset para que reinicie nuestra puntuación
                > NOTA: recordar declararla como global en update
    Paso Nº 4) Aumentaremos la puntuación cada vez que un enemigo haya abandonado la pantalla

---------------------------------------------------------------------------------------------------

NOTA: Recuerden que tenemos un bug ya que nuestro PJ puede saltar mientras sigue en el aire. """

WIDTH = 600   # Ancho de la ventana (en px)
HEIGHT = 300  # Alto de la ventana (en px)

TITLE = "Juego del Alien Atleta y sus piruetas" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

game_over = False    # Vble que registra si nuestra partida ha finalizado o no
puntuacion = 0       # Cantidad de enemigos esquivados

fondo = Actor("background")           # Nuestro fondo NO tiene posición porque queremos que ocupe TODA la pantalla
cartel_game_over = Actor("GO")        # Splash Screen de Game Over

""" > Vamos a crear nuestro personaje :D """
personaje = Actor("alien", (50, 240)) # Nuestro personaje SI la tiene, las coordenadas se registran en pos(x, y)
personaje.velocidad = 5               # velocidad (en px) a la que avanza el personaje por cada frame
personaje.COOLDOWN_SALTO = 0.9        # tiempo de recarga habilidad salto (en segundos)
personaje.timer_salto = 0             # tiempo que debe pasar (en segundos) antes de que nuestro personaje pueda saltar nuevamente
personaje.altura_salto = int(personaje.height * 1.6) # El personaje saltará 1.6 veces su altura

""" Nota: Para evitar que al agacharse se anule la animación de salto DEBERÍAMOS implementar un check para prevenirlo """
personaje.timer_agachado = 0.0        # Tiempo restante (en segundos) antes de poner de pie al personaje
personaje.esta_agachado = False       # Valor que controla si debemos permanecer agachados o no

personaje.posInicial = personaje.pos
personaje.vidas_restantes = 3         # Cantidad de colisiones contra obstáculos/enemigos permitidas
personaje.COOLDOWN_DANIO = 0.6        # tiempo que debe pasar (en segundos) antes de que nuestro personaje vuelva a tomar daño 
personaje.timer_invulnerabilidad = 0  # tiempo hasta que se acabe el efecto de invulnerabilidad 

caja =  Actor("box", (WIDTH - 50 , 265))
abeja = Actor("bee", (WIDTH + 200, 150))

def draw(): # draw() como su nombre lo indica es el método de pgzero que dibuja objetos en pantalla
    if (game_over):
        # Si bien en este caso el cartel de Game Over cubre TODA la pantalla, 
        # sería mejor solamente agregar el texto "GAME OVER" y dibujar el fondo
        fondo.draw() 
        cartel_game_over.draw()
        # Nota: modificamos la altura del otro mensaje para mostrar más info:
        screen.draw.text(("Enemigos esquivados: " + str(puntuacion)), center= (int(WIDTH/2), 2* int(HEIGHT/3)), color = "yellow", fontsize = 24)
        screen.draw.text("Presiona [Enter] para reiniciar", center= (int(WIDTH/2), 4* int(HEIGHT/5)), color = "white", fontsize = 32)

    else:
        fondo.draw()
        personaje.draw()
        caja.draw()
        abeja.draw()
        
        # Indicador de salto:
        if (personaje.timer_salto <= 0):
            screen.draw.text("¡LISTO!", midleft=(20,20), color = (0, 255, 0), fontsize=24)
        else:
            screen.draw.text(str(personaje.timer_salto), midleft=(20,20), color = "red", fontsize=24)    
        
        screen.draw.rect(personaje.collidebox, (255, 0, 255)) # Dibujamos collidebox del PJ
        # INDICADOR DE POS DEL PJ EN EJE X: # screen.draw.text(("X= " + str(personaje.x)), (30,30), background="white", color="black", fontsize=24)
        screen.draw.rect(caja.collidebox, (255, 0, 0)) # Dibujamos collidebox de la caja
        screen.draw.rect(abeja.collidebox, (255, 0, 0)) # Dibujamos collidebox de la abeja

        """ Indicador vidas restantes """
        for v in range(personaje.vidas_restantes):
            screen.draw.filled_circle( ( (WIDTH - (20 + 30 * v)), (50) ), 10, (0, 0, 255) )
        screen.draw.text("VIDAS RESTANTES: ", midright=((WIDTH - 100), 50), color = "blue", background = "white", fontsize=24) 

        # Indicador puntuación
        screen.draw.text(("Enemigos esquivados: " + str(puntuacion)), midright=(WIDTH-20, 20), color ="black", background="white", fontsize=24)


def update(dt): # update(dt) es el bucle ppal de nuestro juego, dt significa delta time (tiempo en segundos entre cada frame)
    # > https://pygame-zero.readthedocs.io/en/stable/hooks.html#update
    # Podemos traducir "update" como "actualizar", es decir, en ella contendremos el código que produzca cambios en nuestro juego

    global game_over, puntuacion

    if (game_over):
        # En caso de game over
        if (keyboard.enter):
            """ >> Reiniciar el juego << """ # Nota: migrar a función
            game_over = False
            puntuacion = 0
            # Reseteamos personaje
            personaje.pos = personaje.posInicial
            personaje.vidas_restantes = 3
            personaje.timer_invulnerabilidad = 0
            personaje.timer_salto = 0
            personaje.timer_agachado = 0.0
            personaje.esta_agachado = False
            personaje.velocidad = 5
            nva_imagen = "alien"

            # Nota: Si hacemos que la velocidad de los enemigos escale con el tiempo, la reseteamos
            # Reseteamos caja
            caja.pos = (WIDTH - 50, 265)
            caja.angle = 0
            # Reseteamos abeja
            abeja.pos = (WIDTH + 200, 150)

    else:
        """   #######################
             # CAMBIOS AUTOMATICOS #
            #######################   """

        personaje.timer_invulnerabilidad -= dt   # restamos al timer de invulnerabilidad depués de tomar daño
        personaje.timer_salto -= dt              # restamos al timer del cooldown de salto del persoanje el tiempo desde el último frame
    
        personaje.timer_agachado -= dt           # restamos al timer para resetar la altura del persoanje el tiempo desde el último frame
    
        if ((personaje.timer_agachado <= 0) and (personaje.esta_agachado)):
            personaje.y = personaje.posInicial[1]   # Reseteamos la altura del PJ 
            personaje.esta_agachado = False         # Indicamos que el PJ ya NO está agachado
    
        personaje.collidebox = Rect((personaje.x - int(personaje.width / 2), personaje.y - int(personaje.height / 2)), (personaje.width, personaje.height))
    
        nva_imagen = "alien"        # variable local que almacena el próximo sprite a renderizar
                                    # "alien": quieto / "left": mov. izq. / "right" : mov. dcha.
        
        """   ################
             # LEER TECLADO #
            ################   """
    
        # Movimiento del personaje:
        if ( (keyboard.right or keyboard.d) and ( personaje.x < ( WIDTH - int(personaje.width / 2) ) ) and (not personaje.esta_agachado) ):
            personaje.x += personaje.velocidad
            nva_imagen = "right"
    
        if ( (keyboard.left or keyboard.a) and ( personaje.x > int(personaje.width / 2) ) and (not personaje.esta_agachado) ):
            personaje.x -= personaje.velocidad
            nva_imagen = "left"
    
        # Salto: lo implementamos en OnKeyDown(key)
    
        if (keyboard.down or keyboard.s):
            personaje.y = 260    # Bajamos el pj
            nva_imagen = "duck"
            personaje.timer_agachado = 0.1 # tiempo que nuestro PJ seguirá agachado DESPUÉS de soltar la tecla
            personaje.esta_agachado = True
    
        """  ########################
            # COMPROBAR COLISIONES #
           ########################   """
    
        # Nota: migrar a función comprobar_colisiones()
    
        if ( personaje.colliderect(caja) or personaje.colliderect(abeja) ):
            nva_imagen = "hurt" # Cambiamos el sprite a "hurt"
            
            if (personaje.timer_invulnerabilidad <= 0):
                personaje.vidas_restantes -= 1   # resto un intento
                personaje.timer_invulnerabilidad = personaje.COOLDOWN_DANIO # Activo invulnerabilidad
            
            if (personaje.vidas_restantes <= 0):
                game_over = True
    
        ###################################################################################
    
        """  ####################
            # MOVER OBSTÁCULOS #
           ####################   """
        
        # Mover la caja - NOTA/TO-DO: Migrar a una función
    
        caja.collidebox = Rect((caja.x - int(caja.width / 2), caja.y - int(caja.height / 2)), (caja.width, caja.height))
        
        if (caja.x < 0):     # Si la caja salió de la ventana de juego...
            caja.x += WIDTH  # La llevamos a la otra punta de la pantalla
            puntuacion += 1  # Aumento en 1 el contador de enemigos esquivados
        else:
            # Si todavía no se escapa de la ventana...
            caja.x -= 5      # mover la caja 5 px a la izquierda en cada frame
        
        caja.angle = (caja.angle % 360) + 5  # rotamos la caja 5 grados cada frame
    
        """ ########################################################################### """
        
        # Mover la abeja - NOTA/TO-DO: Migrar a una función
    
        abeja.collidebox = Rect((abeja.x - int(abeja.width / 2), abeja.y - int(abeja.height / 2)), (abeja.width, abeja.height))
    
        # NOTA: La abeja DEBERÍA tener un movimiento más complejo (creo que es una tarea adicional) con un patrón zigzagueante
        
        if (abeja.x < 0):       # Si la caja salió de la ventana de juego...
            abeja.x += WIDTH    # La llevamos a la otra punta de la pantalla
            puntuacion += 1     # Aumento en 1 el contador de enemigos esquivados
        else:
            # Si todavía no se escapa de la ventana...
            abeja.x -= 5     # mover la caja 5 px a la izquierda en cada frame
    
        ###################################################################################
        """ POST INPUT """
        personaje.image = nva_imagen # Actualizamos el sprite del personaje

def on_key_down(key): # Este método se activa al presionar una tecla
    # https://pygame-zero.readthedocs.io/en/stable/hooks.html?highlight=on_key_down#on_key_down

    if (not game_over):
        
        if (
             (keyboard.space or keyboard.w or keyboard.up) and   # Parte 1 de la cond: presionar tecla
             (personaje.timer_salto <= 0)                  and   # Parte 2 de la cond: timer listo
             (personaje.y > int(personaje.height / 2))     and   # Parte 3 de la cond: el PJ NO ha salido de la pantalla
             (not personaje.esta_agachado)                       # Parte 3 de la cond: el PJ NO está agachado
           ):
            
            personaje.timer_salto = personaje.COOLDOWN_SALTO                 # Reseteamos cooldown
            #personaje.y -= personaje.altura_salto                           # El PJ "salta" (cambiamos su altura)
            #animate(personaje, tween="bounce_end", duration = 2, y = 240)   # Activamos la animación de caída
    
            temp_anim = animate(personaje, tween="decelerate", duration = (personaje.COOLDOWN_SALTO / 2), y = (personaje.y - personaje.altura_salto))   
            temp_anim.on_finished = bajarAlien

def bajarAlien():
    animate(personaje, tween="accelerate", duration = (personaje.COOLDOWN_SALTO / 2), y = personaje.posInicial[1])   # BAJAR ALIEN