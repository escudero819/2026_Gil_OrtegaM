import arcade, os, time, math
from configuraciones import Constantes as const
from clases.salas.interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
#cargar imagenes

sin_elementos_1 = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/sin_elem_1.png")
sin_elementos_2 = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/sin_elem_2.png")
con_elementos = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/con_elem.png")
cortados = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/cortados.png")
cable = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/cable.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

NODOS_IZQUIERDA = {
    "triangulo": (370, 530),
    "cuadrado":  (370, 455),
    "circulo":   (370, 380),
    "rombo":     (370, 305)
}

NODOS_DERECHA = {
    "A": (930, 525),
    "B": (930, 450),
    "C": (930, 375),
    "D": (930, 300)
}

# La solución del puzzle (qué figura va con qué letra)
SOLUCION_CORRECTA = {
    "triangulo": "D",
    "cuadrado":  "B",
    "circulo":   "A",
    "rombo":     "C"
}
class PanelInterfaz(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "sin_elem"
        self.sala = self.partida.sala
        self.parpadeo = 1.5
        self.fondo_parpadeo = False
        self.timer = time.time()
        self.interfaz_texto = None

        # para logica puzzle
        self.puzzle_activo = False  # Cambia a True cuando "cortas" los cables y pones los elementos
        self.seleccion_izquierda = None  # Almacena un string (ej: "cuadrado")
        self.conexiones_hechas = {}      # Guardará pares hechos por el jugador, ej: {"cuadrado": "C"}
        # Diccionarios separados para los botones funcionales
        self.sprites_botones_izq = {}
        self.sprites_botones_der = {}

        self.botones_cargados = False

    def verificar_puzzle(self):
        # Si todavía no conectó las 4 figuras, no puede haber ganado aún
        if len(self.conexiones_hechas) < 4:
            return

        # Comparamos paso a paso
        for figura, letra_correcta in SOLUCION_CORRECTA.items():
            # Si la figura no está conectada o está en la letra incorrecta, salimos
            if figura not in self.conexiones_hechas or self.conexiones_hechas[figura] != letra_correcta:
                print("Hay conexiones erróneas o incompletas.")
                return

        # ¡SI PASÓ EL BUCLE, GANÓ!
        print("¡Puzzle Completado con Éxito! Presión regulada.")
        mensaje = '"vamos!!! eh logrado arreglar el panel!"'
        self.ejecutar_dialogo(mensaje)
        self.sala.PanelResuelto()

    def _colocar_elem(self):
        self.lista_interaccion.clear()
        print(self.fondo)
        elementos = arcade.Sprite(transparente, center_x= self.centro_x, center_y= self.centro_y - const.alto_interfaces / 4)
        elementos.width = self.fondo.width
        elementos.height = 200
        self.lista_interaccion.append(elementos)

    def _botones(self):
        try:
            for figura, ubicacion in NODOS_IZQUIERDA.items():
                sprite = arcade.Sprite(transparente, center_x= ubicacion[0], center_y= ubicacion[1])
                sprite.width = 50
                sprite.height = 50
                lista = arcade.SpriteList()
                lista.append(sprite)
                self.sprites_botones_izq[figura] = lista

            for letra, ubicacion in NODOS_DERECHA.items():
                sprite = arcade.Sprite(transparente, center_x= ubicacion[0], center_y= ubicacion[1])
                sprite.width = 50
                sprite.height = 50
                lista = arcade.SpriteList()
                lista.append(sprite)
                self.sprites_botones_der[letra] = lista
            self.botones_cargados = True
            self.lista_cables = arcade.SpriteList()
            print("se cargaron los botones")
        except:
            print("falla al cargar botones")

    def crear_cable_estirado(self, x1, y1, x2, y2):
        # 1. Calcular el punto medio (Centro del sprite)
        centro_x = (x1 + x2) / 2
        centro_y = (y1 + y2) / 2
        
        # 2. Calcular la distancia (Longitud del cable usando Pitágoras)
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # 3. Calcular el ángulo de inclinación en radianes y pasarlo a grados
        radianes = math.atan2(y2 - y1, x2 - x1)
        grados = math.degrees(radianes)
        
        # 4. Instanciar el Sprite con la textura base
        cable_sprite = arcade.Sprite(cable)
        
        # 5. Aplicar las transformaciones geométricas
        cable_sprite.center_x = centro_x
        cable_sprite.center_y = centro_y
        cable_sprite.width = distancia     # Forzamos a que se estire hasta alcanzar el otro extremo
        cable_sprite.angle = grados  * -1      # Rotamos el sprite para que apunte exactamente al nodo
        
        # Si tu cable original es muy grueso o fino, puedes ajustar su alto de forma fija aquí:
        # cable_sprite.height = 12 
        
        return cable_sprite

    def on_show_view(self):
        super().on_show_view()
        if not self.fondo:
            self.cambiar_fondo(sin_elementos_1)
        else:
            self.cambiar_fondo(self.fondo)
        
        if self.estado == "sin_elem":
            self._colocar_elem()

        if self.botones_cargados:
            self._botones()
            self.lista_cables = arcade.SpriteList()

    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()

        if self.estado == "cortados":
            if self.botones_cargados:
                self.lista_cables.draw()
                for lista in self.sprites_botones_izq.values():
                    lista.draw()

                for lista in self.sprites_botones_der.values():
                    lista.draw()

                # --- RECORREMOS LAS CONEXIONES HECHAS PARA DIBUJAR LOS CÍRCULOS ---
                for figura, letra in self.conexiones_hechas.items():
                    # SOLUCIÓN: Buscamos las coordenadas reales usando los diccionarios globales
                    punto_inicio = NODOS_IZQUIERDA[figura]
                    punto_fin = NODOS_DERECHA[letra]
                    
                    # Dibujamos el círculo del extremo izquierdo (Figura)
                    # Ajusté el radio a 6 y removí el desfase de -25 para que coincida justo en la punta
                    arcade.draw_circle_filled(
                        center_x=punto_inicio[0] - 5, 
                        center_y=punto_inicio[1], 
                        radius=15, 
                        color=arcade.color.COPPER_RED
                    )
                    
                    # Dibujamos el círculo del extremo derecho (Letra)
                    arcade.draw_circle_filled(
                        center_x=punto_fin[0] + 5, 
                        center_y=punto_fin[1], 
                        radius=15, 
                        color=arcade.color.COPPER_RED
                    )

                # 3. Retroalimentación visual: Si seleccionó una figura, hacemos que "brille" su punta
                if self.seleccion_izquierda:
                    lista_boton = self.sprites_botones_izq[self.seleccion_izquierda]
                    arcade.draw_circle_outline(lista_boton[0].center_x, lista_boton[0].center_y, 15, arcade.color.CYAN, border_width=2)

    def on_update(self, delta: float):
        super().on_update(delta)
        if self.estado == "sin_elem":
            if time.time() - self.timer >= self.parpadeo:
                if self.fondo_parpadeo:
                    print("cambio")
                    self.cambiar_fondo(sin_elementos_1)
                    self.fondo_parpadeo = False
                else:
                    print("cambio")
                    self.cambiar_fondo(sin_elementos_2)
                    self.fondo_parpadeo = True
                self.timer = time.time()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if self.estado == "sin_elem":
                if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                    if self.sala.inventario.consultar("cables"):
                        self.lista_interaccion.clear()
                        self.cambiar_fondo(con_elementos)
                        self.estado = "con_elem"
                        print("con_elem")
                    else:
                        mensaje = '"no lo tengo"'
                        self.ejecutar_dialogo(mensaje)
            elif self.estado == "con_elem":
                self.cambiar_fondo(cortados)
                self._botones()
                self.estado = "cortados"
            else:
                cable_clickeado = arcade.get_sprites_at_point((x,y), self.lista_cables)
                if cable_clickeado:
                    self.lista_cables.remove(cable_clickeado[0])
                    return
                # --- 1. VERIFICAR CLICKS EN LA IZQUIERDA (FIGURAS) ---
                for figura, lista_boton in self.sprites_botones_izq.items():
                    # Creamos una caja invisible de colisión de 60x60 píxeles alrededor del nodo
                    if arcade.get_sprites_at_point((x, y), lista_boton):
                        self.seleccion_izquierda = figura
                        print(f"Seleccionaste: {figura}. Ahora elige una letra.")
                        return # Cortamos para que no evalúe nada más en este frame

                # --- 2. VERIFICAR CLICKS EN LA DERECHA (LETRAS) ---
                if self.seleccion_izquierda is not None:
                    for letra, lista_boton in self.sprites_botones_der.items():
                        if arcade.get_sprites_at_point((x, y), lista_boton):
                            # El jugador tocó una letra teniendo una figura ya seleccionada
                            print(f"Conectando {self.seleccion_izquierda} con {letra}")

                            # Obtenemos los dos extremos matemáticos
                            lista_inicio = self.sprites_botones_izq[self.seleccion_izquierda]
                            punto_inicio = (lista_inicio[0].center_x, lista_inicio[0].center_y)
                            lista_fin = self.sprites_botones_der[letra]
                            punto_fin = (lista_fin[0].center_x, lista_fin[0].center_y)
                            
                            # Generamos el sprite estirado dinámicamente
                            nuevo_cable = self.crear_cable_estirado(punto_inicio[0], punto_inicio[1], punto_fin[0], punto_fin[1])
                            
                            # Lo añadimos a la lista de renderizado
                            self.lista_cables.append(nuevo_cable)
                            
                            # También guardas el registro en tu diccionario interno para saber que esa figura ya se usó
                            self.conexiones_hechas[self.seleccion_izquierda] = letra
                            # Reseteamos la selección para la próxima conexión
                            self.seleccion_izquierda = None
                            
                            # Verificar si completó el puzzle entero
                            self.verificar_puzzle()
                            return
        else:
            self.window.show_view(self.partida)