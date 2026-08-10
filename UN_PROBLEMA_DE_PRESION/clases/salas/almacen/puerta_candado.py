import os
import arcade
from configuraciones import Constantes as const
from clases.salas.interaccion_base import InteraccionBase

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------------------------------------------------
# CARGA DE RECURSOS (Rutas relativas a tu estructura de proyecto)
# -----------------------------------------------------------------------------
FONDO_CANDADO = os.path.join(CURRENT_PATH, "texturas", "interfaces", "candado", "candado.png")
fondo = arcade.load_texture(FONDO_CANDADO)

# Carga de las 10 texturas numéricas del 0 al 9
TEXTURAS_NUMEROS = [
    arcade.load_texture(os.path.join(CURRENT_PATH, "texturas", "interfaces", "candado", f"num_{i}.png"))
    for i in range(10)
]

codigo_correcto = [4, 7, 9]  # Código de 3 dígitos requerido para desbloquear la reja

class CandadoInterfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = self.partida.sala
        
        # Código de 3 dígitos requerido para desbloquear la reja
        self.codigo_correcto = codigo_correcto
        
        # Estado actual de los 3 tambores numéricos (empiezan en 0-0-0)
        self.valores_actuales = [0, 0, 0]
        
        # Lista de los 3 sprites de los tambores interactivos
        self.sprites_digitos = []
        self.resuelto = False

    def setup_digitos(self):
        """
        Crea y posiciona los 3 sprites numéricos sobre las ranuras del candado de la imagen.
        """
        self.lista_interaccion.clear()
        self.sprites_digitos.clear()

        # Coordenadas relativas ajustadas a la posición del candado
        offset_y = -20
        posiciones_x = [
            self.centro_x + 102,  # Rojo (Primer dígito)
            self.centro_x + 150,  # Verde (Segundo dígito)
            self.centro_x + 195   # Azul (Tercer dígito)
        ]

        # Calculamos el factor de escala global UNA SOLA VEZ basándonos en la pantalla
        factor_x = const.ancho_interfaces / fondo.width
        factor_y = const.alto_interfaces / fondo.height
        factor_pantalla = min(factor_x, factor_y)
        
        # Escala final combinada (factor de pantalla * tu escala individual deseada)
        escala_final = factor_pantalla * 0.7

        for i in range(3):
            # Asignamos la textura original sin alterarla
            textura_inicial = TEXTURAS_NUMEROS[self.valores_actuales[i]]
            sprite_digito = arcade.Sprite(textura_inicial)
            
            # Aplicamos la escala al SPRITE (no a la textura)
            sprite_digito.scale = escala_final
            
            sprite_digito.center_x = posiciones_x[i]
            sprite_digito.center_y = self.centro_y + offset_y

            self.sprites_digitos.append(sprite_digito)
            self.lista_interaccion.append(sprite_digito)

    def on_show_view(self):
        super().on_show_view()
        # Establece la imagen de la reja con el candado como fondo
        self.cambiar_fondo(fondo)
        self.setup_digitos()

    def _verificar_codigo(self):
        """
        Método privado que evalúa si la combinación ingresada es la correcta.
        """
        if self.valores_actuales == self.codigo_correcto:
            self.resuelto = True
            print("[Candado] ¡Combinación correcta!")
            self.sala._Reja_Abierta()  # Llama al método de la sala para desbloquear la reja
            

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Si el cuadro de texto está activo, el click avanza/cierra el diálogo
        if self.mostrar_cuadro_texto:
            super().on_mouse_press(x, y, button, modifiers)
            return

        # Comprobar si se hizo click fuera de la interfaz para volver a la sala jugable
        if not arcade.get_sprites_at_point((x, y), self.lista_fondo):
            self.window.show_view(self.partida)
            return

        # -----------------------------------------------------------------------------
        # 1. VERIFICACIÓN DE INVENTARIO
        # -----------------------------------------------------------------------------
        tiene_codigo = False
        tiene_codigo = self.sala.inventario.consultar("cod_candado")
        print(self.sala.inventario.lista_objetos)
        if not tiene_codigo:
            self.ejecutar_dialogo('"No tiene sentido adivinar números a lo loco sin encontrar una pista."')
            return

        # Si ya está resuelto, no se permite seguir girando los tambores
        if self.resuelto:
            return

        # ----------------------------------------
        # -----------------------------------------------------------------------------
        sprites_tocados = arcade.get_sprites_at_point((x, y), self.lista_interaccion)
        
        for sprite in sprites_tocados:
            if sprite in self.sprites_digitos:
                indice = self.sprites_digitos.index(sprite)
                
                # Incrementa el número actual de 0 a 9 y reinicia en 0 (bucle circular)
                self.valores_actuales[indice] = (self.valores_actuales[indice] + 1) % 10
                
                # Al cambiar sprite.texture, Arcade conserva el sprite.scale asignado en setup_digitos
                sprite.texture = TEXTURAS_NUMEROS[self.valores_actuales[indice]]
                print(f"[Candado] Estado actual: {self.valores_actuales}")

                # Evalúa si la nueva combinación resuelve el acertijo
                self._verificar_codigo()
                break