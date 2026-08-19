"""
CLASE MEDIDORVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_med.png")
fondo_quimicos_mesa = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_med_mesa.png")
fondo_quimicos_estante = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_med_est.png")
fondo_completo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_med_completa.png")

fondo_puzzle = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_puzzle.png")
quimico_vial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/vial.png")
quimico_morado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/morado.png")
quimico_azul = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/azul.png")
quimico_amarillo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/amarillo.png")
recipiente_medidor = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/medidor.png")

class PuzzleMedidor(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.medidor = None
        self.matraz_azul = None
        self.matraz_morado = None
        self.vial_celeste = None
        self.tarrito_amarillo = None
        self.seleccion = None
        self.combinacion_tomada = False
        self.quimicos_colocados = []
        self.limite_quimicos = 9
        self.combinacion = None

        self.COLOR_OSCURO = (100, 100, 100)     
        self.COLOR_SELECCIONADO = (255, 255, 255) 

        # Colores del líquido
        self.COLOR_LIQUIDO_NORMAL = (20, 20, 20)           # Negro / oscuro
        self.COLOR_CORRECTO = (173, 255, 47)               # Verde amarillento (Yellow-Green)
        self.COLOR_INCORRECTO = (180, 20, 90)              # Rojo violáceo / Magenta oscuro

    def _quimicos(self):
        if not self.combinacion_tomada:
            if not self.medidor:
                self.medidor = arcade.Sprite(self.escalar_interactuable(recipiente_medidor), center_x= self.ancho/2 + self.correccion_x, center_y= self.alto/2 + self.correccion_y - 25)
            self.lista_interaccion.append(self.medidor)
            self.lista_medidor.append(self.medidor)

        if not self.matraz_azul:
            self.matraz_azul = arcade.Sprite(self.escalar_interactuable(quimico_azul), center_x= self.ancho/4 * 0.75 + self.correccion_x, center_y= self.alto/2 + self.correccion_y - 50)
        self.matraz_azul.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.matraz_azul)

        if not self.matraz_morado:
            self.matraz_morado = arcade.Sprite(self.escalar_interactuable(quimico_morado), center_x= self.ancho/4*1.25 + self.correccion_x, center_y= self.alto/2 + self.correccion_y - 50)
        self.matraz_morado.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.matraz_morado)

        if not self.vial_celeste:
            self.vial_celeste = arcade.Sprite(self.escalar_interactuable(quimico_vial), center_x= self.ancho/4*2.75 + self.correccion_x, center_y= self.alto/2 + self.correccion_y - 50)
        self.vial_celeste.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.vial_celeste)

        if not self.tarrito_amarillo:
            self.tarrito_amarillo = arcade.Sprite(self.escalar_interactuable(quimico_amarillo), center_x= self.ancho/4*3.25 + self.correccion_x, center_y= self.alto/2 + self.correccion_y - 50)
        self.tarrito_amarillo.color = self.COLOR_OSCURO
        self.lista_interaccion.append(self.tarrito_amarillo)

    def _seleccionar(self):
        self.matraz_azul.color = self.COLOR_OSCURO
        self.matraz_morado.color = self.COLOR_OSCURO
        self.vial_celeste.color = self.COLOR_OSCURO
        self.tarrito_amarillo.color = self.COLOR_OSCURO

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(fondo_puzzle)
        if not self.combinacion_tomada:
            self.lista_medidor = arcade.SpriteList()
        self._quimicos()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.matraz_azul.collides_with_point((x, y)):
            self._seleccionar()
            self.matraz_azul.color = self.COLOR_SELECCIONADO
            self.seleccion = "azul"

        if self.matraz_morado.collides_with_point((x, y)):
            self._seleccionar()
            self.matraz_morado.color = self.COLOR_SELECCIONADO
            self.seleccion = "morado"

        if self.vial_celeste.collides_with_point((x, y)):
            self._seleccionar()
            self.vial_celeste.color = self.COLOR_SELECCIONADO
            self.seleccion = "celeste"

        if self.tarrito_amarillo.collides_with_point((x, y)):
            self._seleccionar()
            self.tarrito_amarillo.color = self.COLOR_SELECCIONADO
            self.seleccion = "amarillo"

        if self.medidor.collides_with_point((x, y)):
            if self.combinacion:
                self.sala.inventario.agregar_objeto("combinacion final")
                self.combinacion_tomada = True
                self.lista_medidor = None

            if self.seleccion and len(self.quimicos_colocados) < self.limite_quimicos:
                self.quimicos_colocados.append(self.seleccion)
                self.seleccion = None
                self._seleccionar()  # Deselecciona visualmente los matraces

                # Verificar si se llenó por completo
                if len(self.quimicos_colocados) == self.limite_quimicos:
                    c_azul = self.quimicos_colocados.count("azul")
                    c_amarillo = self.quimicos_colocados.count("amarillo")
                    c_celeste = self.quimicos_colocados.count("celeste")
                    c_morado = self.quimicos_colocados.count("morado")

                    if c_azul == 3 and c_amarillo == 3 and c_celeste == 1 and c_morado == 2:
                        self.combinacion = True
                        print("Combinación correcta!")
                    else:
                        self.combinacion = False
                        print("Combinación incorrecta!")

    def on_draw(self):
        # 1. Limpiar pantalla y dibujar elementos base heredados
        super().on_draw()


        if not self.combinacion_tomada:
            # 2. Dibujar el líquido si hay químicos colocados
            if len(self.quimicos_colocados) > 0 and self.medidor:
                # Dimensiones visuales del tubo interno (ajusta según el tamaño de tu sprite)
                ancho_liquido = 45  
                altura_maxima = 200 
                
                # Base inferior desde donde empieza a subir el líquido
                base_y = self.medidor.center_y - (altura_maxima / 2)
                
                # Altura proporcional a la cantidad de químicos ingresados
                progreso = len(self.quimicos_colocados) / self.limite_quimicos
                alto_actual = altura_maxima * progreso

                # Definir color según el estado del puzzle
                if self.combinacion is True:
                    color_actual = self.COLOR_CORRECTO
                elif self.combinacion is False:
                    color_actual = self.COLOR_INCORRECTO
                else:
                    color_actual = self.COLOR_LIQUIDO_NORMAL

                # Dibujo del rectángulo usando la sintaxis de Arcade 3.0+
                arcade.draw_rect_filled(
                    arcade.XYWH(
                        self.medidor.center_x,
                        base_y + (alto_actual / 2),
                        ancho_liquido,
                        alto_actual
                    ),
                    color=color_actual
                )

            # 3. Volver a dibujar el medidor encima para que el líquido quede por detrás del cristal/marcas
            self.lista_medidor.draw()

class MedidorView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"
        self.puzzle = False
        self.medidor = PuzzleMedidor(self.partida)

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)

        if self.estado == "quimicos mesa":
            self.cambiar_fondo(fondo_quimicos_mesa)
            
        if self.estado == "quimicos estante":
            self.cambiar_fondo(fondo_quimicos_estante)

        if self.estado == "completo":
            self.cambiar_fondo(fondo_completo)
            self._puzzle()


    def _puzzle(self):
        self.puzzle_interaccion = arcade.Sprite(transparente, center_x=self.ancho/2 + self.correccion_x, center_y=self.alto/2 + self.correccion_y)
        self.puzzle_interaccion.width = 300
        self.puzzle_interaccion.height = 300
        self.lista_interaccion.append(self.puzzle_interaccion)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.estado == "inicial":
            if self.sala.inventario.consultar("quimicos mesa"):
                self.estado = "quimicos mesa"
                self.cambiar_fondo(fondo_quimicos_mesa)
            else:
                self.ejecutar_dialogo("tendria que investigar mas")
        
        elif self.estado == "quimicos mesa":
            if self.sala.inventario.consultar("quimicos estante"):
                self.estado = "quimicos estante"
                self.cambiar_fondo(fondo_quimicos_estante)
            else:
                self.ejecutar_dialogo("falta el quimico del estante")
        
        elif self.estado == "quimicos estante":
            if self.sala.inventario.consultar("quimico amarillo"):
                self.estado = "completo"
                self.puzzle = True
                self._puzzle()
                self.cambiar_fondo(fondo_completo)
            else:
                self.ejecutar_dialogo("me falta la combinacion que dice la quimica")

        elif self.estado == "completo":
            if self.puzzle_interaccion.collides_with_point((x, y)):
                self.partida.window.show_view(self.medidor)