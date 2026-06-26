import arcade, os
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo_con_candado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/con_candado.png")
fondo_sin_candado = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/sin_candado.png")
fondo_abierto = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/abierto.png")
fondo_sin_objetos = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/armario/sin_objetos.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

class ArmarioInterfaz(arcade.View):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "con_candado"
        self.sala = self.partida.sala
        self.centro_x = const.ancho_ventana / 2
        self.centro_y = const.alto_ventana / 2
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
            self.lista_fondo.pop()
        self.lista_fondo.append(fondo)

    def _candados(self):
        cadenas = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y)
        cadenas.width = 200
        cadenas.height = 200
        self.lista_interaccion.append(cadenas)

    def _cad_rotas(self):
        puertas = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y)
        puertas.width = 200
        puertas.height = const.alto_interfaces
        if self.lista_interaccion:
            self.lista_interaccion.clear()
        self.lista_interaccion.append(puertas)
    
    def _abierto(self):
        objetos = arcade.Sprite(transparente, center_x=self.centro_x, center_y= self.centro_y + self.fondo.height/8 - 40)
        objetos.width = self.fondo.height / 2
        objetos.height = 200
        if self.lista_interaccion:
            self.lista_interaccion.clear()
        self.lista_interaccion.append(objetos)
    
    def _sin_obj(self):
        if self.lista_interaccion:
            self.lista_interaccion.clear()

    def on_show_view(self):

        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()
        if not self.fondo:
            self.cambiar_fondo(fondo_con_candado)
        else:
            self.cambiar_fondo(self.fondo)
        if self.estado == "con_candado":
            self._candados()
        
        elif self.estado == "sin_candado":
            self._cad_rotas()

        elif self.estado == "abierto":
            self._abierto()

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
    

    def mostrar_texto(self, mensaje_nuevo):
        """ Configura y arranca la animación de letras desde cero """
        self.texto_completo = mensaje_nuevo
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.interfaz_texto.text = ""
        self.mostrar_cuadro_texto = True
    
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
            
            # 3. Renderizar las letras que se están escribiendo
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
        if self.mostrar_cuadro_texto:
                 # Si ya se terminó de escribir todo el texto
                if self.indice_letra >= len(self.texto_completo):
                    self.mostrar_cuadro_texto = False  # Oculta la caja y deja seguir jugando
        
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if self.estado != "sin_objetos":
                if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                    if self.estado == "con_candado":
                        if self.sala.inventario.consultar("pinzas"):
                            self.cambiar_fondo(fondo_sin_candado)
                            self._cad_rotas()
                            self.estado = "sin_candado"
                        else:
                            self.mostrar_texto('"cerrado... pero creo que puedo cortarlas con alguna herramienta"')
                    elif self.estado == "sin_candado":
                        self.cambiar_fondo(fondo_abierto)
                        self._abierto()
                        self.estado = "abierto"
                    else:
                        self.cambiar_fondo(fondo_sin_objetos)
                        self.sala.inventario.agregar_objeto("cables")
                        mensaje = "has conseguido cables y guantes"
                        self.mostrar_texto(mensaje)
                        self._sin_obj()
                        self.estado = "sin_objetos"
            else:
                self.window.show_view(self.partida)
        else:
            self.window.show_view(self.partida)