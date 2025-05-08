import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Исправленный импорт

class AIContestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Battle Arena")
        
        # Game parameters
        self.moves = ["rock", "scissors", "paper"]
        self.total_games = 5000
        self.current_game = 0
        self.update_interval = 50
        self.running = False
        
        # AI models
        self.ai_models = {
            "Random AI": RandomAI(),
            "Markov Chain": MarkovAI(),
            "Q-Learning": QLearningAI(),
            "Minimax": MinimaxAI(),
            "Frequency": FrequencyAI()
        }
        
        # Statistics
        self.stats = {
            "AI1": {"wins": 0, "history": []},
            "AI2": {"wins": 0, "history": []},
            "draws": 0
        }
        
        # UI setup
        self.setup_ui()
        self.init_plot()

    def setup_ui(self):
        # Main frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # AI selection
        ttk.Label(control_frame, text="AI 1:").pack()
        self.ai1_var = tk.StringVar()
        self.ai1_combobox = ttk.Combobox(control_frame, 
                                      textvariable=self.ai1_var,
                                      values=list(self.ai_models.keys()))
        self.ai1_combobox.current(0)
        self.ai1_combobox.pack()
        
        ttk.Label(control_frame, text="AI 2:").pack()
        self.ai2_var = tk.StringVar()
        self.ai2_combobox = ttk.Combobox(control_frame, 
                                      textvariable=self.ai2_var,
                                      values=list(self.ai_models.keys()))
        self.ai2_combobox.current(1)
        self.ai2_combobox.pack()
        
        # Controls
        ttk.Label(control_frame, text="Speed:").pack()
        self.speed_slider = ttk.Scale(control_frame, from_=1, to=100, 
                                   command=self.update_speed)
        self.speed_slider.set(50)
        self.speed_slider.pack()
        
        ttk.Button(control_frame, text="Start", 
                 command=self.start_battle).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Stop", 
                 command=self.stop_battle).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Reset", 
                 command=self.reset).pack(pady=5, fill=tk.X)
        
        # Stats
        self.stats_label = ttk.Label(control_frame, 
                                  text="Games: 0 | AI1: 0 | AI2: 0 | Draws: 0")
        self.stats_label.pack(pady=10)
        
        # Plot
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # Исправленный класс
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def init_plot(self):
        self.ax.clear()
        self.ai1_line, = self.ax.plot([], [], 'r-', label='AI1')
        self.ai2_line, = self.ax.plot([], [], 'b-', label='AI2')
        self.draw_line, = self.ax.plot([], [], 'g-', label='Draws')
        self.ax.set_title("AI Battle Results")
        self.ax.set_xlabel("Games")
        self.ax.set_ylabel("Wins")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def update_speed(self, val):
        self.update_interval = 101 - int(float(val))
        
    def start_battle(self):
        if not self.running:
            self.running = True  # Исправлена опечатка (было self.rning)
            self.battle()
        
    def stop_battle(self):
        self.running = False
        
    def battle(self):
        if self.running and self.current_game < self.total_games:
            ai1 = self.ai_models[self.ai1_var.get()]
            ai2 = self.ai_models[self.ai2_var.get()]
            
            ai1_move = ai1.choose_move(self.get_history("AI1"))
            ai2_move = ai2.choose_move(self.get_history("AI2"))
            
            result = self.determine_winner(ai1_move, ai2_move)
            
            if result == "AI1":
                self.stats["AI1"]["wins"] += 1
            elif result == "AI2":
                self.stats["AI2"]["wins"] += 1
            else:
                self.stats["draws"] += 1
                
            self.stats["AI1"]["history"].append(ai1_move)
            self.stats["AI2"]["history"].append(ai2_move)
            self.current_game += 1
            
            self.update_stats()
            self.update_plot()
            self.root.after(self.update_interval, self.battle)
    
    def update_stats(self):
        self.stats_label.config(
            text=f"Games: {self.current_game} | {self.ai1_var.get()}: {self.stats['AI1']['wins']} | "
                 f"{self.ai2_var.get()}: {self.stats['AI2']['wins']} | Draws: {self.stats['draws']}"
        )
    
    def get_history(self, ai):
        return self.stats[ai]["history"]
    
    def determine_winner(self, move1, move2):
        if move1 == move2:
            return "draw"
        elif (move1 == "rock" and move2 == "scissors") or \
             (move1 == "scissors" and move2 == "paper") or \
             (move1 == "paper" and move2 == "rock"):
            return "AI1"
        return "AI2"
    
    def update_plot(self):
        if self.current_game > 0:
            x = range(self.current_game)
            
            ai1_wins = [sum(1 for i in range(g+1) 
                          if self.determine_winner(
                              self.stats["AI1"]["history"][i],
                              self.stats["AI2"]["history"][i]) == "AI1")
                      for g in range(self.current_game)]
            
            ai2_wins = [sum(1 for i in range(g+1) 
                          if self.determine_winner(
                              self.stats["AI1"]["history"][i],
                              self.stats["AI2"]["history"][i]) == "AI2")
                      for g in range(self.current_game)]
            
            draws = [sum(1 for i in range(g+1) 
                       if self.stats["AI1"]["history"][i] == self.stats["AI2"]["history"][i])
                   for g in range(self.current_game)]
            
            self.ai1_line.set_data(x, ai1_wins)
            self.ai2_line.set_data(x, ai2_wins)
            self.draw_line.set_data(x, draws)
            
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
    
    def reset(self):
        self.stop_battle()
        self.current_game = 0
        self.stats = {
            "AI1": {"wins": 0, "history": []},
            "AI2": {"wins": 0, "history": []},
            "draws": 0
        }
        self.update_stats()
        self.init_plot()

