import arcade
import time
import cv2
import os
from PIL import Image
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from clases.salas.almacen.sala_almacen import Sala_Almacen
from clases.salas.laboratorio.sala_laboratorio import Sala_Laboratorio
from clases.salas.hidroponia.sala_hidroponia import Sala_Hidroponia
from sala_instanciada1 import SalaActualView
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# Rutas de videos de transición
RUTAS_VIDEOS = {
    "transicion_almacen": os.path.join(CURRENT_PATH, "transiciones", "transicion_sala2.mp4"),
    "transicion_laboratorio": os.path.join(CURRENT_PATH, "transiciones", "transicion_sala3.mp4"),
    "transicion_hidroponia": os.path.join(CURRENT_PATH, "transiciones", "transicion_sala4.mp4"),
}

class Manager(arcade.View):
    def __init__(self):
        super().__init__()
        self.sala_actual = "ninguna"
        self.temporizador_inicio = 0.0

        # Control del reproductor de video
        self.cap = None
        self.textura_actual = None
        self.reproduciendo_video = False
        self.fps = 30
        self.frame_time = 1.0 / self.fps
        self.timer = 0.0

    def iniciar_video(self, ruta):
        if not os.path.exists(ruta):
            print(f"[ERROR VIDEO] No se encontró el archivo: {ruta}")
            return False

        self.cap = cv2.VideoCapture(ruta)
        if not self.cap.isOpened():
            print(f"[ERROR VIDEO] No se pudo decodificar el video: {ruta}")
            return False

        fps_video = self.cap.get(cv2.CAP_PROP_FPS)
        if fps_video > 0:
            self.fps = fps_video
            self.frame_time = 1.0 / self.fps

        self.timer = 0.0
        self.reproduciendo_video = True
        return self._leer_siguiente_frame()

    def _leer_siguiente_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb).convert("RGBA")
                self.textura_actual = arcade.Texture(image=pil_img)
                return True
            else:
                self.cap.release()
                self.cap = None
                self.reproduciendo_video = False
                return False
        return False

    def _avanzar_siguiente_sala(self):
        """Lógica para cargar la siguiente sala tras terminar el video o si este no existe."""
        self.textura_actual = None

        if self.sala_actual == "tuberias":
            self.sala_actual = "almacen"
            self.sala = SalaActualView(Sala_Almacen(), self)
            self.window.show_view(self.sala)

        elif self.sala_actual == "almacen":
            self.sala_actual = "laboratorio"
            self.sala = SalaActualView(Sala_Laboratorio(), self)
            self.window.show_view(self.sala)

        elif self.sala_actual == "laboratorio":
            self.sala_actual = "hidroponia"
            self.sala = SalaActualView(Sala_Hidroponia(), self)
            self.window.show_view(self.sala)

        elif self.sala_actual == "hidroponia":
            self._pantalla_victoria()

    def _pantalla_victoria(self):
        from victoria import VictoriaView
        victoria_view = VictoriaView()
        self.window.show_view(victoria_view)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.temporizador_inicio = time.time()

        # Diccionario de transiciones según la sala completada
        mapeo_transiciones = {
            "tuberias": RUTAS_VIDEOS["transicion_almacen"],
            "almacen": RUTAS_VIDEOS["transicion_laboratorio"],
            "laboratorio": RUTAS_VIDEOS["transicion_hidroponia"],
        }

        if self.sala_actual in mapeo_transiciones:
            video_a_reproducir = mapeo_transiciones[self.sala_actual]
            exito = self.iniciar_video(video_a_reproducir)
            if not exito:
                self._avanzar_siguiente_sala()

    def on_update(self, delta_time):
        # Arranque del juego (Sala 1: Tuberías)
        if self.sala_actual == "ninguna":
            if time.time() - self.temporizador_inicio > 1.0:
                self.sala_actual = "tuberias"
                self.sala = SalaActualView(Sala_Tuberias(), self)
                self.window.show_view(self.sala)

        # Si hay un video en reproducción
        elif self.reproduciendo_video:
            self.timer += delta_time
            if self.timer >= self.frame_time:
                self.timer = 0.0
                hay_frame = self._leer_siguiente_frame()
                if not hay_frame:
                    self._avanzar_siguiente_sala()

    def on_draw(self):
        self.clear()
        if self.reproduciendo_video and self.textura_actual:
            arcade.draw_texture_rect(
                self.textura_actual,
                arcade.XYWH(
                    const.ancho_ventana / 2,
                    const.alto_ventana / 2,
                    const.ancho_ventana,
                    const.alto_ventana
                )
            )