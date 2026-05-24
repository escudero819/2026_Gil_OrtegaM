import arcade

class Sala():

    def __init__(self):        
        # una lista de texturas del fondo por si el mismo es animado
        self.texturas_fondo = []
        # una SpriteList de las paredes invisibles para las colisiones
        self.paredes = arcade.SpriteList()
        # una lista de los objetos interactuables para aparte de colisionar, poder interactuar
        self.objetos = [dict]
        # un Sprite de 'Salida' para saber que cuando el jugador lo toque se pasara al siguiente nivel
        self.salida = arcade.Sprite()
        