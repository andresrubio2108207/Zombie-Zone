import tkinter as tk
from tkinter import messagebox
from logica import Juego
import pygame
import random


pygame.mixer.init()
sonido_correcto = pygame.mixer.Sound("Sounds/correcto.mp3")
sonido_incorrecto = pygame.mixer.Sound("Sounds/error.mp3")
sonido_game_over = pygame.mixer.Sound("Sounds/gameover.mp3")

puede_saltar = False

juego = Juego()

ventana = tk.Tk()
ventana.title("Supervivencia Zombi")
ventana.geometry("1920x1080")
ventana.configure(bg="#1a1a1a")

titulo = tk.Label(
    ventana,
    text="🧟 SUPERVIVENCIA ZOMBI 🧟",
    font=("Arial Black", 40),
    fg="#6CFF6C",
    bg="#1a1a1a"
)
titulo.pack(pady=40)

texto = tk.Label(
    ventana,
    text="Haz clic en Iniciar para comenzar",
    font=("Arial", 28),
    fg="white",
    bg="#1a1a1a"
)
texto.pack(pady=20)

vida_lbl = tk.Label(
    ventana,
    text=f"❤ Vida: {juego.vida}",
    font=("Arial Black", 26),
    fg="#FF5C5C",
    bg="#1a1a1a"
)
vida_lbl.pack(pady=10)

tiempo_lbl = tk.Label(
    ventana,
    text=f"⏳ Tiempo restante: {juego.tiempo}s",
    font=("Arial", 24),
    fg="#FFE066",
    bg="#1a1a1a"
)
tiempo_lbl.pack(pady=10)

entrada = tk.Entry(
    ventana,
    font=("Arial", 28),
    justify="center",
    bg="#2b2b2b",
    fg="white",
    width=20,
    insertbackground="white",
    relief="flat"
)
entrada.pack(pady=40)

contador_activo = False

ronda_lbl = tk.Label(
    ventana,
    text="Ronda 1",
    font=("Arial Black", 26),
    bg="#1a1a1a",
    fg="white"
)
ronda_lbl.pack(pady=5)

power_lbl = tk.Label(
    ventana,
    text="",
    font=("Arial Black", 32),
    bg="#1a1a1a",
    fg="#6CFF6C"
)
power_lbl.pack(pady=10)

def generar_powerup():
    chance = random.randint(1, 100)

    if chance <= 25:
        return "vida"      
    elif chance <= 50:
        return "tiempo"    
    elif chance <= 60:
        return "saltar"     
    else:
        return None         

def saltar_ronda():
    global puede_saltar

    if puede_saltar:
        puede_saltar = False
        power_lbl.config(text="🎁 ¡Ronda saltada!", fg="yellow")
        ventana.after(1000, iniciar)
    else:
        power_lbl.config(text="No tienes power-up de salto", fg="red")

def iniciar():
    btn_iniciar.pack_forget()

    global contador_activo
    contador_activo = False

    entrada.delete(0, tk.END)
    juego.tiempo = 3

    secuencia = juego.generar_secuencia()
    texto.config(text=f"Secuencia: {secuencia}", fg="#5CD6FF")

    ventana.after(1500, limpiar_texto)
    contar_tiempo()

def limpiar_texto():
    texto.config(text="¡Escribe la secuencia ahora!", fg="white")

def contar_tiempo():
    global contador_activo
    contador_activo = True

    if juego.tiempo > 0:
        tiempo_lbl.config(text=f"⏳ Tiempo restante: {juego.tiempo}s")
        juego.tiempo -= 1
        ventana.after(1000, contar_tiempo)
    else:
        verificar()

def parpadeo_rojo():
    ventana.config(bg="#660000")
    ventana.after(150, lambda: ventana.config(bg="#1a1a1a"))

def verificar():
    global puede_saltar
    global contador_activo

    entrada_usuario = entrada.get().lower().replace(" ", "")
    correcto = juego.verificar(entrada_usuario)

    if correcto:
        texto.config(text="¡Correcto! Sobreviviste esta ronda", fg="#6CFF6C")
        juego.ronda += 1
        ronda_lbl.config(text=f"Ronda {juego.ronda}")

        sonido_correcto.play()

        power = generar_powerup()

        if power == "vida":
            juego.vida += 1
            power_lbl.config(text="🛡 ¡Power-Up! +1 Vida", fg="#6CFF6C")
            vida_lbl.config(text=f"❤ Vida: {juego.vida}")

        elif power == "tiempo":
            juego.tiempo += 2
            power_lbl.config(text="⏳ ¡Power-Up! +2 segundos!", fg="#FFE066")

        elif power == "saltar":
            puede_saltar = True
            power_lbl.config(text="🎁 ¡Power-Up! Puedes saltar una ronda", fg="#FFB84C")

        else:
            power_lbl.config(text="")

    else:
        texto.config(text="Te equivocaste, los zombis te alcanzan", fg="#FF5C5C")
        sonido_incorrecto.play()
        parpadeo_rojo()

    vida_lbl.config(text=f"❤ Vida: {juego.vida}")
    tiempo_lbl.config(text=f"⏳ Tiempo restante: {juego.tiempo}s")
    contador_activo = False

    if juego.vida <= 0:
        sonido_game_over.play()
        texto.config(text="¡¡LOS ZOMBIS TE ATRAPARON!!", fg="red", font=("Arial", 40, "bold"))

        ventana.after(1200, lambda: (
            messagebox.showinfo("Fin del juego", "Los zombis ganaron"),
            ventana.destroy()
        ))
    else:
        ventana.after(1500, iniciar)

btn_iniciar = tk.Button(
    ventana,
    text="INICIAR",
    font=("Arial Black", 30),
    command=iniciar,
    bg="#4CAF50",
    fg="white",
    relief="flat",
    padx=40,
    pady=20,
    cursor="hand2"
)
btn_iniciar.pack(pady=50)

btn_saltar = tk.Button(
    ventana,
    text="SALTAR RONDA",
    font=("Arial Black", 26),
    bg="#9932CC",
    fg="white",
    relief="flat",
    padx=20,
    pady=10,
    command=saltar_ronda
)
btn_saltar.pack(pady=20)

ventana.mainloop()
