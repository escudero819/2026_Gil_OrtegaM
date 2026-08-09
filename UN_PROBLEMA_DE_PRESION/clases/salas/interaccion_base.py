import arcade, os
from configuraciones import Constantes as const
import edge_tts, asyncio, threading

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

class InteraccionBase(arcade.View):
    def __init__(self):
        super().__init__()
        self.centro_x = const.ancho_ventana / 2
        self.centro_y = const.alto_ventana / 2
        self.estado = "indefinido"
        self.fondo = None

        # variables para la logica de la caja de texto emergente
        self.mostrar_cuadro_texto = False
        self.texto_completo = ""       # El texto total que queremos mostrar
        self.texto_actual = ""         # Lo que se va escribiendo en pantalla poco a poco
        self.indice_letra = 0          # En qué letra del string vamos
        
        # Temporizadores para las letras
        self.temporizador_letra = 0.0
        self.VELOCIDAD_TEXTO = 0.03    # Tiempo en segundos entre cada letra (0.03 es ideal)
        
        # El objeto de texto de Arcade
        self.interfaz_texto = None

        # Control de voz (edge-tts / arcade sound player)
        self.reproductor_audio = None

    def ejecutar_dialogo(self, texto: str, voz: str = "es-ES-AlvaroNeural", velocidad: str = "+0%", tono: str = "+0Hz"):
        """
        Ejecuta voz y texto sincronizados.
        - velocidad: p. ej. '+25%' para desesperación/alarma, '-10%' para lentitud.
        - tono: p. ej. '+15Hz' para tono agudo/tembloroso, '-10Hz' para voz grave.
        """
        self.mostrar_texto(texto)

        """
        if voz == "Guia":
            voz = "es-CO-GonzaloNeural"  # Voz de guía en español colombiano

        # Detenemos cualquier audio anterior
        if self.reproductor_audio:
            arcade.stop_sound(self.reproductor_audio)
            self.reproductor_audio = None

        # 1. Crear un nombre único de archivo según el texto y entonación (Sistema de Caché)
        # Usamos hash para que textos iguales reutilicen el mismo MP3 ya descargado
        id_audio = abs(hash(f"{texto}_{voz}_{velocidad}_{tono}"))
        carpeta_cache = os.path.join(CURRENT_PATH, "cache_audio")
        os.makedirs(carpeta_cache, exist_ok=True)
        archivo_audio = os.path.join(carpeta_cache, f"dialogo_{id_audio}.mp3")

        # 2. Si el audio YA EXISTE en caché, se reproduce AL INSTANTE (sin lag)
        if os.path.exists(archivo_audio):
            try:
                audio = arcade.load_sound(archivo_audio)
                self.reproductor_audio = arcade.play_sound(audio)
                return
            except Exception as e:
                print(f"[Aviso Caché] Error cargando audio existente: {e}")

        # 3. Si no existe, lo descargamos asíncronamente en segundo plano
        async def _generar_audio():
            try:
                # Usamos los parámetros rate y pitch nativos en lugar de código XML/SSML
                comunicador = edge_tts.Communicate(
                    text=texto, 
                    voice=voz, 
                    rate=velocidad, 
                    pitch=tono
                )
                await comunicador.save(archivo_audio)
                return True
            except Exception as e:
                print(f"[Aviso Edge-TTS] Error de red al generar voz: {e}")
                return False

        def _hilo_trabajador():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                exito = loop.run_until_complete(_generar_audio())
                loop.close()

                if exito:
                    def _reproducir_en_pantalla(dt):
                        if os.path.exists(archivo_audio):
                            try:
                                audio = arcade.load_sound(archivo_audio)
                                self.reproductor_audio = arcade.play_sound(audio)
                            except Exception as audio_err:
                                print(f"[Aviso Audio] Falló la carga del MP3: {audio_err}")

                    arcade.schedule_once(_reproducir_en_pantalla, 0)
            except Exception as thread_err:
                print(f"[Aviso Hilo Voice] Error secundario ignorado: {thread_err}")

        threading.Thread(target=_hilo_trabajador, daemon=True).start()
        """
    
    def mostrar_texto(self, mensaje_nuevo):
        """ Configura y arranca la animación de letras desde cero """
        self.texto_completo = mensaje_nuevo
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.interfaz_texto.text = ""
        self.mostrar_cuadro_texto = True

    def escalar_interactuable(self, sprite):
        """ Ajusta el tamaño de un sprite para que encaje en la ventana según la escala de la interfaz """
        factor_y = sprite.height / const.alto_interfaces 
        factor_x = sprite.width / const.ancho_interfaces
        factor = min(factor_x, factor_y)
        sprite.height *= factor
        sprite.width *= factor


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
            self.lista_fondo.clear()
        self.lista_fondo.append(fondo)
        print("se cambio el fondo", self.fondo)

    def on_show_view(self):
        # Inicializamos el objeto de texto en la parte inferior de la ventana
        self.interfaz_texto = arcade.Text(
            text="",
            x=80,                          # Margen izquierdo para que no toque el borde de la pantalla
            y=110,                         # Altura interna de la caja de texto
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Courier New",             
            bold=True,
            multiline=True,
            width=self.window.width - 160        # Se adapta al ancho de tu pantalla automáticamente
        )
        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()

    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()
        if self.mostrar_cuadro_texto:
                    ancho_pantalla = self.window.width
                    
                    # Configuramos las coordenadas de la caja usando la esquina inferior izquierda como base
                    margen_izquierdo = 40
                    borde_inferior = 25
                    ancho_caja = ancho_pantalla - 80
                    alto_caja = 110
        
                    # 1. Fondo de la caja (Left, Bottom, Width, Height)
                    arcade.draw_lbwh_rectangle_filled(
                        left=margen_izquierdo,
                        bottom=borde_inferior,
                        width=ancho_caja,
                        height=alto_caja,
                        color=(15, 15, 15, 230)
                    )
                    
                    # 2. Borde de la caja
                    arcade.draw_lbwh_rectangle_outline(
                        left=margen_izquierdo,
                        bottom=borde_inferior,
                        width=ancho_caja,
                        height=alto_caja,
                        color=arcade.color.WHITE,
                        border_width=3
                    )

                    if self.interfaz_texto:
                        self.interfaz_texto.draw()

    def on_update(self, delta_time: float):
             # ANIMACIÓN DE TEXTO GRADUAL (MÁQUINA DE ESCRIBIR)
            if self.mostrar_cuadro_texto:
                # Si todavía faltan letras por escribir del mensaje completo
                if self.indice_letra < len(self.texto_completo):
                    self.temporizador_letra += delta_time
                    
                    # Cuando pasa el tiempo configurado, añadimos el siguiente caracter
                    if self.temporizador_letra >= self.VELOCIDAD_TEXTO:
                        self.temporizador_letra = 0.0
                        self.texto_actual += self.texto_completo[self.indice_letra]
                        self.indice_letra += 1
                        
                        # Actualizamos el contenido visual del objeto de texto
                        self.interfaz_texto.text = self.texto_actual

    def on_mouse_press(self, x, y, button, modifiers):
        if not button == arcade.MOUSE_BUTTON_LEFT:
            return
        if self.estado == "sin objetos":
            self.window.show_view(self.partida)  # Regresa a la vista de la sala principal
        if self.mostrar_cuadro_texto:
            # Si ya se terminó de escribir todo el texto
            if self.indice_letra >= len(self.texto_completo):
                self.mostrar_cuadro_texto = False
                self.texto_completo = ""
                self.texto_actual = ""
                self.indice_letra = 0
                self.temporizador_letra = 0.0
                self.interfaz_texto.text = ""
        if not arcade.get_sprites_at_point((x,y), self.lista_fondo):
            self.window.show_view(self.partida)  # Regresa a la vista de la sala principal