import arcade, os, math
from configuraciones import Constantes as const
from clases.salas.interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# Carga de recursos estables
fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/valvulas/fondo.png")
valvula_tex = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/valvulas/valvula.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

# El objetivo en grados para ganar (Casi una vuelta completa: 340°)
SOLUCION = 340

class ValvulasInterfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "incompleto"
        self.sala = self.partida.sala
        
        # Guardará el sprite de la válvula que el jugador está cliqueando/manteniendo activamente
        self.valvula_girando = None
        self.fondo_sprite = None

        # VELOCIDADES DE GIRO Y AFLOJAMIENTO (Grados por segundo)
        self.VELOCIDAD_APRIETE = 120.0  # Cuánto sube la válvula que mantienes presionada
        
        # Configuración de las 3 velocidades de aflojamiento (pérdida de ángulo)
        self.VEL_SOFT = 10.0
        self.VEL_MEDIUM = 35.0
        self.VEL_HIGH = 40.0

        # Inicialización de las 3 válvulas en posiciones horizontales fijas
        # Ajusta las posiciones en X si tus válvulas se superponen
        self.config_valvulas = [
            {"name": "Válvula 1", "x": self.centro_x - 230, "y": self.centro_y + 27, "vel_bajada": self.VEL_SOFT},
            {"name": "Válvula 2", "x": self.centro_x - 77,  "y": self.centro_y - 69, "vel_bajada": self.VEL_MEDIUM},
            {"name": "Válvula 3", "x": self.centro_x + 75, "y": self.centro_y + 27, "vel_bajada": self.VEL_HIGH}
        ]

    def _inicializar_sprites_fijos(self):
        """ Crea los sprites de fondo y válvulas de forma persistente en memoria """
        # Sprite del fondo metálico de la interfaz
        self.cambiar_fondo(fondo)

        # Generación de los 3 objetos de válvula con sus respectivas propiedades físicas
        for config in self.config_valvulas:
            spr = arcade.Sprite(valvula_tex, center_x=config["x"], center_y=config["y"])
            spr.angle = 0.0  # Comienzan totalmente cerradas/flojas
            spr.vel_bajada = config["vel_bajada"]
            spr.name = config["name"]
            self.lista_valvulas.append(spr)

    def on_show_view(self):
        super().on_show_view()
        """ Se ejecuta al abrir la interfaz de las válvulas """
        self.valvula_girando = None
        # Contenedores gráficos de Arcade
        self.lista_fondo = arcade.SpriteList()
        self.lista_valvulas = arcade.SpriteList()
        self._inicializar_sprites_fijos()

    def on_draw(self):
        super().on_draw()
        self.lista_fondo.draw()
        self.lista_valvulas.draw()

        # Opcional: Feedback visual en texto para ver los grados exactos de cada válvula
        for v in self.lista_valvulas:
            arcade.draw_text(
                text=f"{int(v.angle)}° / {360}°",
                x=v.center_x,
                y=v.center_y - 120,
                color=arcade.color.GREEN if v.angle >= SOLUCION else arcade.color.WHITE,
                font_size=14,
                anchor_x="center"
            )

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.estado != "incompleto":
            return

        # 1. Si el jugador está interactuando con una válvula, la hacemos girar (apretar)
        if self.valvula_girando:
            self.valvula_girando.angle += self.VELOCIDAD_APRIETE * delta_time
            # Limitamos el giro al ángulo objetivo para que no dé vueltas infinitas
            if self.valvula_girando.angle > 360:
                self.valvula_girando.angle = 360

        # 2. Las válvulas que NO están siendo presionadas se aflojan con sus velocidades asignadas
        for v in self.lista_valvulas:
            if v != self.valvula_girando:
                v.angle -= v.vel_bajada * delta_time
                # No permitimos que tengan ángulos negativos
                if v.angle < 0:
                    v.angle = 0.0

        # 3. Corroboración de la condición de victoria
        self.verificar_puzzle()

    def verificar_puzzle(self):
        # El puzzle se resuelve si las 3 válvulas alcanzaron simultáneamente el ángulo SOLUCION
        for v in self.lista_valvulas:
            if v.angle < SOLUCION:
                return  # Si una sola válvula no llegó al objetivo, el juego continúa

        # ¡VICTORIA! Todas las válvulas están ajustadas a la presión correcta
        self.estado = "resuelto"
        self.valvula_girando = None
        print("¡Puzzle de Válvulas Completado con Éxito!")
        
        # Ejecutamos la resolución en la sala base y notificamos al jugador
        self.sala.ValvulasResuelto()
        self.partida.ejecutar_dialogo("¡Excelente! Las válvulas han cortado el flujo de agua en la sala.", 
                                      voz="es-ES-AlvaroNeural", velocidad="+0%", tono="+0Hz")
        
        # Cerramos la interfaz regresando a la simulación limpia de la partida
        self.window.show_view(self.partida)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        # Detectar cuál de las 3 válvulas fue presionada por el cursor
        valvulas_tocadas = arcade.get_sprites_at_point((x, y), self.lista_valvulas)
        if valvulas_tocadas:
            self.valvula_girando = valvulas_tocadas[0]
            print(f"Apretando: {self.valvula_girando.name}")

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # En el momento en el que el jugador suelta el botón del mouse, la válvula deja de girar
            if self.valvula_girando:
                print(f"Se soltó: {self.valvula_girando.name}")
                self.valvula_girando = None