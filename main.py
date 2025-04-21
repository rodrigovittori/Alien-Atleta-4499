#pgzero

""" NOTA 1: El código de este proyecto está publicado en el repo:
            > https://github.com/rodrigovittori/Alien-Atleta-4499/
    
    NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
            pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
            y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  
    
---------------------------------------------------------------------------------------------------

    [M6.L4] - Actividad Nº 9 y 10 (Extras): "Esquivando"
    Objetivo: Agregar la lógica necesaria para que nuestro personaje pueda agacharse

    NOTA: La primer tarea extra ("Controles mejorados") ya la cumple nuestro código anterior

    Paso Nº 1) Agregar check para cuando se presione la tecla "S" o la flecha hacia abajo
    Paso Nº 2) Modificar la altura del personaje cuando se presione la tecla
    Paso Nº 3) Cambiar el sprite del personaje
    Paso Nº 4) Crear dos atributos "esta_agachado" y "timer_agachado" para controlar cuando deshacemos los cambios
    Paso Nº 5) Implementar la lógica de reseteo de la altura
    Paso Nº 6) Agregamos una condición para que NO se pueda saltar mientras el PJ está agachado

    NOTA: Si NO queremos permitir que el PJ se mueva mientras está agachado debemos agregar una cond. extra al mov.

    Nota: Para evitar que al agacharse se anule la animación de salto DEBERÍAMOS implementar un check para prevenirlo

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

personaje.COOLDOWN_SALTO = 0.9        # tiempo de recarga habilidad salto (en segundos)
personaje.timer_salto = 0             # tiempo que debe pasar (en segundos) antes de que nuestro personaje pueda saltar nuevamente
personaje.altura_salto = int(personaje.height * 1.6) # El personaje saltará 1.6 veces su altura

""" Nota: Para evitar que al agacharse se anule la animación de salto DEBERÍAMOS implementar un check para prevenirlo """
personaje.timer_agachado = 0.0        # Tiempo restante (en segundos) antes de poner de pie al personaje
personaje.esta_agachado = False       # Valor que controla si debemos permanecer agachados o no

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

    personaje.timer_salto -= dt    # restamos al timer del cooldown de salto del persoanje el tiempo desde el último frame

    personaje.timer_agachado -= dt # restamos al timer para resetar la altura del persoanje el tiempo desde el último frame

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