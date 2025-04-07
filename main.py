#pgzero
""" [M6.L3] - Actividad 3: "La función draw()"
    Objetivo: Que la clase muestre un mensaje personalizado con el método draw() """

WIDTH = 900 # Ancho de la pantalla (en px)
HEIGHT = 360 # Alto de la pantalla (en px)

TITLE = "TITULO ÉPICO" # sin archivos
FPS = 30 # Tope/Límite de FPS (cuadros por segundo) a dibujar

string_mensaje = "¡Hola chicos!"

def draw():
    screen.fill((220, 125, 131))
    screen.draw.text(string_mensaje, center=(WIDTH/2, HEIGHT/2), color="white", background="black", fontsize = 48)
    # MUCHO TEXTO :V -> https://pygame-zero.readthedocs.io/en/stable/builtins.html?highlight=text#Screen.draw.text
    #                -> https://pygame-zero.readthedocs.io/en/stable/ptext.html?highlight=text