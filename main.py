#pgzero

""" NOTA 1: El código de este proyecto está publicado en el repo:
            > https://github.com/rodrigovittori/Alien-Atleta-4499/
    
    NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
            pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
            y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  
    
---------------------------------------------------------------------------------------------------

    [M6.L4] - Actividad Nº 7: "Cambiando Sprites"
    Objetivo: Agregar la lógica necesaria para que el sprite del personaje cambie según las acciones del jugador

    NOTA: La Actividad Nº 6 se resuelve con el código de la Actividad Nº 5

    Paso Nº 1) Crear una variable local en update() para almacenar la imágen que vamos a asignar al actor en cada frame.
                NOTA: Ésta actividad normalmente se resuelve mediante el uso de una variable global, pero el
                      grupo ha decidido controlar los cambios DIRECTAMENTE desde el atributo .image de Actor()

                > https://pygame-zero.readthedocs.io/en/stable/builtins.html#actors
                      
    Paso Nº 2) Agregamos en las condiciones de movimiento un cambio de valor de nva_imagen
    Paso Nº 3) Post-input actualizamos el sprite del personaje para que sea la imágen almacenada en nuestra variable

---------------------------------------------------------------------------------------------------

NOTA: Les quedan las actividades adicionales y tenemos un bug ya que nuestro PJ puede saltar mientras
      sigue en el aire. Nos vemos la próxima semana :D    """

WIDTH = 600   # Ancho de la ventana (en px)
HEIGHT = 300  # Alto de la ventana (en px)

TITLE = "Juego del Alien Atleta y sus piruetas" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

""" > Vamos a crear nuestro personaje :D """
fondo = Actor("background")           # Nuestro fondo NO tiene posición porque queremos que ocupe TODA la pantalla
personaje = Actor("alien", (50, 240)) # Nuestro personaje SI la tiene, las coordenadas se registran en pos(x, y)
personaje.velocidad = 5               # velocidad (en px) a la que avanza el personaje por cada frame

personaje.COOLDOWN_SALTO = 0.7        # tiempo de recarga habilidad salto (en segundos)
personaje.timer_salto = 0             # tiempo que debe pasar (en segundos) antes de que nuestro personaje pueda saltar nuevamente
personaje.altura_salto = int(personaje.height * 1.6) # El personaje saltará 1.6 veces su altura

""" Nota: Si quisieramos facilitar la tarea de "reiniciar"/"resetear"
          la posición del personaje o los obstáculos/enemigos a su estado
          inicial, podemos hacerlo de la siguiente manera:

    Paso 1) Creamos un atributo del actor donde registramos su posición inicial:

            personaje.posInicial = personaje.pos # almacenamos la posición inicial

    Paso 2) Cuando querramos resetear la posición, usaremos:

            personaje.pos = personaje.posInicial
"""
personaje.posInicial = personaje.pos

caja = Actor("box", (WIDTH - 50, 265))

def draw(): # draw() como su nombre lo indica es el método de pgzero que dibuja objetos en pantalla
    fondo.draw()
    personaje.draw()
    caja.draw()
    
    # Indicador de salto:
    if (personaje.timer_salto <= 0):
        screen.draw.text("¡LISTO!", midleft=(20,20), color = (0, 255, 0), fontsize=24)
    else:
        screen.draw.text(str(personaje.timer_salto), midleft=(20,20), color = "red", fontsize=24)    
    
    screen.draw.rect(personaje.collidebox, (255, 0, 255)) # Dibujamos collidebox del PJ
    # INDICADOR DE POS DEL PJ EN EJE X: # screen.draw.text(("X= " + str(personaje.x)), (30,30), background="white", color="black", fontsize=24)

def update(dt): # update(dt) es el bucle ppal de nuestro juego, dt significa delta time (tiempo en segundos entre cada frame)
    # > https://pygame-zero.readthedocs.io/en/stable/hooks.html#update
    # Podemos traducir "update" como "actualizar", es decir, en ella contendremos el código que produzca cambios en nuestro juego

    """   #######################
         # CAMBIOS AUTOMATICOS #
        #######################   """

    personaje.timer_salto -= dt # restamos al timer del cooldown de salto del persoanje el tiempo desde el último frame
    personaje.collidebox = Rect((personaje.x - int(personaje.width / 2), personaje.y - int(personaje.height / 2)), (personaje.width, personaje.height))

    nva_imagen = "alien"        # variable local que almacena el próximo sprite a renderizar
                                # "alien": quieto / "left": mov. izq. / "right" : mov. dcha.
    
    """   ################
         # LEER TECLADO #
        ################   """

    # Movimiento del personaje:
    if ( (keyboard.right or keyboard.d) and ( personaje.x < ( WIDTH - int(personaje.width / 2) ) ) ):
        personaje.x += personaje.velocidad
        nva_imagen = "right"

    if ( (keyboard.left or keyboard.a) and ( personaje.x > int(personaje.width / 2) ) ):
        personaje.x -= personaje.velocidad
        nva_imagen = "left"

    # Salto: lo implementamos en OnKeyDown(key)
    
    ###################################################################################
    
    # Mover la caja - NOTA/TO-DO: Migrar a una función
    
    if (caja.x < 0):     # Si la caja salió de la ventana de juego...
        caja.x += WIDTH  # La llevamos a la otra punta de la pantalla
    else:
        # Si todavía no se escapa de la ventana...
        caja.x -= 5      # mover la caja 5 px a la izquierda en cada frame
    
    caja.angle = (caja.angle % 360) + 5  # rotamos la caja 5 grados cada frame

    ###################################################################################
    """ POST INPUT """
    personaje.image = nva_imagen # Actualizamos el sprite del personaje

def on_key_down(key): # Este método se activa al presionar una tecla
    # https://pygame-zero.readthedocs.io/en/stable/hooks.html?highlight=on_key_down#on_key_down

    if (
         (keyboard.space or keyboard.w or keyboard.up) and   # Parte 1 de la cond: presionar tecla
         (personaje.timer_salto <= 0) and                    # Parte 2 de la cond: timer listo
         (personaje.y > int(personaje.height / 2))           # Parte 3 de la cond: el PJ NO ha salido de la pantalla
       ):
        
        personaje.timer_salto = personaje.COOLDOWN_SALTO                # Reseteamos cooldown
        #personaje.y -= personaje.altura_salto                           # El PJ "salta" (cambiamos su altura)
        #animate(personaje, tween="bounce_end", duration = 2, y = 240)   # Activamos la animación de caída

        temp_anim = animate(personaje, tween="decelerate", duration = personaje.COOLDOWN_SALTO, y = (personaje.y - personaje.altura_salto))   # PRIMERO ANIMACIÓN
        temp_anim.on_finished = bajarAlien

def bajarAlien():
    animate(personaje, tween="accelerate", duration = personaje.COOLDOWN_SALTO, y = personaje.posInicial[1])   # BAJAR ALIEN