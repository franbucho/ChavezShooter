import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class JuegoTiroAlBlanco:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Tiro al Blanco")

        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        # Obtener la ruta del script
        ruta_script = os.path.dirname(os.path.abspath(__file__))

        # Cargar la imagen desde la misma ubicación del script
        imagen_chavez = Image.open(os.path.join(ruta_script, "chavez.png"))
        imagen_chavez = imagen_chavez.resize((20, 20), Image.BICUBIC)  # Ajustar el tamaño si es necesario
        self.chavez_img = ImageTk.PhotoImage(imagen_chavez)

        # Crear el blanco con la imagen
        self.blanco = self.canvas.create_image(240, 190, image=self.chavez_img, anchor=tk.NW)

        self.puntuacion = 0
        self.intentos_restantes = 10
        self.tiempo_restante = 30

        self.instrucciones = tk.Label(root, text="¡Haz clic en el blanco!", font=("Helvetica", 12))
        self.instrucciones.pack()

        self.lbl_puntuacion = tk.Label(root, text="Puntuación: 0", font=("Helvetica", 10))
        self.lbl_puntuacion.pack()

        self.lbl_intentos = tk.Label(root, text="Intentos restantes: 10", font=("Helvetica", 10))
        self.lbl_intentos.pack()

        self.lbl_tiempo = tk.Label(root, text="Tiempo restante: 30", font=("Helvetica", 10))
        self.lbl_tiempo.pack()

        self.actualizar_puntuacion()
        self.actualizar_intentos()

        self.canvas.bind("<Button-1>", self.hacer_clic)

        self.actualizar_temporizador()
        self.mover_blanco_aleatoriamente()

    def hacer_clic(self, event):
        if self.ha_colisionado(event.x, event.y):
            self.puntuacion += 1
            self.actualizar_puntuacion()
            self.mover_blanco_aleatoriamente()

        self.intentos_restantes -= 1
        self.actualizar_intentos()

        if self.intentos_restantes == 0 or self.tiempo_restante == 0:
            self.mostrar_resultados()

    def ha_colisionado(self, x, y):
        blanco_coords = self.canvas.coords(self.blanco)
        return blanco_coords[0] <= x <= blanco_coords[0] + 20 and blanco_coords[1] <= y <= blanco_coords[1] + 20

    def mover_blanco_aleatoriamente(self):
        nueva_x = random.randint(50, 450)
        nueva_y = random.randint(50, 350)
        self.canvas.coords(self.blanco, nueva_x, nueva_y)

    def actualizar_puntuacion(self):
        self.lbl_puntuacion.config(text=f"Puntuación: {self.puntuacion}")

    def actualizar_intentos(self):
        self.lbl_intentos.config(text=f"Intentos restantes: {self.intentos_restantes}")

    def actualizar_temporizador(self):
        if self.tiempo_restante > 0 and self.intentos_restantes > 0:
            self.tiempo_restante -= 1
            self.lbl_tiempo.config(text=f"Tiempo restante: {self.tiempo_restante}")
            self.root.after(1000, self.actualizar_temporizador)
        else:
            self.mostrar_resultados()

    def mostrar_resultados(self):
        self.canvas.unbind("<Button-1>")
        mensaje_final = f"¡Juego terminado!\nPuntuación final: {self.puntuacion}"
        messagebox.showinfo("Fin del juego", mensaje_final)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoTiroAlBlanco(root)
    root.mainloop()