# AI implementations
class RandomAI:
    def choose_move(self, history):
        return random.choice(["rock", "scissors", "paper"])

class MarkovAI:
    def __init__(self, n=3):
        self.n = n
        
    def choose_move(self, history):
        if len(history) < self.n or random.random() < 0.1:
            return random.choice(["rock", "scissors", "paper"])
        
        pattern = tuple(history[-self.n:])
        counts = {"rock": 0, "scissors": 0, "paper": 0}
        
        for i in range(len(history)-self.n):
            if tuple(history[i:i+self.n]) == pattern:
                next_move = history[i+self.n] if (i+self.n) < len(history) else random.choice(["rock", "scissors", "paper"])
                if next_move in counts:
                    counts[next_move] += 1
                
        if sum(counts.values()) == 0:
            return random.choice(["rock", "scissors", "paper"])
        
        return max(counts.items(), key=lambda x: x[1])[0]

class QLearningAI:
    def __init__(self, learning_rate=0.1, discount=0.9, exploration=0.1):
        self.q_table = {}
        self.lr = learning_rate
        self.discount = discount
        self.exploration = exploration
        
    def get_state_key(self, history):
        return tuple(history[-3:]) if len(history) >= 3 else tuple(history)
    
    def choose_move(self, history):
        state = self.get_state_key(history)
        
        if state not in self.q_table or random.random() < self.exploration:
            return random.choice(["rock", "scissors", "paper"])
            
        return max(self.q_table[state].items(), key=lambda x: x[1])[0]

class MinimaxAI:
    def choose_move(self, history):
        if not history:
            return random.choice(["rock", "scissors", "paper"])
        
        counts = {"rock": 0, "scissors": 0, "paper": 0}
        for move in history[-10:]:
            counts[move] += 1
            
        if sum(counts.values()) == 0:
            return random.choice(["rock", "scissors", "paper"])
            
        predicted = max(counts.items(), key=lambda x: x[1])[0]
        
        # Choose what beats the predicted move
        if predicted == "rock":
            return "paper"
        elif predicted == "scissors":
            return "rock"
        else:
            return "scissors"

class FrequencyAI:
    def choose_move(self, history):
        if not history:
            return random.choice(["rock", "scissors", "paper"])
        
        counts = {"rock": 0, "scissors": 0, "paper": 0}
        for move in history[-10:]:
            counts[move] += 1
            
        # Choose move to beat the most common move
        if counts["rock"] >= counts["scissors"] and counts["rock"] >= counts["paper"]:
            return "paper"
        elif counts["scissors"] >= counts["paper"]:
            return "rock"
        else:
            return "scissors"

if __name__ == "__main__":
    root = tk.Tk()
    app = AIContestApp(root)
    root.mainloop()