# Supervivencia Zombi - Game Structure

## Game Components

```
supervivencia_zombi.py (582 lines)
│
├── PowerUp (Class)
│   ├── Types: EXTRA_LIFE, EXTRA_TIME, SKIP_ROUND
│   ├── Properties: type (read-only), active (read-only)
│   └── Methods: use()
│
├── GameState (Class)
│   ├── Encapsulated attributes:
│   │   ├── _health (current health)
│   │   ├── _time (countdown timer)
│   │   ├── _round (current round number)
│   │   ├── _score (player score)
│   │   ├── _current_sequence (sequence to type)
│   │   └── _power_ups (list of available power-ups)
│   ├── Properties (read-only access):
│   │   ├── health
│   │   ├── time
│   │   ├── round
│   │   ├── score
│   │   └── current_sequence
│   └── Methods:
│       ├── decrease_health()
│       ├── increase_health()
│       ├── decrease_time()
│       ├── add_time()
│       ├── reset_time()
│       ├── next_round()
│       ├── add_power_up()
│       ├── get_power_ups()
│       ├── use_power_up()
│       ├── is_game_over()
│       └── reset()
│
├── SequenceGenerator (Class)
│   ├── Static Methods:
│   │   ├── generate_sequence() - Creates random character sequences
│   │   └── get_sequence_length() - Calculates length based on round
│   └── Character sets:
│       ├── Letters (A-Z)
│       ├── Numbers (0-9)
│       └── Symbols (rounds 5+): !@#$%&*+-=?
│
├── SoundManager (Class)
│   ├── Uses Pygame mixer
│   ├── Sound effects:
│   │   ├── "correct" - High pitch beep (800 Hz)
│   │   ├── "error" - Low pitch beep (200 Hz)
│   │   ├── "gameover" - Descending tone (400 Hz)
│   │   └── "powerup" - Ascending tone (1000 Hz)
│   └── Methods:
│       ├── play()
│       └── stop_all()
│
└── ZombieSurvivalGame (Class)
    ├── Main game controller
    ├── Tkinter GUI (600x500 window)
    ├── UI Components:
    │   ├── Title label (zombie theme)
    │   ├── Stats frame (health, time, round, score)
    │   ├── Sequence display (large Courier font)
    │   ├── Input entry field
    │   └── Buttons:
    │       ├── Verify button
    │       ├── Extra Life button
    │       ├── Extra Time button
    │       └── Skip Round button
    ├── Timer system:
    │   ├── Countdown every second
    │   └── Auto-trigger wrong answer on timeout
    └── Game flow methods:
        ├── _start_new_round()
        ├── _check_input()
        ├── _on_correct_answer()
        ├── _on_wrong_answer()
        ├── _use_*_powerup() (3 methods)
        ├── _game_over()
        └── _restart_game()
```

## Game Flow Diagram

```
START
  │
  ├─→ Initialize GameState (3 lives, 30s)
  │
  ├─→ Generate random sequence
  │
  ├─→ Start countdown timer
  │
  ├─→ Player types sequence
  │
  ├─→ Check input or timeout
      │
      ├─→ CORRECT?
      │   ├─→ Play "correct" sound
      │   ├─→ Add score
      │   ├─→ Next round
      │   ├─→ Maybe grant power-up (20%)
      │   └─→ Loop to generate sequence
      │
      └─→ WRONG/TIMEOUT?
          ├─→ Play "error" sound
          ├─→ Decrease health (-1)
          │
          └─→ Health = 0?
              ├─→ YES: Game Over
              │   ├─→ Play "gameover" sound
              │   └─→ Restart option
              │
              └─→ NO: Continue
                  └─→ Loop to generate sequence
```

## Difficulty Progression

| Round | Sequence Length | Character Types | Example |
|-------|----------------|-----------------|---------|
| 1 | 3 | Letters + Numbers | `A3K` |
| 2 | 4 | Letters + Numbers | `7BQ2` |
| 3 | 5 | Letters + Numbers | `M9D8F` |
| 4 | 6 | Letters + Numbers | `K1N7P4` |
| 5+ | 7+ | Letters + Numbers + Symbols | `Q@3K#8M` |

## Power-Up System

- **Spawn Rate**: 20% chance per round
- **Types**:
  1. ❤️ Extra Life - Adds 1 health (max: initial + 2)
  2. ⏰ Extra Time - Adds 10 seconds to current round
  3. ⏭️ Skip Round - Complete current round without typing

## Scoring System

- Base score per round: `100 × round_number`
- Example:
  - Round 1: +100 points
  - Round 2: +200 points  
  - Round 3: +300 points
  - etc.

## Requirements

See `requirements.txt`:
- pygame >= 2.0.0
- numpy >= 1.20.0
- tkinter (included with Python)
