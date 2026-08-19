"""
CLASE ESCRITORIOVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_faltante.png")
fondo_vacio = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_vacio.png")
fondo_con_quimicos = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_inicial.png")
fondo_proceso1 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_pros_1.png")
fondo_proceso2 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_pros_2.png")
fondo_terminado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_finalizado.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/dest_retirado.png")

class DestiladorView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"
        self.bandera_destilacion = None

    def _destilador(self):
        self.destilador = arcade.Sprite(transparente, center_x= self.ancho/3 + self.correccion_x, center_y= self.alto/2 + self.correccion_y)
        self.destilador.width = 300
        self.destilador.height = 350
        self.lista_interaccion.append(self.destilador)

    def _tarrito(self):
        self.lista_interaccion.clear()
        self.tarrito = arcade.Sprite(transparente, center_x= self.ancho/3 + 215, center_y= self.alto/2)
        self.tarrito.width = 100
        self.tarrito.height = 100
        self.lista_interaccion.append(self.tarrito)

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)
            self._destilador()

        if self.estado == "vacio":
            self.cambiar_fondo(fondo_vacio)
            self._destilador()

        if self.estado == "con_quimicos":
            tiempo_trascurrido = time.time() - self.bandera_destilacion
            if tiempo_trascurrido > 30:
                self.cambiar_fondo(fondo_terminado)
                self.estado = "terminado"
                self._tarrito()
            elif tiempo_trascurrido > 20:
                self.cambiar_fondo(fondo_proceso2)
            elif tiempo_trascurrido > 10:
                self.cambiar_fondo(fondo_proceso1)
            else:
                self.cambiar_fondo(fondo_con_quimicos)


    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.estado == "con_quimicos":
            tiempo_trascurrido = time.time() - self.bandera_destilacion
            if tiempo_trascurrido > 30:
                self.cambiar_fondo(fondo_terminado)
                self.estado = "terminado"
                self._tarrito()
            elif tiempo_trascurrido > 20:
                self.cambiar_fondo(fondo_proceso2)
            elif tiempo_trascurrido > 10:
                self.cambiar_fondo(fondo_proceso1)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.destilador.collides_with_point((x, y)): 

            if self.estado == "inicial":
                if self.sala.inventario.consultar("destilador"):
                    self.estado = "vacio"
                    self.cambiar_fondo(fondo_vacio)

            elif self.estado == "vacio":
                if self.sala.inventario.consultar("quimicos estante"):
                    self.estado = "con_quimicos"
                    self.cambiar_fondo(fondo_con_quimicos)
                    self.bandera_destilacion = time.time()
        
            elif self.estado == "terminado":
                self.estado = "final"
                self.cambiar_fondo(fondo_final)
                self.sala.inventario.agregar_objeto("quimico amarillo")
                self.ejecutar_dialogo("bien, ahora hay que ir con la quimica")