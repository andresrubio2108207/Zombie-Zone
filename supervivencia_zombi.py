#!/usr/bin/env python3
"""
Supervivencia Zombi - Zombie Survival Game
A typing game where you must type sequences to survive zombie waves
"""

import tkinter as tk
from tkinter import messagebox
import random
import string
import pygame
from typing import List, Optional


class PowerUp:
    """Class to represent power-ups in the game"""
    
    EXTRA_LIFE = "vida_extra"
    EXTRA_TIME = "tiempo_extra"
    SKIP_ROUND = "saltar_ronda"
    
    def __init__(self, power_type: str):
        """Initialize a power-up with a specific type"""
        self._type = power_type
        self._active = True
    
    @property
    def type(self) -> str:
        """Get the power-up type"""
        return self._type
    
    @property
    def active(self) -> bool:
        """Check if power-up is active"""
        return self._active
    
    def use(self):
        """Use the power-up"""
        self._active = False


class GameState:
    """Class to manage game state with encapsulation"""
    
    def __init__(self, initial_health: int = 3, initial_time: int = 30):
        """Initialize game state"""
        self._health = initial_health
        self._max_health = initial_health
        self._time = initial_time
        self._initial_time = initial_time
        self._round = 1
        self._score = 0
        self._current_sequence = ""
        self._power_ups: List[PowerUp] = []
    
    @property
    def health(self) -> int:
        """Get current health"""
        return self._health
    
    @property
    def time(self) -> int:
        """Get current time"""
        return self._time
    
    @property
    def round(self) -> int:
        """Get current round number"""
        return self._round
    
    @property
    def score(self) -> int:
        """Get current score"""
        return self._score
    
    @property
    def current_sequence(self) -> str:
        """Get current sequence to type"""
        return self._current_sequence
    
    def set_sequence(self, sequence: str):
        """Set the current sequence"""
        self._current_sequence = sequence
    
    def decrease_health(self):
        """Decrease health by 1"""
        self._health = max(0, self._health - 1)
    
    def increase_health(self):
        """Increase health by 1 (with power-up)"""
        self._health = min(self._max_health + 2, self._health + 1)
    
    def decrease_time(self):
        """Decrease time by 1 second"""
        self._time = max(0, self._time - 1)
    
    def add_time(self, seconds: int = 10):
        """Add extra time (with power-up)"""
        self._time += seconds
    
    def reset_time(self):
        """Reset time for new round"""
        self._time = self._initial_time
    
    def next_round(self):
        """Advance to next round"""
        self._round += 1
        self._score += 100 * self._round
    
    def add_power_up(self, power_up: PowerUp):
        """Add a power-up to inventory"""
        self._power_ups.append(power_up)
    
    def get_power_ups(self) -> List[PowerUp]:
        """Get list of active power-ups"""
        return [pu for pu in self._power_ups if pu.active]
    
    def use_power_up(self, power_type: str) -> bool:
        """Use a power-up if available"""
        for pu in self._power_ups:
            if pu.type == power_type and pu.active:
                pu.use()
                return True
        return False
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self._health <= 0
    
    def reset(self):
        """Reset game state"""
        self._health = self._max_health
        self._time = self._initial_time
        self._round = 1
        self._score = 0
        self._current_sequence = ""
        self._power_ups = []


class SequenceGenerator:
    """Class to generate random sequences for the game"""
    
    @staticmethod
    def generate_sequence(length: int, include_symbols: bool = False) -> str:
        """Generate a random sequence of characters"""
        chars = string.ascii_uppercase + string.digits
        if include_symbols:
            chars += "!@#$%&*+-=?"
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def get_sequence_length(round_num: int) -> int:
        """Calculate sequence length based on round number"""
        base_length = 3
        return base_length + (round_num - 1)


class SoundManager:
    """Class to manage game sounds using Pygame"""
    
    def __init__(self):
        """Initialize sound manager"""
        pygame.mixer.init()
        self._sounds = {}
        self._setup_sounds()
    
    def _setup_sounds(self):
        """Setup sound effects (using beeps as placeholders)"""
        # Create simple beep sounds at different frequencies
        try:
            # Correct answer sound (high pitch)
            self._create_beep(800, 0.1, "correct")
            # Error sound (low pitch)
            self._create_beep(200, 0.2, "error")
            # Game over sound (descending)
            self._create_beep(400, 0.5, "gameover")
            # Power-up sound (ascending)
            self._create_beep(1000, 0.15, "powerup")
        except Exception as e:
            print(f"Warning: Could not initialize sounds: {e}")
    
    def _create_beep(self, frequency: int, duration: float, name: str):
        """Create a beep sound at given frequency"""
        try:
            sample_rate = 22050
            n_samples = int(round(duration * sample_rate))
            
            # Generate sine wave
            import numpy as np
            buf = np.zeros((n_samples, 2), dtype=np.int16)
            max_sample = 2047
            
            for s in range(n_samples):
                t = float(s) / sample_rate
                value = int(round(max_sample * np.sin(2 * np.pi * frequency * t)))
                buf[s][0] = value
                buf[s][1] = value
            
            sound = pygame.sndarray.make_sound(buf)
            self._sounds[name] = sound
        except ImportError:
            # NumPy not available, skip sound generation
            pass
        except Exception as e:
            print(f"Warning: Could not create {name} sound: {e}")
    
    def play(self, sound_name: str):
        """Play a sound effect"""
        try:
            if sound_name in self._sounds:
                self._sounds[sound_name].play()
        except Exception as e:
            print(f"Warning: Could not play sound {sound_name}: {e}")
    
    def stop_all(self):
        """Stop all playing sounds"""
        try:
            pygame.mixer.stop()
        except Exception:
            pass


