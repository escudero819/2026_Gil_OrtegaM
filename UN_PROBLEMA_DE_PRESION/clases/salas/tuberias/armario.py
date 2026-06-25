import arcade, os
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo_con_candado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/con_candado.png")
fondo_sin_candado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/sin_candado.png")
fondo_abierto = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/abierto.png")
fondo_sin_objetos = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/sin_objetos.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class ArmarioInterfaz(arcade.View):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "con_candado"
        self.sala = self.partida.sala
        self.centro_x = const.ancho_ventana / 2
        self.centro_y = const.alto_ventana / 2
        self.fondo = None
    
    def cambiar_fondo(self, fondo):
        self.fondo = fondo
        fondo = arcade.Sprite(fondo)
        factor_y = const.alto_interfaces / fondo.height 
        factor_x = const.ancho_interfaces/ fondo.width
        factor = min(factor_x, factor_y)
        fondo.height = fondo.height * factor
        fondo.width = fondo.width * factor
        fondo.center_x = self.centro_x
        fondo.center_y = self.centro_y
        if self.lista_fondo:
            self.lista_fondo.pop()
        self.lista_fondo.append(fondo)

    def _candados(self):
        cadenas = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y)
        cadenas.width = 200
        cadenas.height = 200
        self.lista_interaccion.append(cadenas)

    def _cad_rotas(self):
        puertas = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y)
        puertas.width = 200
        puertas.height = const.alto_interfaces
        if self.lista_interaccion:
            self.lista_interaccion.clear()
        self.lista_interaccion.append(puertas)
    
    def _abierto(self):
        objetos = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y + self.fondo.height/6)
        objetos.width = self.fondo.height / 2
        objetos.height = 200
        if self.lista_interaccion:
            self.lista_interaccion.clear()
        self.lista_interaccion.append(objetos)
    
    def _sin_obj(self):
        if self.lista_interaccion:
            self.lista_interaccion.clear()

    def on_show_view(self):

        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()
        if not self.fondo:
            self.cambiar_fondo(fondo_con_candado)
        else:
            self.cambiar_fondo(self.fondo)
        if self.estado == "con_candado":
            self._candados()
        
        elif self.estado == "sin_candado":
            self._cad_rotas()

        elif self.estado == "abierto":
            self._abierto()

        print(self.fondo.width, self.fondo.height) # borrar linea
    


    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                if self.estado == "con_candado":
                    if self.sala.inventario.consultar("pinzas"):
                        self.cambiar_fondo(fondo_sin_candado)
                        self._cad_rotas()
                        self.estado = "sin_candado"
                    else:
                        self.sala.mostrar_texto("cerrado... pero creo que puedo cortarlas con alguna herramienta")
                elif self.estado == "sin_candado":
                    self.cambiar_fondo(fondo_abierto)
                    self._abierto()
                    self.estado = "abierto"
                else:
                    self.cambiar_fondo(fondo_sin_objetos)
                    self.sala.inventario.agregar_objeto("herramientas")
                    mensaje = "he conseguido cables y herramientas, me seran utiles"
                    self.partida.mostrar_texto(mensaje)
                    self._sin_obj()
                    self.estado = "sin_objetos"
        else:
            self.window.show_view(self.partida)