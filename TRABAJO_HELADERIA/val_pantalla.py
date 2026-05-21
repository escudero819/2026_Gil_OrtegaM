def val_pantalla():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    return ancho, alto


#en caso de uqerer ver los valores de pantalla 
"""ancho, alto = val_pantalla()
print(ancho, alto)"""