import arcade
import os
from configuraciones import Constantes as const
from clases.salas.interaccion_base import InteraccionBase

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# Texturas del puzzle
fondo_circuito = arcade.load_texture(os.path.join(CURRENT_PATH, "texturas/interfaces/circuito/circuito.png"))
tex_res_100 = arcade.load_texture(os.path.join(CURRENT_PATH, "texturas/interfaces/circuito/res_100x.png"))
tex_res_150 = arcade.load_texture(os.path.join(CURRENT_PATH, "texturas/interfaces/circuito/res_150x.png"))
tex_res_200 = arcade.load_texture(os.path.join(CURRENT_PATH, "texturas/interfaces/circuito/res_200x.png"))
tex_transistor = arcade.load_texture(os.path.join(CURRENT_PATH, "texturas/interfaces/circuito/transistorx.png"))
tex_transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))


class CircuitoMontacargasInterfaz(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = self.partida.sala
        
        # Estados del puzzle: "incompleto" -> "iniciado" -> "trans_col"
        self.estado_puzzle = "incompleto"
        
        # Control de componentes colocados en la base
        self.resistencia_100_puesta = False
        self.resistencia_150_puesta = False
        self.resistencia_200_puesta = False
        
        self.transistor1_puesto = False
        self.transistor2_puesto = False

        # Referencias a los sprites de las 3 resistencias base de la derecha
        self.sprite_base_100 = None
        self.sprite_base_150 = None
        self.sprite_base_200 = None

        # ---------------------------------------------------------------------
        # 📌 REGULADOR DE REGULACIÓN Y COLOR DE RESISTENCIAS
        # Cambia estos valores RGB para ajustar la intensidad de oscurecimiento
        # ---------------------------------------------------------------------
        self.COLOR_OSCURO = (100, 100, 100)      # RESISTENCIA DESSELECCIONADA / APAGADA
        self.COLOR_SELECCIONADO = (255, 255, 255) # RESISTENCIA SELECCIONADA / BRILLANTE

        # Selección de resistencia activa ("100", "150", "200" o None)
        self.resistencia_seleccionada = None

        # Variables de voltaje del puzzle
        self.VOLTAJE_INICIAL = 50
        self.voltaje_actual = self.VOLTAJE_INICIAL
        self.texto_voltaje = None

        # Mapeo de valores de voltaje reducidos
        self.VALORES_RESISTENCIAS = {
            "100": -3,
            "150": -7,
            "200": -10
        }

        # Seguimiento del estado del PCB (4 slots)
        # Almacena el valor numérico (-3, -7, -10) en cada posición [slot_0, slot_1, slot_2, slot_3]
        self.valores_resistencias_puestas = [None, None, None, None]
        # Almacena las referencias a los Sprites colocados dentro del PCB para poder reemplazarlos o redibujarlos
        self.sprites_resistencias_pcb = [None, None, None, None]

        # Listas de Sprites
        self.lista_componentes = arcade.SpriteList()
        self.sprites_transistores_siluetas = arcade.SpriteList()
        self.sprites_ranuras_siluetas = arcade.SpriteList()

        # Coordenadas fijas de colocación de las 3 resistencias iniciales (derecha)
        self.POS_RESISTENCIA_100 = (940, 514)
        self.POS_RESISTENCIA_150 = (940, 388)
        self.POS_RESISTENCIA_200 = (940, 260)

        # Ubicaciones y dimensiones de los transistores
        self.POS_TRANSISTOR_1 = (484, 400)
        self.POS_TRANSISTOR_2 = (684, 400)
        self.ANCHO_SILUETA_TRANSISTOR = 60
        self.ALTO_SILUETA_TRANSISTOR = 90

        # Posiciones de las 4 ranuras de resistencias dentro del PCB
        self.POS_RANURAS_PCB = [
            (605, 570),  # Ranura 0 (Superior)
            (605, 500),  # Ranura 1 (Media-Superior)
            (607, 312),  # Ranura 2 (Media-Inferior)
            (607, 262)   # Ranura 3 (Inferior)
        ]

        self.ANCHO_RANURA_SLOT = 70
        self.ALTO_RANURA_SLOT = 20

        # Ubicación en pantalla del indicador de voltaje
        self.POS_TEXTO_VOLTAJE = (320, 530)

        # Referencias a los sprites transparentes
        self.silueta_trans_1 = None
        self.silueta_trans_2 = None

    # ----------------------------------------------------------------------
    # MÉTODOS PRIVADOS PARA COLOCAR RESISTENCIAS INICIALES
    # ----------------------------------------------------------------------
    def _colocar_resistencia_100(self):
        self.sprite_base_100 = arcade.Sprite(tex_res_100, center_x=self.POS_RESISTENCIA_100[0], center_y=self.POS_RESISTENCIA_100[1])
        self.lista_componentes.append(self.sprite_base_100)
        self.resistencia_100_puesta = True
        print("Resistencia 100Ω colocada.")
        self._verificar_resistencias_completas()

    def _colocar_resistencia_150(self):
        self.sprite_base_150 = arcade.Sprite(tex_res_150, center_x=self.POS_RESISTENCIA_150[0], center_y=self.POS_RESISTENCIA_150[1])
        self.lista_componentes.append(self.sprite_base_150)
        self.resistencia_150_puesta = True
        print("Resistencia 150Ω colocada.")
        self._verificar_resistencias_completas()

    def _colocar_resistencia_200(self):
        self.sprite_base_200 = arcade.Sprite(tex_res_200, center_x=self.POS_RESISTENCIA_200[0], center_y=self.POS_RESISTENCIA_200[1])
        self.lista_componentes.append(self.sprite_base_200)
        self.resistencia_200_puesta = True
        print("Resistencia 200Ω colocada.")
        self._verificar_resistencias_completas()

    def _verificar_resistencias_completas(self):
        if self.resistencia_100_puesta and self.resistencia_150_puesta and self.resistencia_200_puesta:
            self.estado_puzzle = "iniciado"
            print("Las 3 resistencias colocadas. Estado del puzzle: INICIADO")
            self._generar_siluetas_transistores()

    # ----------------------------------------------------------------------
    # MÉTODO PRIVADO PARA GENERAR SILUETAS INVISIBLES DE TRANSISTORES
    # ----------------------------------------------------------------------
    def _generar_siluetas_transistores(self):
        self.sprites_transistores_siluetas.clear()

        self.silueta_trans_1 = arcade.Sprite(
            tex_transparente, 
            center_x=self.POS_TRANSISTOR_1[0], 
            center_y=self.POS_TRANSISTOR_1[1]
        )
        self.silueta_trans_1.width = self.ANCHO_SILUETA_TRANSISTOR
        self.silueta_trans_1.height = self.ALTO_SILUETA_TRANSISTOR

        self.silueta_trans_2 = arcade.Sprite(
            tex_transparente, 
            center_x=self.POS_TRANSISTOR_2[0], 
            center_y=self.POS_TRANSISTOR_2[1]
        )
        self.silueta_trans_2.width = self.ANCHO_SILUETA_TRANSISTOR
        self.silueta_trans_2.height = self.ALTO_SILUETA_TRANSISTOR

        self.sprites_transistores_siluetas.append(self.silueta_trans_1)
        self.sprites_transistores_siluetas.append(self.silueta_trans_2)
        
        self.lista_interaccion.append(self.silueta_trans_1)
        self.lista_interaccion.append(self.silueta_trans_2)
        print("Siluetas invisibles de transistores cargadas en el mapa.")

    # ----------------------------------------------------------------------
    # GENERACIÓN DE LAS 4 RANURAS DEL PCB Y EL INDICADOR DE VOLTAJE INICIAL (40V)
    # ----------------------------------------------------------------------
    def _generar_ranuras_puzzle(self):
        """ Genera las 4 hitboxes transparentes del PCB, oscurece las resistencias base e inicia el voltaje a 40V """
        self.sprites_ranuras_siluetas.clear()

        for pos in self.POS_RANURAS_PCB:
            sprite_ranura = arcade.Sprite(tex_transparente, center_x=pos[0], center_y=pos[1])
            sprite_ranura.width = self.ANCHO_RANURA_SLOT
            sprite_ranura.height = self.ALTO_RANURA_SLOT
            self.sprites_ranuras_siluetas.append(sprite_ranura)
            self.lista_interaccion.append(sprite_ranura)

        # Aplicar tono oscuro por defecto a los 3 componentes base
        if self.sprite_base_100:
            self.sprite_base_100.color = self.COLOR_OSCURO
        if self.sprite_base_150:
            self.sprite_base_150.color = self.COLOR_OSCURO
        if self.sprite_base_200:
            self.sprite_base_200.color = self.COLOR_OSCURO

        # Creación del texto dinámico de voltaje inicializado a 40V
        self.texto_voltaje = arcade.Text(
            text=f"{self.voltaje_actual}V",
            x=self.POS_TEXTO_VOLTAJE[0],
            y=self.POS_TEXTO_VOLTAJE[1],
            color=arcade.color.GREEN,
            font_size=24,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )
        print("Ranuras del puzzle generadas, componentes oscurecidos e indicador a 40V iniciado.")

    # ----------------------------------------------------------------------
    # CONTROL PÚBLICO DEL VOLTAJE Y COMPROBACIÓN DE VICTORIA
    # ----------------------------------------------------------------------
    def actualizar_voltaje(self):
        """ Recalcula el voltaje sumando las reducciones aplicadas y actualiza el texto """
        suma_reducciones = sum([val for val in self.valores_resistencias_puestas if val is not None])
        self.voltaje_actual = self.VOLTAJE_INICIAL + suma_reducciones

        if self.texto_voltaje:
            self.texto_voltaje.text = f"{self.voltaje_actual}V"

        print(f"[Voltaje] Actual: {self.voltaje_actual}V | Historial en PCB: {self.valores_resistencias_puestas}")

        # Comprobar condición de victoria: 4 resistencias colocadas y exactamente 24V
        resistencias_puestas_count = sum(1 for val in self.valores_resistencias_puestas if val is not None)
        if resistencias_puestas_count == 4 and self.voltaje_actual == 24:
            print("puzzle completado")

    # ----------------------------------------------------------------------
    # LÓGICA PRIVADA DE SELECCIÓN DE COMPONENTES BASE Y COLOCACIÓN EN EL PCB
    # ----------------------------------------------------------------------
    def _seleccionar_resistencia_base(self, tipo: str):
        """ Modifica la intensidad del color según la selección activa """
        self.resistencia_seleccionada = tipo

        # Resetear los 3 sprites al color oscuro por defecto
        if self.sprite_base_100:
            self.sprite_base_100.color = self.COLOR_OSCURO
        if self.sprite_base_150:
            self.sprite_base_150.color = self.COLOR_OSCURO
        if self.sprite_base_200:
            self.sprite_base_200.color = self.COLOR_OSCURO

        # Elevar intensidad / brillo al componente seleccionado
        if tipo == "100" and self.sprite_base_100:
            self.sprite_base_100.color = self.COLOR_SELECCIONADO
        elif tipo == "150" and self.sprite_base_150:
            self.sprite_base_150.color = self.COLOR_SELECCIONADO
        elif tipo == "200" and self.sprite_base_200:
            self.sprite_base_200.color = self.COLOR_SELECCIONADO

        print(f"[Selección] Resistencia {tipo}Ω seleccionada.")

    def _colocar_resistencia_en_ranura(self, indice_ranura: int):
        """ Coloca una copia escalada a 0.5 en la ranura indicada y registra su valor numérico """
        if self.resistencia_seleccionada is None:
            return

        # Seleccionar la textura correspondiente
        texturas = {
            "100": tex_res_100,
            "150": tex_res_150,
            "200": tex_res_200
        }
        tex = texturas[self.resistencia_seleccionada]
        pos = self.POS_RANURAS_PCB[indice_ranura]

        # Si ya había un sprite en esa ranura, lo eliminamos
        if self.sprites_resistencias_pcb[indice_ranura] is not None:
            self.lista_componentes.remove(self.sprites_resistencias_pcb[indice_ranura])

        # Crear nuevo sprite escalado a 0.75
        nuevo_sprite = arcade.Sprite(tex, center_x=pos[0], center_y=pos[1])
        nuevo_sprite.scale = 0.75
        
        self.sprites_resistencias_pcb[indice_ranura] = nuevo_sprite
        self.lista_componentes.append(nuevo_sprite)

        # Guardar valor numérico (-3, -7, -10) en la lista
        self.valores_resistencias_puestas[indice_ranura] = self.VALORES_RESISTENCIAS[self.resistencia_seleccionada]

        # Actualizar el voltaje dinámico
        self.actualizar_voltaje()

    # ----------------------------------------------------------------------
    # MÉTODOS PRIVADOS PARA COLOCAR Y PROCESAR TRANSISTORES
    # ----------------------------------------------------------------------
    def _colocar_transistor_1(self):
        sprite = arcade.Sprite(tex_transistor, center_x=self.POS_TRANSISTOR_1[0], center_y=self.POS_TRANSISTOR_1[1])
        self.lista_componentes.append(sprite)
        self.transistor1_puesto = True
        print("Transistor colocado en la posición izquierda.")
        self._verificar_transistores_completos()

    def _colocar_transistor_2(self):
        sprite = arcade.Sprite(tex_transistor, center_x=self.POS_TRANSISTOR_2[0], center_y=self.POS_TRANSISTOR_2[1])
        self.lista_componentes.append(sprite)
        self.transistor2_puesto = True
        print("Transistor colocado en la posición derecha.")
        self._verificar_transistores_completos()

    def _verificar_transistores_completos(self):
        if self.transistor1_puesto and self.transistor2_puesto:
            self.estado_puzzle = "trans_col"
            print("Ambos transistores colocados. Estado del puzzle: TRANS_COL")
            self._generar_ranuras_puzzle()

    def _intentar_colocar_transistor(self, slot: int):
        if (slot == 1 and self.transistor1_puesto) or (slot == 2 and self.transistor2_puesto):
            return

        puestos_actuales = (1 if self.transistor1_puesto else 0) + (1 if self.transistor2_puesto else 0)

        if puestos_actuales == 0:
            if self.sala.inventario.consultar("transistor1"):
                if slot == 1:
                    self._colocar_transistor_1()
                else:
                    self._colocar_transistor_2()
            else:
                self.ejecutar_dialogo('"no lo tengo"')

        elif puestos_actuales == 1:
            if self.sala.inventario.consultar("transistor2"):
                if slot == 1:
                    self._colocar_transistor_1()
                else:
                    self._colocar_transistor_2()
            else:
                self.ejecutar_dialogo('"no lo tengo"')

    # ----------------------------------------------------------------------
    # EVENTOS DE CICLO DE VIDA Y RENDERIZADO
    # ----------------------------------------------------------------------
    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(fondo_circuito)

    def on_draw(self):
        super().on_draw()
        self.lista_componentes.draw()

        if self.texto_voltaje:
            self.texto_voltaje.draw()

    # ----------------------------------------------------------------------
    # LÓGICA DE INTERACCIÓN
    # ----------------------------------------------------------------------
    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Avanzar diálogo si está activo
        if self.mostrar_cuadro_texto:
            super().on_mouse_press(x, y, button, modifiers)
            return

        # Clic fuera del panel de fondo -> regresar a la sala
        if not arcade.get_sprites_at_point((x, y), self.lista_fondo):
            self.window.show_view(self.partida)
            return

        # 1. ETAPA INICIAL: Colocación de resistencias iniciales al hacer clic en el fondo
        if self.estado_puzzle == "incompleto":
            self._procesar_intento_resistencias()
            return

        # 2. ETAPA "INICIADO": Colocación de transistores tocando sus siluetas
        if self.estado_puzzle == "iniciado":
            siluetas_tocadas = arcade.get_sprites_at_point((x, y), self.sprites_transistores_siluetas)
            
            if siluetas_tocadas:
                silueta = siluetas_tocadas[0]
                if silueta == self.silueta_trans_1:
                    self._intentar_colocar_transistor(slot=1)
                elif silueta == self.silueta_trans_2:
                    self._intentar_colocar_transistor(slot=2)

        # 3. ETAPA "TRANS_COL": Selección de resistencias base e inserción en el PCB
        if self.estado_puzzle == "trans_col":
            # A. Comprobar si tocó alguno de los 3 componentes base usando collides_with_point
            if self.sprite_base_100 and self.sprite_base_100.collides_with_point((x, y)):
                self._seleccionar_resistencia_base("100")
                return

            if self.sprite_base_150 and self.sprite_base_150.collides_with_point((x, y)):
                self._seleccionar_resistencia_base("150")
                return

            if self.sprite_base_200 and self.sprite_base_200.collides_with_point((x, y)):
                self._seleccionar_resistencia_base("200")
                return

            # B. Comprobar si tocó alguna de las 4 ranuras del PCB
            ranuras_tocadas = arcade.get_sprites_at_point((x, y), self.sprites_ranuras_siluetas)
            if ranuras_tocadas:
                ranura_sprite = ranuras_tocadas[0]
                indice_ranura = self.sprites_ranuras_siluetas.index(ranura_sprite)
                self._colocar_resistencia_en_ranura(indice_ranura)

    def _procesar_intento_resistencias(self):
        # Resistencia 100Ω
        if not self.resistencia_100_puesta and self.sala.inventario.consultar("resistencia_100"):
            self._colocar_resistencia_100()

        # Resistencia 150Ω
        if not self.resistencia_150_puesta and self.sala.inventario.consultar("resistencia_150"):
            self._colocar_resistencia_150()

        # Resistencia 200Ω
        if not self.resistencia_200_puesta and self.sala.inventario.consultar("resistencia_200"):
            self._colocar_resistencia_200()
        
        if self.estado_puzzle == "incompleto":
            self.ejecutar_dialogo('"Todavía me faltan resistencias."')