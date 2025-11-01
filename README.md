# CLI-Habit-Tracker

Simple command-line habit tracker written in Python.

Features
- Add habits, mark them done for today, list habits, view basic stats, and remove habits.
- Tracks a simple streak: marking a habit done on the day after the previous done date increments the streak; otherwise the streak resets to 1.

Usage
```
python habit_tracker.py add "Read 10 pages"
python habit_tracker.py done "Read 10 pages"
python habit_tracker.py list
python habit_tracker.py stats
python habit_tracker.py remove "Read 10 pages"
```

Data
- Stored in `habits.json` in the working directory.

Notes
- This project is small and intentionally dependency-free.