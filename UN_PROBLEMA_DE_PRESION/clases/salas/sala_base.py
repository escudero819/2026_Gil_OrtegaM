import arcade
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))   

Colisiones_Transparentes = True



class Interactuable():

    def __init__(self, script):
        self.script = script


class Objeto():

    def __init__(self, nombre, imagen):

        self.imagen = imagen
        self.nombre = nombre
        

class Sala():

    def __init__(self):
        # una lista de texturas del fondo por si el mismo es animado
        self.fondo_texturas = []
        self.fondo_lista = arcade.SpriteList()
        self.fondo_sprite = None
        # una SpriteList de las paredes invisibles para las colisiones
        self.lista_bloqueos = arcade.SpriteList(use_spatial_hash=True)
        # una lista de los objetos interactuables para poder interactuar
        self.interactuables_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.interactuables_objetos = []

        # una lista de los objetos capaces de levantar del suelo e integrarse en el inventario
        self.objetos_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.objetos_objetos = []

        # un Sprite de 'Salida' para saber que cuando el jugador lo toque se pasara al siguiente nivel
        self.salida = arcade.Sprite()
    
    def Fondo(self, texturas_fondo: list[arcade.Texture]):

        self.fondo_texturas = texturas_fondo
        self.fondo_sprite = arcade.Sprite(self.fondo_texturas[0])
        self.fondo_lista.append(self.fondo_sprite)
        self.ancho = self.fondo_texturas[0].width
        self.alto = self.fondo_texturas[0].height
        self.fondo_sprite.center_x = self.ancho/2
        self.fondo_sprite.center_y = self.alto/2
    
    def Colisiones(self, paredes: list[dict]):

        for colision in paredes:
            if Colisiones_Transparentes:
                pared = arcade.Sprite(CURRENT_PATH + "/transparente.png")
            else:
                pared = arcade.Sprite(CURRENT_PATH + "/semitransparente_rojo.png")
            pared.center_x = colision["x"]
            pared.center_y = colision["y"]
            pared.width = colision["ancho"]
            pared.height = colision["alto"]
            self.lista_bloqueos.append(pared)
    
    def Interactuables(self, interactuables: list[dict]):
        
        for interactuable in interactuables:
            # Creamos el Sprite con el que se genera la interaccion
            textura = interactuable["textura"]
            objeto = arcade.Sprite(textura)
            objeto.center_x = interactuable["x"]
            objeto.center_y = interactuable["y"]
            self.interactuables_sprites.append(objeto)
            # Creamos el objeto que interactua y genera pantallas emergentes
            objeto_interactuable = Interactuable(interactuable["funcion"])
            self.interactuables_objetos = objeto_interactuable
    
    def Objetos(self, objetos: list[dict]):

        for objeto in objetos:
            textura = arcade.load_texture(objeto["textura"])
            objeto = arcade.Sprite(textura)
            objeto.center_x = objeto["x"]
            objeto.center_y = objeto["y"]
            self.interactuables_sprites.append(objeto)

            objeto_objeto = Objeto(objeto["nombre"], objeto["textura"])
            self.objetos_objetos.append(objeto_objeto)

    def draw(self):
        self.fondo_lista.draw()
        self.interactuables_sprites.draw()
        self.lista_bloqueos.draw()