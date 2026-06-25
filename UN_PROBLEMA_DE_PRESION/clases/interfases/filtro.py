import arcade

class modo_filtro:
    def __init__(self, ancho=None, alto=None, color=(192, 192, 192), alfa=100, visible=True):
        # Si no se recibe ancho/alto, intentar obtener la ventana actual de arcade
        if ancho is None or alto is None:
            try:
                vent = arcade.get_window()
                if vent is not None:
                    if ancho is None:
                        ancho = vent.width
                    if alto is None:
                        alto = vent.height
            except Exception:
                pass

        # Guardar valores (pueden ser None para indicar "usar ventana actual")
        self.ancho = ancho
        self.alto = alto
        self.color = tuple(color)
        self.alfa = int(alfa)  # 0-255
        self.visible = bool(visible)

    def dibujar(self):
        if not self.visible:
            return
        # Preferir las dimensiones proporcionadas; si son None, leer la ventana activa
        a = self.ancho
        al = self.alto
        try:
            vent = arcade.get_window()
            if vent is not None:
                if a is None:
                    a = vent.width
                if al is None:
                    al = vent.height
        except Exception:
            pass

        if not a or not al:
            return

        arcade.draw_lrbt_rectangle_filled(0, a, 0, al, (self.color[0], self.color[1], self.color[2], self.alfa))

    def alternar(self):
        self.visible = not self.visible

    def mostrar(self):
        self.visible = True

    def ocultar(self):
        self.visible = False

    def establecer_color(self, tupla_color):
        self.color = tuple(tupla_color)

    def establecer_alfa(self, alfa):
        self.alfa = int(alfa)

    def redimensionar(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
