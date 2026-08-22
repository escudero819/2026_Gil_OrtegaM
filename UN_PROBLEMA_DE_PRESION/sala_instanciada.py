import arcade
import os, math, asyncio, threading, time
from clases.salas.sala_base import Interactuable, Objeto
from clases.personajes.ingeniero import Ingeniero
from configuraciones import Constantes as consts
import edge_tts

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"
velocidad_jugador_click = 7

# ================= RUTAS DE SONIDOS Y MÚSICAS (CONFIGURACIÓN) =================
RUTA_ESTRUENDO = os.path.join(CURRENT_PATH, "sonidos", "estruendo.mp3")
RUTA_MUSICA_DESENLACE = os.path.join(CURRENT_PATH, "sonidos", "musica_fondo_final.mp3") # Clímax últimos 15 seg
RUTA_SONIDO_DERROTA_1 = os.path.join(CURRENT_PATH, "sonidos", "agua_corriendo.mp3")
RUTA_SONIDO_DERROTA_2 = os.path.join(CURRENT_PATH, "sonidos", "derrumbe.mp3")
# ==============================================================================

class SalaActualView(arcade.View):
    def __init__(self, sala_instanciada, manager, lim_tiempo):
        super().__init__()
        self.sala = sala_instanciada
        self.manager = manager
        self.texto_inicial = False
        self.sala.InstanciarInterfaces(self)
        
        # --- Control del Temporizador de Sala ---
        self.lim_tiempo = lim_tiempo
        self.tiempo_inicio = None
        self.tiempo_restante = lim_tiempo
        self.tiempo_agotado = False

        # Propiedades del jugador y físicas
        self.jugador = None
        self.jugador_lista = None
        self.motor_fisica = None
        
        # Estado de la interacción
        self.objeto_objetivo = None
        self.moviéndose_por_click = False
        self.objetivo_alcanzado = False
        self.listo_para_interactuar = False

        # Integración de la animación de fondo
        self.current_bg_index = 0
        self.bg_timer = 0.0

        # Variables para la caja de texto emergente
        self.mostrar_cuadro_texto = False
        self.texto_completo = ""       
        self.texto_actual = ""         
        self.indice_letra = 0          
        self.temporizador_letra = 0.0
        self.VELOCIDAD_TEXTO = 0.03    
        self.interfaz_texto = None
        self.reproductor_audio = None

        # --- Control de Estruendos y Audios ---
        self.bandera_estruendo = time.time()
        self.estruendo = arcade.load_sound(RUTA_ESTRUENDO)
        self.volumen_estruendo = 0.2
        self.tempo_estruendo = 7.0   # Empieza espaciado (7s) y bajará hacia 2s

        # Control del clímax final
        self.musica_desenlace = arcade.load_sound(RUTA_MUSICA_DESENLACE)
        self.desenlace_activado = False
        self.reproductor_desenlace = None

        # Objeto de texto del temporizador (Arriba a la derecha)
        self.texto_reloj = None

    def reproducir_estruendo(self):
        arcade.play_sound(self.estruendo, volume=self.volumen_estruendo)

    def sonidos_derrota(self):
        """Secuencia de sonidos ejecutados al consumirse todo el tiempo."""
        try:
            if os.path.exists(RUTA_SONIDO_DERROTA_1):
                arcade.play_sound(arcade.load_sound(RUTA_SONIDO_DERROTA_1), volume=0.8)
            if os.path.exists(RUTA_SONIDO_DERROTA_2):
                arcade.play_sound(arcade.load_sound(RUTA_SONIDO_DERROTA_2), volume=1.0)
        except Exception as e:
            print(f"[Aviso Audio Derrota]: {e}")

    def pausar_estruendo(self):
        if self.reproductor_desenlace:
            arcade.stop_sound(self.reproductor_desenlace)
            self.reproductor_desenlace = None

    def ejecutar_dialogo(self, texto: str, voz: str = "es-ES-AlvaroNeural", velocidad: str = "+0%", tono: str = "+0Hz"):
        self.mostrar_texto(texto)

    def on_show_view(self):
        if self.tiempo_inicio is None:
            self.tiempo_inicio = time.time()
            self.bandera_estruendo = time.time()

        if not self.jugador:
            self.jugador = Ingeniero(center_x=self.sala.posicion_inicial[0], center_y=self.sala.posicion_inicial[1])
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador)

        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador, self.sala.lista_bloqueos)

        self.interfaz_texto = arcade.Text(
            text="",
            x=80,
            y=110,
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Courier New",             
            bold=True,
            multiline=True,
            width=self.window.width - 160
        )

        # Reloj arriba a la derecha
        self.texto_reloj = arcade.Text(
            text="00:00",
            x=consts.ancho_ventana - 85,
            y=consts.alto_ventana - 40,
            color=arcade.color.RED,
            font_size=22,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        if not self.texto_inicial:
            self.ejecutar_dialogo(self.sala.texto_inicial, voz="es-ES-AlvaroNeural", velocidad="+30%", tono="+15Hz")
            self.texto_inicial = True

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S, arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.moviéndose_por_click = False
            self.objeto_objetivo = None

        if key == arcade.key.UP or key == arcade.key.W:
            self.jugador.move_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jugador.move_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jugador.move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.jugador.move_right = True
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.jugador.move_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jugador.move_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jugador.move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.jugador.move_right = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.mostrar_cuadro_texto:
                if self.indice_letra >= len(self.texto_completo):
                    self.mostrar_cuadro_texto = False
                    if self.reproductor_audio:
                        arcade.stop_sound(self.reproductor_audio)
                        self.reproductor_audio = None
                    return

            self.moviéndose_por_click = True
            objetos_cliqueados = arcade.get_sprites_at_point((x, y), self.sala.lista_bloqueos)
            
            if objetos_cliqueados and isinstance(objetos_cliqueados[0], Interactuable):
                self.objeto_objetivo = objetos_cliqueados[0]
                self.jugador.destino_x = self.objeto_objetivo.ubicacion_jugador["x"]
                self.jugador.destino_y = self.objeto_objetivo.ubicacion_jugador["y"]
            else:
                self.objeto_objetivo = None
                self.jugador.destino_x = x
                self.jugador.destino_y = y

    def mostrar_texto(self, mensaje_nuevo):
        self.texto_completo = mensaje_nuevo
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.interfaz_texto.text = ""
        self.mostrar_cuadro_texto = True

    def Escapar(self):
        print("HAS SALIDOOOO")
        self.pausar_estruendo()
        self.window.show_view(self.manager)

    def on_update(self, delta_time: float):
        # 1. Actualización del reloj de tiempo límite
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.tiempo_restante = max(0, self.lim_tiempo - tiempo_transcurrido)

        minutos = int(self.tiempo_restante // 60)
        segundos = int(self.tiempo_restante % 60)
        if self.texto_reloj:
            self.texto_reloj.text = f"{minutos:02d}:{segundos:02d}"

        # 2. Ajuste dinámico de estruendos según el progreso (0.0 al inicio -> 1.0 al final)
        progreso = min(1.0, tiempo_transcurrido / self.lim_tiempo)
        self.volumen_estruendo = 0.2 + (0.6 * progreso)        # Aumenta de 0.2 a 0.8
        self.tempo_estruendo = max(1.5, 7.0 - (5.0 * progreso)) # Reduce el intervalo de 7s a 2s

        # 3. Clímax (Últimos 15 segundos)
        if self.tiempo_restante <= 15.0 and not self.desenlace_activado and not self.tiempo_agotado:
            self.desenlace_activado = True
            if hasattr(self.manager, "pausar_todo"):
                self.manager.pausar_todo()
            elif hasattr(self.manager, "pausar_musica"):
                self.manager.pausar_musica()

            try:
                self.reproductor_desenlace = arcade.play_sound(self.musica_desenlace, volume=0.8, loop=False)
            except Exception as e:
                print(f"[Aviso Desenlace]: {e}")

        # 4. Derrota por límite de tiempo
        if self.tiempo_restante <= 0 and not self.tiempo_agotado:
            self.tiempo_agotado = True
            self.pausar_estruendo()
            self.sonidos_derrota()
            time.sleep(2)
            from game_over import Game_Over
            vista_game_over = Game_Over("agua") # Cambiar a por tiempo
            self.window.show_view(vista_game_over)
            return

        # Animación de fondo
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            self.current_bg_index = (self.current_bg_index + 1) % len(self.sala.fondo_texturas)
            self.sala.fondo_sprite.texture = self.sala.fondo_texturas[self.current_bg_index]

        # Colisiones de eliminación
        if self.sala.lista_eliminadores:
            if arcade.check_for_collision_with_list(self.jugador, self.sala.lista_eliminadores):
                self.pausar_estruendo()
                from game_over import Game_Over
                vista_game_over = Game_Over("agua")
                self.window.show_view(vista_game_over)
                return
            
        # Salida alcanzada
        if arcade.check_for_collision_with_list(self.jugador, self.sala.lista_salida):
            self.Escapar()
            return

        # Movimiento
        if self.jugador.move_left or self.jugador.move_right or self.jugador.move_up or self.jugador.move_down:
            self.jugador.update_por_teclado()
        elif self.moviéndose_por_click:
            if self.jugador.update_por_click():
                self.moviéndose_por_click = False
                if self.objeto_objetivo is not None:
                    self.objetivo_alcanzado = True
        else:
            self.jugador.change_x = 0
            self.jugador.change_y = 0
        
        self.motor_fisica.update()
        
        if self.objeto_objetivo is not None and self.objetivo_alcanzado:
            self.moviéndose_por_click = False
            self.jugador.change_x = 0
            self.jugador.change_y = 0
            self.listo_para_interactuar = True
            self.objetivo_alcanzado = False
                
        if getattr(self, 'listo_para_interactuar', False):
            self.listo_para_interactuar = False
            mueble_actual = self.objeto_objetivo
            self.objeto_objetivo = None 
            mueble_actual.funcion(self)      
        
        if self.mostrar_cuadro_texto and self.indice_letra < len(self.texto_completo):
            self.temporizador_letra += delta_time
            if self.temporizador_letra >= self.VELOCIDAD_TEXTO:
                self.temporizador_letra = 0.0
                self.texto_actual += self.texto_completo[self.indice_letra]
                self.indice_letra += 1
                self.interfaz_texto.text = self.texto_actual

        # Reproducción periódica del estruendo dinámico
        if time.time() - self.bandera_estruendo > self.tempo_estruendo:
            self.reproducir_estruendo()
            self.bandera_estruendo = time.time()

    def on_draw(self):
        self.clear()

        self.sala.fondo_lista.draw()
        self.sala.lista_bloqueos.draw()  
        self.jugador_lista.draw()
        self.sala.interactuables_sprites.draw()
        self.sala.lista_salida.draw()

        # --- Recuadro y Texto del Temporizador (Arriba a la derecha) ---
        ancho_caja = 130
        alto_caja = 50
        margen_der = 20
        margen_arr = 15

        arcade.draw_lbwh_rectangle_filled(
            left=consts.ancho_ventana - ancho_caja - margen_der,
            bottom=consts.alto_ventana - alto_caja - margen_arr,
            width=ancho_caja,
            height=alto_caja,
            color=(0, 0, 0, 220)
        )
        arcade.draw_lbwh_rectangle_outline(
            left=consts.ancho_ventana - ancho_caja - margen_der,
            bottom=consts.alto_ventana - alto_caja - margen_arr,
            width=ancho_caja,
            height=alto_caja,
            color=arcade.color.RED,
            border_width=2
        )

        if self.texto_reloj:
            self.texto_reloj.draw()

        # Cuadro de diálogo
        if self.mostrar_cuadro_texto:
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