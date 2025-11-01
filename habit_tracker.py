#!/usr/bin/env python3
"""CLI Habit Tracker

Usage examples:
  python habit_tracker.py add "Read 10 pages"
  python habit_tracker.py done "Read 10 pages"
  python habit_tracker.py list
  python habit_tracker.py stats

This script stores data in a JSON file (`habits.json` by default) and
implements a simple streak rule: if you mark a habit done on a day after
the previous done date was yesterday, the streak increases; otherwise it
resets to 1 when marking a habit done again.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

DATA_FILE = Path("habits.json")


def load_data(path: Path = DATA_FILE) -> Dict[str, List[Dict]]:
    if not path.exists():
        return {"habits": []}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict, path: Path = DATA_FILE) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def find_habit(data: Dict, name: str) -> Optional[Dict]:
    for h in data.get("habits", []):
        if h.get("name", "").lower() == name.lower():
            return h
    return None


def add_habit(name: str) -> None:
    data = load_data()
    if find_habit(data, name):
        print(f"Habit '{name}' already exists.")
        return
    data.setdefault("habits", []).append({"name": name, "streak": 0, "last_done": None})
    save_data(data)
    print(f"Added habit: {name}")


def mark_done(name: str, on_date: Optional[date] = None) -> None:
    data = load_data()
    h = find_habit(data, name)
    if not h:
        print(f"Habit '{name}' not found. Use 'add' to create it.")
        return

    today = (on_date or date.today()).isoformat()
    last = h.get("last_done")
    if last == today:
        print(f"Already marked '{name}' as done today.")
        return

    # Determine streak continuity: if last was yesterday -> increment, else reset to 1
    if last:
        try:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
        except ValueError:
            last_date = None
    else:
        last_date = None

    if last_date == (date.fromisoformat(today) - timedelta(days=1)):
        h["streak"] = int(h.get("streak", 0)) + 1
    else:
        h["streak"] = 1

    h["last_done"] = today
    save_data(data)
    print(f"Marked '{name}' as done. Streak: {h['streak']}")


def list_habits() -> None:
    data = load_data()
    if not data.get("habits"):
        print("No habits found. Use 'add' to create one.")
        return
    print("\nYour Habits:")
    today = date.today().isoformat()
    for h in data["habits"]:
        done_today = "Done" if h.get("last_done") == today else "Not done"
        print(f"- {h.get('name')} | Streak: {h.get('streak', 0)} | Today: {done_today}")
    print()


def show_stats() -> None:
    data = load_data()
    habits = data.get("habits", [])
    total = len(habits)
    if total == 0:
        print("No habits tracked yet.")
        return
    today = date.today().isoformat()
    done_today = sum(1 for h in habits if h.get("last_done") == today)
    longest = max(habits, key=lambda x: x.get("streak", 0), default=None)
    print(f"{done_today}/{total} habits done today.")
    if longest:
        print(f"Longest streak: {longest.get('name')} ({longest.get('streak', 0)} days)")


def remove_habit(name: str) -> None:
    data = load_data()
    before = len(data.get("habits", []))
    data["habits"] = [h for h in data.get("habits", []) if h.get("name", "").lower() != name.lower()]
    after = len(data.get("habits", []))
    if before == after:
        print(f"Habit '{name}' not found.")
    else:
        save_data(data)
        print(f"Removed habit: {name}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Simple CLI Habit Tracker")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Add a new habit")
    a.add_argument("name", nargs='+', help="Name of the habit")

    d = sub.add_parser("done", help="Mark a habit done for today")
    d.add_argument("name", nargs='+', help="Name of the habit")

    sub.add_parser("list", help="List tracked habits")
    sub.add_parser("stats", help="Show progress stats")

    r = sub.add_parser("remove", help="Remove a habit")
    r.add_argument("name", nargs='+', help="Name of the habit to remove")

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        add_habit(" ".join(args.name))
    elif args.command == "done":
        mark_done(" ".join(args.name))
    elif args.command == "list":
        list_habits()
    elif args.command == "stats":
        show_stats()
    elif args.command == "remove":
        remove_habit(" ".join(args.name))


if __name__ == "__main__":
    main()
