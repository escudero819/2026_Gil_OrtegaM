import arcade
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))   

Colisiones_Transparentes = False

class Objeto(arcade.Sprite):

    def __init__(self, tipo, imagen_path, center_x, center_y):
        super().__init__(imagen_path, center_x=center_x, center_y=center_y)
        self.tipo = tipo

class Interactuable(Objeto):
    
    def __init__(self, nombre, imagen_path, center_x, center_y, funcion, ubicacion_jugador = None, radio_interaccion = 30):
        super().__init__("interactuable", imagen_path, center_x, center_y)
        self.nombre = nombre
        self.funcion = funcion
        self.ubicacion_jugador = (self.center_x + ubicacion_jugador(1), self.center_y + ubicacion_jugador(2))
        self.radio_interaccion = radio_interaccion

class Bloqueo(Objeto):

    def __init__(self,imagen_transparente, center_x, center_y, ancho, alto):
        super().__init__("bloqueo", imagen_transparente, center_x, center_y)
        self.width = ancho
        self.height = alto

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
                imagen = CURRENT_PATH + "/transparente.png"
            else:
                imagen = CURRENT_PATH + "/semitransparente_rojo.png"
            pared = Bloqueo(imagen, int(colision["x"]), int(colision["y"]), int(colision["ancho"]), int(colision["alto"]))
            self.lista_bloqueos.append(pared)
    
    def Interactuables(self, interactuables: list[dict]):
        
        for interactuable in interactuables:
            # Creamos el objeto que interactua y genera pantallas emergentes
            objeto_interactuable = Interactuable(interactuable["funcion"], interactuable["textura"], interactuable["x"], interactuable["y"], ubicacion_jugador=interactuable.get("ubicacion_jugador"), radio_interaccion=interactuable.get("radio_interaccion"))
            self.lista_bloqueos.append(objeto_interactuable)
    
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