"""
Este modulo permitira modificar y leer el archivo de TIPOS mediante la entrega y devolucion de DICCIONARIOS
"""

PATH = "C:/Mati/2026/archivos/tipos.txt"
CARACTER = "-"

def Recopilar():
    # devuelve un diccionario con el stock de sabores

    estado_tipos = {}
    with open(PATH, "r") as tipos:
        line = tipos.readline()
        while line:
            print(line)
            line = line.strip().split(CARACTER)
            estado_tipos[line[0]] = {"cantidad de sabores": int(line[1]), "precio": int(line[2])}
            line = tipos.readline()
    
    return estado_tipos

def Añadir(diccionario_tipos):
    # al recibir un diccionario lo transformara en una nueva linea en el txt

    with open(PATH, "r") as tipos:
        archivo = tipos.readlines()
        tipos_existentes = []
        for linea in archivo:
            linea_leida = linea.strip().split("-")
            for tipo in diccionario_tipos.keys():
                tipo = tipo.capitalize()
                if linea_leida[0] == tipo:
                    tipos_existentes.append(tipo)
                    diccionario_tipos.pop(tipo)

    with open(PATH, "a") as tipos:
        for tipo, caracteristicas in diccionario_tipos.items():
            line = tipo.capitalize() + CARACTER + str(caracteristicas["cantidad de bochas"]) + CARACTER + str(caracteristicas["precio"]) + "\n"
            tipos.write(line)
    
    return True

def Eleminar(lista_sabores):
    # buscara y eliminara el sabor mediante el nombre
    lista_sabores = list(map(lambda nom: nom.capitalize(), lista_sabores))
    print(lista_sabores)
    reescritura = []
    with open(PATH, "r") as sabores:
        linea = sabores.readline()
        while linea:
            linea_leida = linea.strip().split("-")
            if linea_leida[0] not in lista_sabores:
                reescritura.append(linea)
            linea = sabores.readline()
    
    with open(PATH, "w") as sabores:
        for linea in reescritura:
            sabores.write(linea)
    
    return True

def Modificar_stock(sabor, estado):
    # cambiara el estado del sabor que se pide
    
    reescritura = []
    with open(PATH, "r") as sabores:
        existencia = False
        linea = sabores.readline()
        while linea:
            linea_leida = linea.strip().split("-")
            if linea_leida[0] == sabor.capitalize():
                linea = linea_leida[0] + CARACTER + str(estado) + "\n"
                existencia = True
            reescritura.append(linea)
            linea = sabores.readline()
    
    with open(PATH, "w") as sabores:
        for linea in reescritura:
            sabores.write(linea)
    
    if existencia:
        return(True, f"se a modificado el stock del sabor {sabor} a {estado}")
    else:
        return (False, f"el sabor {sabor} no se encuentra en los archivos. Añadalo para ver su estado")
    