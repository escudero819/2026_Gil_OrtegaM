import arcade
import time
import cv2
import threading
from PIL import Image
from clases.salas.almacen.sala_almacen import Sala_Almacen
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from sala_instanciada import SalaActualView
from configuraciones import Constantes as const

ruta_transicion_sala2 = "transiciones/transicion_sala2.mp4"

class Manager(arcade.View):
    def __init__(self):
        super().__init__()
        self.sala_actual = "ninguna"  
        self.temporizador_inicio = 0.0

        self.frames_texturas = []
        self.current_frame_index = 0
        self.video_finished = False
        self.video_cargado = False

        self.fps = 30
        self.frame_time = 1.0 / self.fps
        self.timer = 0.0

        # Lanzamos la carga de frames en un hilo separado para evitar bloqueos
        threading.Thread(target=self._cargar_video_hilo, daemon=True).start()

    def _cargar_video_hilo(self):
        cap = cv2.VideoCapture(ruta_transicion_sala2)
        fps_video = cap.get(cv2.CAP_PROP_FPS)
        if fps_video > 0:
            self.fps = fps_video
            self.frame_time = 1.0 / self.fps

        frames_temporales = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb).convert("RGBA")
            # Nota: la textura se creará de forma segura en el hilo principal
            frames_temporales.append(pil_image)
            
        cap.release()

        # Una vez listas las imágenes PIL, creamos las texturas de Arcade
        for pil_img in frames_temporales:
            self.frames_texturas.append(arcade.Texture(image=pil_img))
        
        self.video_cargado = True

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.temporizador_inicio = time.time()

    def on_update(self, delta_time):
        if self.sala_actual == "ninguna":
            if time.time() - self.temporizador_inicio > 1.0:  
                self.sala_actual = "tuberias"
                self.sala = SalaActualView(Sala_Tuberias(), self)
                self.window.show_view(self.sala)
        
        elif self.sala_actual == "tuberias" and not self.video_finished:
            # Solo avanzamos el video si ya terminó de cargarse en segundo plano
            if self.video_cargado and self.frames_texturas:
                self.timer += delta_time
                if self.timer >= self.frame_time:
                    self.timer = 0.0
                    self.current_frame_index += 1
                    
                    if self.current_frame_index >= len(self.frames_texturas):
                        self.video_finished = True
                        self.sala_actual = "almacen" # Reiniciamos para que no intente reproducir de nuevo
                        self.sala = SalaActualView(Sala_Almacen(), self)
                        self.window.show_view(self.sala)

    def on_draw(self):
        self.clear()
        
        if self.sala_actual == "tuberias" and not self.video_finished:
            if self.video_cargado and self.frames_texturas:
                texture_to_draw = self.frames_texturas[min(self.current_frame_index, len(self.frames_texturas) - 1)]
                arcade.draw_texture_rect(
                    texture_to_draw,
                    arcade.XYWH(const.ancho_ventana / 2, const.alto_ventana / 2, const.ancho_ventana, const.alto_ventana)
                )