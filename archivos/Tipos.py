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
            line = tipo.capitalize() + CARACTER + str(caracteristicas["cantidad de sabores"]) + CARACTER + str(caracteristicas["precio"]) + "\n"
            tipos.write(line)
    
    return True

def Eleminar(lista_tipos):
    # buscara y eliminara el sabor mediante el nombre
    lista_tipos = list(map(lambda nom: nom.capitalize(), lista_tipos))
    print(lista_tipos)
    reescritura = []
    with open(PATH, "r") as tipos:
        linea = tipos.readline()
        while linea:
            linea_leida = linea.strip().split("-")
            if linea_leida[0] not in lista_tipos:
                reescritura.append(linea)
            linea = tipos.readline()
    
    with open(PATH, "w") as tipos:
        for linea in reescritura:
            tipos.write(linea)
    
    return True