class ZombieSurvivalGame:
    """Main game class for Zombie Survival"""
    
    def __init__(self, root: tk.Tk):
        """Initialize the game"""
        self.root = root
        self.root.title("Supervivencia Zombi")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Initialize game components
        self.game_state = GameState()
        self.sequence_gen = SequenceGenerator()
        self.sound_manager = SoundManager()
        
        # Timer tracking
        self.timer_running = False
        self.timer_id: Optional[str] = None
        
        # Setup UI
        self._setup_ui()
        
        # Start first round
        self._start_new_round()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🧟 SUPERVIVENCIA ZOMBI 🧟",
            font=("Arial", 24, "bold"),
            fg="#8B0000",
            bg="#2F2F2F",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#1A1A1A", pady=10)
        stats_frame.pack(fill=tk.X, padx=20)
        
        self.health_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 14),
            fg="#FF0000",
            bg="#1A1A1A"
        )
        self.health_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 14),
            fg="#00FF00",
            bg="#1A1A1A"
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.round_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 14),
            fg="#FFD700",
            bg="#1A1A1A"
        )
        self.round_label.pack(side=tk.LEFT, padx=10)
        
        self.score_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 14),
            fg="#00BFFF",
            bg="#1A1A1A"
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Sequence display
        sequence_frame = tk.Frame(self.root, bg="#000000", pady=30)
        sequence_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            sequence_frame,
            text="Escribe esta secuencia:",
            font=("Arial", 12),
            fg="#FFFFFF",
            bg="#000000"
        ).pack(pady=5)
        
        self.sequence_label = tk.Label(
            sequence_frame,
            text="",
            font=("Courier", 32, "bold"),
            fg="#00FF00",
            bg="#000000"
        )
        self.sequence_label.pack(pady=10)
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            sequence_frame,
            textvariable=self.input_var,
            font=("Courier", 24),
            justify="center",
            width=20
        )
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self._check_input)
        self.input_entry.focus()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2F2F2F")
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.check_button = tk.Button(
            buttons_frame,
            text="Verificar",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self._check_input,
            width=12
        )
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        # Power-up buttons
        self.life_button = tk.Button(
            buttons_frame,
            text="❤️ Vida Extra",
            font=("Arial", 10),
            bg="#FF4444",
            fg="white",
            command=self._use_life_powerup,
            width=12
        )
        self.life_button.pack(side=tk.LEFT, padx=5)
        
        self.time_button = tk.Button(
            buttons_frame,
            text="⏰ Tiempo Extra",
            font=("Arial", 10),
            bg="#4444FF",
            fg="white",
            command=self._use_time_powerup,
            width=12
        )
        self.time_button.pack(side=tk.LEFT, padx=5)
        
        self.skip_button = tk.Button(
            buttons_frame,
            text="⏭️ Saltar Ronda",
            font=("Arial", 10),
            bg="#FF8800",
            fg="white",
            command=self._use_skip_powerup,
            width=12
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)
        
        # Set background color
        self.root.configure(bg="#2F2F2F")
        
        self._update_display()
    
    def _update_display(self):
        """Update all display elements"""
        self.health_label.config(text=f"❤️ Vida: {self.game_state.health}")
        self.time_label.config(text=f"⏰ Tiempo: {self.game_state.time}s")
        self.round_label.config(text=f"🌙 Ronda: {self.game_state.round}")
        self.score_label.config(text=f"⭐ Puntos: {self.game_state.score}")
        self.sequence_label.config(text=self.game_state.current_sequence)
        
        # Update power-up button states
        power_ups = self.game_state.get_power_ups()
        has_life = any(pu.type == PowerUp.EXTRA_LIFE for pu in power_ups)
        has_time = any(pu.type == PowerUp.EXTRA_TIME for pu in power_ups)
        has_skip = any(pu.type == PowerUp.SKIP_ROUND for pu in power_ups)
        
        self.life_button.config(state=tk.NORMAL if has_life else tk.DISABLED)
        self.time_button.config(state=tk.NORMAL if has_time else tk.DISABLED)
        self.skip_button.config(state=tk.NORMAL if has_skip else tk.DISABLED)
    
    def _start_new_round(self):
        """Start a new round"""
        # Generate new sequence
        length = self.sequence_gen.get_sequence_length(self.game_state.round)
        include_symbols = self.game_state.round >= 5
        sequence = self.sequence_gen.generate_sequence(length, include_symbols)
        self.game_state.set_sequence(sequence)
        
        # Reset time
        self.game_state.reset_time()
        
        # Random chance to grant power-up (20% chance)
        if random.random() < 0.2:
            power_type = random.choice([
                PowerUp.EXTRA_LIFE,
                PowerUp.EXTRA_TIME,
                PowerUp.SKIP_ROUND
            ])
            self.game_state.add_power_up(PowerUp(power_type))
            self.sound_manager.play("powerup")
        
        # Clear input
        self.input_var.set("")
        self.input_entry.focus()
        
        # Update display
        self._update_display()
        
        # Start timer
        self._start_timer()
    
    def _start_timer(self):
        """Start the countdown timer"""
        self.timer_running = True
        self._update_timer()
    
    def _stop_timer(self):
        """Stop the countdown timer"""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def _update_timer(self):
        """Update the countdown timer"""
        if not self.timer_running:
            return
        
        if self.game_state.time > 0:
            self.game_state.decrease_time()
            self._update_display()
            self.timer_id = self.root.after(1000, self._update_timer)
        else:
            # Time ran out
            self._on_wrong_answer()
    
    def _check_input(self, event=None):
        """Check if the input matches the sequence"""
        user_input = self.input_var.get().strip().upper()
        
        if not user_input:
            return
        
        if user_input == self.game_state.current_sequence:
            self._on_correct_answer()
        else:
            self._on_wrong_answer()
    
    def _on_correct_answer(self):
        """Handle correct answer"""
        self._stop_timer()
        self.sound_manager.play("correct")
        
        # Show success message
        self.sequence_label.config(fg="#00FF00")
        self.input_entry.config(state=tk.DISABLED)
        
        # Advance round
        self.game_state.next_round()
        self._update_display()
        
        # Continue to next round after delay
        self.root.after(1000, self._continue_after_correct)
    
    def _continue_after_correct(self):
        """Continue game after correct answer"""
        self.sequence_label.config(fg="#00FF00")
        self.input_entry.config(state=tk.NORMAL)
        self._start_new_round()
    
    def _on_wrong_answer(self):
        """Handle wrong answer or timeout"""
        self._stop_timer()
        self.sound_manager.play("error")
        
        # Decrease health
        self.game_state.decrease_health()
        
        # Show error
        self.sequence_label.config(fg="#FF0000")
        self.input_entry.config(state=tk.DISABLED)
        
        self._update_display()
        
        if self.game_state.is_game_over():
            self._game_over()
        else:
            # Continue after delay
            self.root.after(1500, self._continue_after_wrong)
    
    def _continue_after_wrong(self):
        """Continue game after wrong answer"""
        self.sequence_label.config(fg="#00FF00")
        self.input_entry.config(state=tk.NORMAL)
        self._start_new_round()
    
    def _use_life_powerup(self):
        """Use extra life power-up"""
        if self.game_state.use_power_up(PowerUp.EXTRA_LIFE):
            self.game_state.increase_health()
            self.sound_manager.play("powerup")
            self._update_display()
    
    def _use_time_powerup(self):
        """Use extra time power-up"""
        if self.game_state.use_power_up(PowerUp.EXTRA_TIME):
            self.game_state.add_time(10)
            self.sound_manager.play("powerup")
            self._update_display()
    
    def _use_skip_powerup(self):
        """Use skip round power-up"""
        if self.game_state.use_power_up(PowerUp.SKIP_ROUND):
            self._stop_timer()
            self.sound_manager.play("powerup")
            self.game_state.next_round()
            self._update_display()
            self.root.after(500, self._start_new_round)
    
    def _game_over(self):
        """Handle game over"""
        self._stop_timer()
        self.sound_manager.play("gameover")
        
        message = f"¡GAME OVER!\n\n"
        message += f"Rondas completadas: {self.game_state.round - 1}\n"
        message += f"Puntuación final: {self.game_state.score}\n\n"
        message += "¿Quieres jugar de nuevo?"
        
        response = messagebox.askyesno("Fin del Juego", message)
        
        if response:
            self._restart_game()
        else:
            self.root.quit()
    
    def _restart_game(self):
        """Restart the game"""
        self.game_state.reset()
        self.sequence_label.config(fg="#00FF00")
        self.input_entry.config(state=tk.NORMAL)
        self.input_var.set("")
        self._update_display()
        self._start_new_round()


def main():
    """Main function to run the game"""
    root = tk.Tk()
    game = ZombieSurvivalGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
