## 🌍 English

### 🚀 Overview
AI Battle Arena is a visual simulation platform where different AI algorithms compete in Rock-Paper-Scissors battles. The project demonstrates various artificial intelligence approaches in a game theory environment.

### ✨ Features
- **5 AI implementations**:
  - Random AI (baseline)
  - Markov Chain (pattern recognition)
  - Q-Learning (reinforcement learning)
  - Minimax (game theory)
  - Frequency Analysis (statistical approach)
- **Real-time visualization** of battle outcomes
- **Customizable parameters**: game speed, AI matchups
- **Comprehensive statistics** tracking

  🎮 Usage
Run the application:

Bash

python ai_battle_arena.py
Interface controls:

Select AI models from dropdown menus
Adjust battle speed with the slider
Start/Stop/Reset battles with control buttons

❓ FAQ
Q: Can I add new AI algorithms?
A: Yes! Simply create a new class that implements the choose_move() method.

Q: Why does Q-Learning sometimes perform poorly?
A: This implementation uses simple state representation. More complex state encoding would improve results.
  📊 Results Interpretation
The application displays:

Cumulative win counts for each AI
Win rate percentages
Real-time graph of battle outcomes
🤝 Contributing
Contributions are welcome! Please follow these guidelines:

Fork the repository
Create a feature branch
Submit a pull request
