import arcade
import os
from configuraciones import Constantes as consts

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class EscenaIntro:
    """Estructura de datos para almacenar una imagen y su lista secuencial de diálogos."""
    def __init__(self, ruta_imagen: str, lista_textos: list):
        self.ruta_imagen = ruta_imagen
        self.lista_textos = lista_textos


class IntroduccionView(arcade.View):
    def __init__(self, manager_siguiente=None):
        super().__init__()
        self.manager_siguiente = manager_siguiente

        # Lista de escenas añadidas
        self.escenas = []

        # Punteros de avance
        self.indice_escena = 0
        self.indice_texto = 0

        # Fondo actual en pantalla
        self.textura_fondo = None

        # Variables para efecto máquina de escribir
        self.texto_completo = ""
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.VELOCIDAD_TEXTO = 0.03

        # Objeto de texto Arcade
        self.interfaz_texto = None

    def agregar_escena(self, ruta_imagen: str, lista_textos: list):
        """Añade una diapositiva con su lista ordenada de diálogos."""
        self.escenas.append(EscenaIntro(ruta_imagen, lista_textos))
        return self  # Permite encadenar llamadas si se desea

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        ancho_pantalla = self.window.width
        self.interfaz_texto = arcade.Text(
            text="",
            x=80,
            y=110,
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Courier New",
            bold=True,
            multiline=True,
            width=ancho_pantalla - 160
        )

        # Si aún no se ha cargado ninguna escena, iniciamos desde la primera
        if self.escenas and self.textura_fondo is None:
            self._cargar_escena_actual()

    def _cargar_escena_actual(self):
        """Carga la imagen de la diapositiva actual y prepara su primer diálogo."""
        if self.indice_escena < len(self.escenas):
            escena = self.escenas[self.indice_escena]
            if os.path.exists(escena.ruta_imagen):
                self.textura_fondo = arcade.load_texture(escena.ruta_imagen)
            else:
                print(f"[Error Intro] No se encontró la imagen: {escena.ruta_imagen}")
                self.textura_fondo = None

            self.indice_texto = 0
            if escena.lista_textos:
                self._mostrar_texto(escena.lista_textos[self.indice_texto])
            else:
                # Si la escena no tiene textos, pasa a la siguiente
                self._avanzar_escena()
        else:
            self._finalizar_intro()

    def _mostrar_texto(self, mensaje: str):
        """Reinicia el efecto de tipeo con el nuevo texto."""
        self.texto_completo = mensaje
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.interfaz_texto.text = ""

    def _avanzar_escena(self):
        self.indice_escena += 1
        if self.indice_escena < len(self.escenas):
            self._cargar_escena_actual()
        else:
            self._finalizar_intro()

    def _finalizar_intro(self):
        """Lanza el Manager (o la vista configurada) al agotar todas las escenas."""
        if self.manager_siguiente:
            self.manager_siguiente._iniciar_musica_global()
            self.window.show_view(self.manager_siguiente)
        else:
            from manager import Manager
            self.manager_siguiente = Manager()
            self.manager_siguiente._iniciar_musica_global()
            self.window.show_view(Manager())

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if not self.escenas or self.indice_escena >= len(self.escenas):
            self._finalizar_intro()
            return

        # 1. Si el texto aún se está escribiendo, el clic lo completa de golpe
        if self.indice_letra < len(self.texto_completo):
            self.texto_actual = self.texto_completo
            self.indice_letra = len(self.texto_completo)
            self.interfaz_texto.text = self.texto_actual
            return

        # 2. Si ya terminó de escribir, avanza al siguiente diálogo de la lista
        escena_actual = self.escenas[self.indice_escena]
        self.indice_texto += 1

        if self.indice_texto < len(escena_actual.lista_textos):
            self._mostrar_texto(escena_actual.lista_textos[self.indice_texto])
        else:
            # 3. Al terminar los textos de la diapositiva, pasa a la siguiente escena
            self._avanzar_escena()

    def on_update(self, delta_time: float):
        if self.indice_letra < len(self.texto_completo):
            self.temporizador_letra += delta_time
            if self.temporizador_letra >= self.VELOCIDAD_TEXTO:
                self.temporizador_letra = 0.0
                self.texto_actual += self.texto_completo[self.indice_letra]
                self.indice_letra += 1
                self.interfaz_texto.text = self.texto_actual

    def on_draw(self):
        self.clear()

        # Dibujar imagen de fondo ajustada a la ventana
        if self.textura_fondo:
            arcade.draw_texture_rect(
                self.textura_fondo,
                arcade.XYWH(
                    self.window.width / 2,
                    self.window.height / 2,
                    self.window.width,
                    self.window.height
                )
            )

        # Cuadro de diálogo inferior
        ancho_pantalla = self.window.width
        arcade.draw_lbwh_rectangle_filled(
            left=40,
            bottom=25,
            width=ancho_pantalla - 80,
            height=110,
            color=(15, 15, 15, 230)
        )
        arcade.draw_lbwh_rectangle_outline(
            left=40,
            bottom=25,
            width=ancho_pantalla - 80,
            height=110,
            color=arcade.color.WHITE,
            border_width=3
        )

        if self.interfaz_texto:
            self.interfaz_texto.draw()