"""
CLASE DE LA CLASE TOLDOVIEW 
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))
fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/toldo.png")
potasio = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/potasio.png")
nitrogeno = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/nitrogeno.png")
fosforo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/fosforo.png")
ingresar = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/ingresar.png")

class ToldoView(InteraccionBase):

    def __init__(self, partida, plantio):
        super().__init__()
        self.partida = partida
        self.plantio = plantio
        self.bolsas = False

        self.ubicacion_potasio_y = None
        self.ubicacion_nitrogeno_y = None
        self.ubicacion_fosforo_y = None
        self.ubicacion_bolsas_x = None
        self.ubicacion_numeros_x =  None

        self.bolsa_seleccionada = None
        self.ingresar = None

        self.COLOR_OSCURO = (100, 100, 100)     
        self.COLOR_SELECCIONADO = (255, 255, 255) 

    def _volver(self):
        self.volver = arcade.Sprite(transparente, center_x= 40 + self.correccion_x, center_y= self.alto - 40 + self.correccion_y)
        self.volver.width = 50
        self.volver.height = 50
        print("volver")
        self.lista_interaccion.append(self.volver)

    def _bolsas(self):
        self.potasio = arcade.Sprite(potasio, center_x= self.ubicacion_bolsas_x, center_y= self.ubicacion_potasio_y)
        self.potasio.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.potasio)

        self.nitrogeno = arcade.Sprite(nitrogeno, center_x= self.ubicacion_bolsas_x, center_y= self.ubicacion_nitrogeno_y)
        self.nitrogeno.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.nitrogeno)

        self.fosforo = arcade.Sprite(fosforo, center_x= self.ubicacion_bolsas_x, center_y= self.ubicacion_fosforo_y)
        self.fosforo.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.fosforo)

    def _numeros(self):

        self.cant_potasio = self.partida.sala.inventario.lista_objetos.count('potasio') if self.partida.sala.inventario.consultar("potasio") else 0

        self.num_potasio = arcade.Text(
            text=f"{self.cant_potasio}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_potasio_y - 15,
            color=arcade.color.WHITE_SMOKE,
            font_size=30,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.cant_nitrogeno = self.partida.sala.inventario.lista_objetos.count('nitrogeno') if self.partida.sala.inventario.consultar("nitrogeno") else 0

        self.num_nitrogeno = arcade.Text(
            text=f"{self.cant_nitrogeno}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_nitrogeno_y - 10,
            color=arcade.color.WHITE_SMOKE,
            font_size=30,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.cant_fosforo = self.partida.sala.inventario.lista_objetos.count('fosforo') if self.partida.sala.inventario.consultar("fosforo") else 0

        self.num_fosforo = arcade.Text(
            text=f"{self.cant_fosforo}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_fosforo_y,
            color=arcade.color.WHITE_SMOKE,
            font_size=30,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )
        print(self.cant_potasio, self.cant_nitrogeno, self.cant_fosforo)

    def _ingresar(self):
        self.potasio.color = self.COLOR_OSCURO
        self.nitrogeno.color = self.COLOR_OSCURO
        self.fosforo.color = self.COLOR_OSCURO
        if not self.ingresar:
            self.ingresar = arcade.Sprite(ingresar, center_x= self.ancho/3 + self.correccion_x, center_y= self.alto/3 + self.correccion_y)
            self.lista_interaccion.append(self.ingresar)
    
    def on_show_view(self):
        super().on_show_view()
        if not self.bolsas:
            self.cambiar_fondo(fondo)
            self.ubicacion_potasio_y = self.alto / 6 * 4.75 + self.correccion_y
            self.ubicacion_nitrogeno_y = self.alto / 6 * 3 + self.correccion_y
            self.ubicacion_fosforo_y = self.alto / 6 * 1.25 + self.correccion_y
            self.ubicacion_bolsas_x = self.ancho / 4 * 3 + self.correccion_x
            self.ubicacion_numeros_x = self.ubicacion_bolsas_x + self.ancho / 8 + 18
        else:
            self.cambiar_fondo(self.fondo)
        self.ingresar = None
        self._volver()
        self._bolsas()
        self._numeros()

    def on_draw(self):
        super().on_draw()
        self.num_potasio.draw()
        self.num_nitrogeno.draw()
        self.num_fosforo.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.volver.collides_with_point((x,y)):
            self.partida.window.show_view(self.plantio)

        if self.potasio.collides_with_point((x,y)):
            self.bolsa_seleccionada = "potasio"
            self._ingresar()
            self.potasio.color = self.COLOR_SELECCIONADO

        if self.nitrogeno.collides_with_point((x,y)):
            self.bolsa_seleccionada = "nitrogeno"
            self._ingresar()
            self.nitrogeno.color = self.COLOR_SELECCIONADO

        if self.fosforo.collides_with_point((x,y)):
            self.bolsa_seleccionada = "fosforo"
            self._ingresar()
            self.fosforo.color = self.COLOR_SELECCIONADO

        if self.bolsa_seleccionada:
            if self.ingresar.collides_with_point((x,y)):
                if self.bolsa_seleccionada == "potasio" and self.cant_potasio > 0 or self.bolsa_seleccionada == "nitrogeno" and self.cant_nitrogeno > 0 or self.bolsa_seleccionada == "fosforo" and self.cant_fosforo > 0:
                    self.plantio.nutrientes[self.bolsa_seleccionada] += 1
                    # EJECUTAR SONIDO DE TIERRA

                    self.partida.sala.inventario.eliminar_objeto(self.bolsa_seleccionada)
                    self._numeros()
                else:
                    self.ejecutar_dialogo("no tengo nada del nutriente")