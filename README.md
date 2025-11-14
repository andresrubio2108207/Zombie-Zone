# Zombie-Zone 🧟

Supervivencia Zombi es un juego en Python donde debes memorizar y escribir secuencias para sobrevivir a oleadas de zombis. Consigue power-ups de vida, tiempo o para saltar rondas. Con Tkinter y Pygame, combina rapidez, memoria y estrategia en una experiencia divertida y desafiante.

## 📋 Requisitos

- Python 3.7 o superior
- Pygame
- NumPy
- Tkinter (generalmente incluido con Python)

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/andresrubio2108207/Zombie-Zone.git
cd Zombie-Zone
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Cómo Jugar

1. Ejecuta el juego:
```bash
python3 supervivencia_zombi.py
```

2. **Objetivo**: Escribe correctamente las secuencias mostradas antes de que se acabe el tiempo.

3. **Mecánicas**:
   - **Vida**: Empiezas con 3 vidas (❤️)
   - **Tiempo**: Tienes 30 segundos por ronda (⏰)
   - **Rondas**: Cada ronda aumenta la dificultad (🌙)
   - **Puntuación**: Gana puntos completando rondas (⭐)

4. **Secuencias**:
   - Rondas 1-4: Letras y números
   - Ronda 5+: Letras, números y símbolos (!@#$%&*+-=?)
   - La longitud aumenta con cada ronda

5. **Power-ups** (20% de probabilidad cada ronda):
   - **❤️ Vida Extra**: Añade una vida
   - **⏰ Tiempo Extra**: Añade 10 segundos
   - **⏭️ Saltar Ronda**: Avanza a la siguiente ronda sin perder vida

6. **Game Over**: El juego termina cuando tu vida llega a 0.

## 🏗️ Arquitectura del Código

El juego está implementado con programación orientada a objetos y encapsulamiento:

- **`GameState`**: Maneja el estado del juego (vida, tiempo, ronda, puntuación)
- **`PowerUp`**: Representa los power-ups del juego
- **`SequenceGenerator`**: Genera secuencias aleatorias
- **`SoundManager`**: Administra los efectos de sonido
- **`ZombieSurvivalGame`**: Clase principal que controla la GUI y lógica del juego

## 🎵 Efectos de Sonido

El juego incluye sonidos para:
- ✅ Respuesta correcta (tono alto)
- ❌ Respuesta incorrecta (tono bajo)
- 💀 Game Over (tono descendente)
- ⭐ Power-up obtenido (tono ascendente)

## 🎨 Características

- ✅ Interfaz gráfica con Tkinter
- ✅ Sistema de puntuación
- ✅ Dificultad progresiva
- ✅ Power-ups aleatorios
- ✅ Efectos de sonido
- ✅ Sistema de vidas
- ✅ Temporizador de cuenta regresiva
- ✅ Reinicio de juego

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Andrés Rubio
