import tkinter as tk
from tkinter import messagebox
import random

# --- Lógica del juego (igual que antes, pero adaptada) ---
def crear_tablero(filas, columnas, cantidad_naufragos):
    tablero = [['.' for _ in range(columnas)] for _ in range(filas)]
    naufragos_colocados = 0
    while naufragos_colocados < cantidad_naufragos:
        f = random.randint(0, filas-1)
        c = random.randint(0, columnas-1)
        if tablero[f][c] == '.':
            tablero[f][c] = 'N'
            naufragos_colocados += 1
    return tablero

def activar_sonda(tablero, fila, columna):
    if tablero[fila][columna] == 'N':
        tablero[fila][columna] = 'R'
        return "¡Náufrago rescatado!"
    filas = len(tablero)
    columnas = len(tablero[0])
    direcciones = [(-1,0), (1,0), (0,-1), (0,1)]
    for df, dc in direcciones:
        f, c = fila + df, columna + dc
        while 0 <= f < filas and 0 <= c < columnas:
            if tablero[f][c] == 'N':
                return "¡Señal detectada! (luz parpadea)"
            f += df
            c += dc
    return "La señal se pierde (no hay náufragos en línea recta)"

# --- Interfaz gráfica ---
class NaufragosApp:
    def __init__(self, root, filas=6, columnas=6, naufragos=5, sondas=15):
        self.root = root
        self.filas = filas
        self.columnas = columnas
        self.naufragos = naufragos
        self.sondas = sondas
        self.rescatados = 0
        self.tablero = crear_tablero(filas, columnas, naufragos)
        self.botones = []
        self.info = tk.Label(root, text=f"Sondas restantes: {self.sondas}")
        self.info.pack()
        self.crear_tablero_grafico()

    def crear_tablero_grafico(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(self.filas):
            fila_botones = []
            for j in range(self.columnas):
                b = tk.Button(frame, text=".", width=3, height=1,
                              command=lambda x=i, y=j: self.intentar_rescate(x, y))
                b.grid(row=i, column=j)
                fila_botones.append(b)
            self.botones.append(fila_botones)

    def intentar_rescate(self, fila, columna):
        if self.sondas <= 0 or self.rescatados == self.naufragos:
            return
        resultado = activar_sonda(self.tablero, fila, columna)
        self.sondas -= 1
        self.info.config(text=f"Sondas restantes: {self.sondas}")
        if resultado == "¡Náufrago rescatado!":
            self.botones[fila][columna].config(text="R", bg="green")
            self.rescatados += 1
        elif resultado.startswith("¡Señal detectada"):
            self.botones[fila][columna].config(bg="yellow")
        else:
            self.botones[fila][columna].config(bg="blue")
        messagebox.showinfo("Resultado", resultado)
        if self.rescatados == self.naufragos:
            messagebox.showinfo("Fin", "¡Rescataste a todos los náufragos!")
            self.mostrar_final()
        elif self.sondas == 0:
            messagebox.showinfo("Fin", "¡Se acabaron las sondas!")
            self.mostrar_final()

    def mostrar_final(self):
        # Muestra todos los náufragos que no fueron rescatados
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == 'N':
                    self.botones[i][j].config(text="N", bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Náufragos - Juego sencillo")
    app = NaufragosApp(root, filas=6, columnas=6, naufragos=5, sondas=15)
    root.mainloop()