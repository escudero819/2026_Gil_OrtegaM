from pedido import Pedido
import modo_stock
pedido_actual = Pedido(1)
orden1 = {
    "nombre": "1 bocha",
    "sabores": ["Frutilla"],
    "precio": 700
}
orden2 = {
    "nombre": "1 bocha",
    "sabores": ["Banana"],
    "precio": 700
}
pedido_actual.Añadir(orden1)
pedido_actual.Añadir(orden2)
pedido_actual.Eliminar(0)
lista_resultado = pedido_actual.VerPedido()
