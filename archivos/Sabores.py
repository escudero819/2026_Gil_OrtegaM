"""
Este modulo permitira modificar y leer el archivo de SABORES mediante la entrega y devolucion de DICCIONARIOS
"""
PATH = "C:/Mati/2026/archivos/sabores.txt"
CARACTER = "-"

def Recopilar_sabores():
    # devuelve un diccionario con el stock de sabores

    estado_sabores = {}
    with open(PATH, "r") as sabores:
        line = sabores.readline()
        print(line)
        while line:
            line = line.strip().split(CARACTER)
            estado_sabores[line[0]] = bool(line[1])
            line = sabores.readline()
    
    return estado_sabores

def Añadir_sabores(diccionario_sabores):
    # al recibir un diccionario lo transformara en una nueva linea en el txt

    with open(PATH, "r") as sabores:
        archivo = sabores.readlines()
        sabores_existentes = []
        for linea in archivo:
            linea_leida = linea.strip().split("-")
            for sabor in diccionario_sabores.keys():
                sabor = sabor.capitalize()
                if linea_leida[0] == sabor:
                    sabores_existentes.append(sabor)
                    diccionario_sabores.pop(sabor)

    with open(PATH, "a"):
        for sabor, estado in diccionario_sabores.items():
            line = sabor.capitalize() + CARACTER + str(estado) + "\n"
            sabores.write(line)
    
    return True

def Eleminar_sabores(lista_sabores):
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
    
