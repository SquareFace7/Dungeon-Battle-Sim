#!/usr/bin/env python3
"""
Dungeon Battle Game Simulator
A non-interactive battle simulation for DevOps CI/CD pipelines.
Generates detailed logs and HTML reports for battle outcomes.
"""

import argparse
import random
import sys
from datetime import datetime
from typing import Dict, List, Tuple


class Hero:
    """Represents the player's hero character."""

    VALID_CLASSES = ['Warrior', 'Mage', 'Rogue']

    def __init__(self, name: str, hero_class: str, level: int, hardcore_mode: bool):
        self.name = name
        self.hero_class = hero_class
        self.level = level
        self.hardcore_mode = hardcore_mode

        self.max_hp = self._calculate_max_hp()
        self.current_hp = self.max_hp
        self.attack = self._calculate_attack()
        self.defense = self._calculate_defense()
        self.critical_chance = self._calculate_critical_chance()

    def _calculate_max_hp(self) -> int:
        """Calculate maximum HP based on class and level."""
        base_hp = {
            'Warrior': 150,
            'Mage': 100,
            'Rogue': 120
        }
        return base_hp[self.hero_class] + (self.level * 10)

    def _calculate_attack(self) -> int:
        """Calculate attack power based on class and level."""
        base_attack = {
            'Warrior': 25,
            'Mage': 35,
            'Rogue': 30
        }
        return base_attack[self.hero_class] + (self.level * 2)

    def _calculate_defense(self) -> int:
        """Calculate defense based on class and level."""
        base_defense = {
            'Warrior': 20,
            'Mage': 10,
            'Rogue': 15
        }
        return base_defense[self.hero_class] + (self.level * 1)

    def _calculate_critical_chance(self) -> float:
        """Calculate critical hit chance."""
        base_crit = {
            'Warrior': 0.15,
            'Mage': 0.25,
            'Rogue': 0.35
        }
        return min(base_crit[self.hero_class] + (self.level * 0.002), 0.75)

    def attack_enemy(self) -> Tuple[int, bool]:
        """Perform an attack. Returns (damage, is_critical)."""
        is_critical = random.random() < self.critical_chance
        damage = self.attack + random.randint(-5, 10)

        if is_critical:
            damage = int(damage * 2.0)

        return damage, is_critical

    def take_damage(self, damage: int) -> int:
        """Take damage after defense calculation."""
        actual_damage = max(damage - (self.defense // 2), 1)
        self.current_hp -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        """Check if hero is still alive."""
        return self.current_hp > 0


class Enemy:
    """Represents the dungeon enemy."""

    def __init__(self, hero_level: int, hardcore_mode: bool):
        self.level = hero_level + random.randint(-2, 3)
        self.hardcore_mode = hardcore_mode

        difficulty_multiplier = 1.5 if hardcore_mode else 1.0

        self.name = self._generate_name()
        self.max_hp = int((100 + self.level * 12) * difficulty_multiplier)
        self.current_hp = self.max_hp
        self.attack = int((20 + self.level * 2) * difficulty_multiplier)
        self.defense = 10 + self.level

    def _generate_name(self) -> str:
        """Generate a random enemy name."""
        prefixes = ['Dark', 'Ancient', 'Cursed', 'Vile', 'Shadow', 'Blood']
        creatures = ['Dragon', 'Demon', 'Golem', 'Wraith', 'Beast', 'Lich']
        return f"{random.choice(prefixes)} {random.choice(creatures)}"

    def attack_hero(self) -> int:
        """Perform an attack."""
        if random.random() < 0.15:
            return 0
        return self.attack + random.randint(-3, 8)

    def take_damage(self, damage: int) -> int:
        """Take damage after defense calculation."""
        actual_damage = max(damage - (self.defense // 2), 1)
        self.current_hp -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        """Check if enemy is still alive."""
        return self.current_hp > 0


class BattleSimulator:
    """Manages the battle simulation between hero and enemy."""

    def __init__(self, hero: Hero, enemy: Enemy):
        self.hero = hero
        self.enemy = enemy
        self.battle_log: List[str] = []
        self.turn_count = 0
        self.max_turns = 50

    def log_event(self, message: str):
        """Add a timestamped event to the battle log."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] Turn {self.turn_count}: {message}"
        self.battle_log.append(log_entry)
        print(log_entry)

    def simulate_battle(self) -> bool:
        """
        Simulate the battle between hero and enemy.
        Returns True if hero wins, False otherwise.
        """
        self.log_event(f"=== BATTLE START ===")
        self.log_event(f"{self.hero.name} the {self.hero.hero_class} (Lv.{self.hero.level}) vs {self.enemy.name} (Lv.{self.enemy.level})")
        self.log_event(f"Hero HP: {self.hero.max_hp} | Attack: {self.hero.attack} | Defense: {self.hero.defense}")
        self.log_event(f"Enemy HP: {self.enemy.max_hp} | Attack: {self.enemy.attack} | Defense: {self.enemy.defense}")

        if self.hero.hardcore_mode:
            self.log_event("⚠️  HARDCORE MODE ACTIVE - Enemy is stronger!")

        self.log_event("")

        while self.hero.is_alive() and self.enemy.is_alive() and self.turn_count < self.max_turns:
            self.turn_count += 1

            hero_damage, is_crit = self.hero.attack_enemy()
            actual_damage = self.enemy.take_damage(hero_damage)

            crit_indicator = " 💥 CRITICAL HIT!" if is_crit else ""
            self.log_event(f"{self.hero.name} attacks for {hero_damage} damage (dealt {actual_damage} after defense){crit_indicator}")
            self.log_event(f"Enemy HP: {max(0, self.enemy.current_hp)}/{self.enemy.max_hp}")

            if not self.enemy.is_alive():
                self.log_event(f"💀 {self.enemy.name} has been defeated!")
                break

            enemy_damage = self.enemy.attack_hero()
            if enemy_damage == 0:
                self.log_event(f"{self.enemy.name} attacks but MISSES!")
            else:
                actual_damage = self.hero.take_damage(enemy_damage)
                self.log_event(f"{self.enemy.name} attacks for {enemy_damage} damage (dealt {actual_damage} after defense)")

            self.log_event(f"Hero HP: {max(0, self.hero.current_hp)}/{self.hero.max_hp}")
            self.log_event("")

            if not self.hero.is_alive():
                self.log_event(f"💀 {self.hero.name} has been defeated...")
                break

        if self.turn_count >= self.max_turns:
            self.log_event("⏱️  Battle timeout - Enemy escaped!")
            return False

        victory = self.hero.is_alive()
        self.log_event(f"=== BATTLE END - {'VICTORY!' if victory else 'DEFEAT!'} ===")

        return victory


class ReportGenerator:
    """Generates battle reports in various formats."""

    @staticmethod
    def save_text_log(battle_log: List[str], filename: str = "game_log.txt"):
        """Save battle log to a text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Dungeon Battle Simulation Log\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write('\n'.join(battle_log))
        print(f"\n📝 Battle log saved to: {filename}")

    @staticmethod
    def generate_html_report(hero: Hero, enemy: Enemy, victory: bool,
                           battle_log: List[str], battle_date: str,
                           filename: str = "battle_report.html"):
        """Generate a styled HTML battle report."""

        hero_hp_percent = max(0, (hero.current_hp / hero.max_hp) * 100)
        enemy_hp_percent = max(0, (enemy.current_hp / enemy.max_hp) * 100)

        result_color = "#2ecc71" if victory else "#e74c3c"
        result_text = "⚔️ VICTORY!" if victory else "💀 DEFEAT"
        result_subtitle = "The hero emerges triumphant!" if victory else "The hero has fallen..."

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Battle Report - {hero.name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .header .date {{
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .result-banner {{
            background: {result_color};
            color: white;
            padding: 30px;
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .result-subtitle {{
            font-size: 0.5em;
            margin-top: 10px;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .battle-summary {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}

        .character-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border: 3px solid #dee2e6;
            transition: transform 0.3s;
        }}

        .character-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }}

        .character-card h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}

        .stat-row {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px;
            background: white;
            border-radius: 5px;
        }}

        .stat-label {{
            font-weight: bold;
            color: #555;
        }}

        .stat-value {{
            color: #2c3e50;
            font-weight: 600;
        }}

        .hp-bar-container {{
            margin: 20px 0;
        }}

        .hp-bar-label {{
            font-weight: bold;
            margin-bottom: 8px;
            color: #2c3e50;
        }}

        .hp-bar {{
            width: 100%;
            height: 30px;
            background: #ecf0f1;
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid #bdc3c7;
        }}

        .hp-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .hp-bar-fill.hero {{
            background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%);
        }}

        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-top: 10px;
        }}

        .badge-warrior {{
            background: #e67e22;
            color: white;
        }}

        .badge-mage {{
            background: #9b59b6;
            color: white;
        }}

        .badge-rogue {{
            background: #16a085;
            color: white;
        }}

        .badge-hardcore {{
            background: #c0392b;
            color: white;
            margin-left: 10px;
        }}

        .battle-log {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 25px;
            border-radius: 10px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.6;
        }}

        .battle-log h3 {{
            color: #3498db;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}

        .log-entry {{
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #3498db;
            padding-left: 10px;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #7f8c8d;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .battle-summary {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .result-banner {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗡️ Dungeon Battle Report 🗡️</h1>
            <div class="date">📅 Battle Date: {battle_date}</div>
        </div>

        <div class="result-banner">
            {result_text}
            <div class="result-subtitle">{result_subtitle}</div>
        </div>

        <div class="content">
            <div class="battle-summary">
                <div class="character-card">
                    <h2>🦸 Hero</h2>
                    <div class="stat-row">
                        <span class="stat-label">Name:</span>
                        <span class="stat-value">{hero.name}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Class:</span>
                        <span class="stat-value">{hero.hero_class}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Level:</span>
                        <span class="stat-value">{hero.level}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Attack:</span>
                        <span class="stat-value">{hero.attack}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Defense:</span>
                        <span class="stat-value">{hero.defense}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Crit Chance:</span>
                        <span class="stat-value">{hero.critical_chance:.1%}</span>
                    </div>
                    <div>
                        <span class="badge badge-{hero.hero_class.lower()}">{hero.hero_class}</span>
                        {f'<span class="badge badge-hardcore">HARDCORE</span>' if hero.hardcore_mode else ''}
                    </div>
                    <div class="hp-bar-container">
                        <div class="hp-bar-label">Health: {max(0, hero.current_hp)}/{hero.max_hp}</div>
                        <div class="hp-bar">
                            <div class="hp-bar-fill hero" style="width: {hero_hp_percent}%">
                                {hero_hp_percent:.0f}%
                            </div>
                        </div>
                    </div>
                </div>

                <div class="character-card">
                    <h2>👹 Enemy</h2>
                    <div class="stat-row">
                        <span class="stat-label">Name:</span>
                        <span class="stat-value">{enemy.name}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Level:</span>
                        <span class="stat-value">{enemy.level}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Attack:</span>
                        <span class="stat-value">{enemy.attack}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Defense:</span>
                        <span class="stat-value">{enemy.defense}</span>
                    </div>
                    <div class="hp-bar-container">
                        <div class="hp-bar-label">Health: {max(0, enemy.current_hp)}/{enemy.max_hp}</div>
                        <div class="hp-bar">
                            <div class="hp-bar-fill" style="width: {enemy_hp_percent}%">
                                {enemy_hp_percent:.0f}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="battle-log">
                <h3>📜 Battle Log</h3>
                {''.join([f'<div class="log-entry">{entry}</div>' for entry in battle_log])}
            </div>
        </div>

        <div class="footer">
            Generated by Dungeon Battle Simulator | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📊 HTML report saved to: {filename}")


def validate_arguments(args) -> None:
    """Validate command-line arguments and raise errors if invalid."""
    if args.level < 1 or args.level > 100:
        raise ValueError(f"Level must be between 1 and 100, got: {args.level}")

    if args.hero_class not in Hero.VALID_CLASSES:
        raise ValueError(f"Hero class must be one of {Hero.VALID_CLASSES}, got: {args.hero_class}")

    try:
        datetime.strptime(args.battle_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Battle date must be in YYYY-MM-DD format, got: {args.battle_date}")


def main():
    """Main entry point for the dungeon battle simulator."""
    parser = argparse.ArgumentParser(
        description='Dungeon Battle Simulator - A non-interactive game simulation for DevOps pipelines',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--player_name',
        type=str,
        required=True,
        help='The name of the hero'
    )

    parser.add_argument(
        '--hero_class',
        type=str,
        required=True,
        choices=Hero.VALID_CLASSES,
        help=f'The hero class: {", ".join(Hero.VALID_CLASSES)}'
    )

    parser.add_argument(
        '--level',
        type=int,
        required=True,
        help='The hero level (1-100)'
    )

    parser.add_argument(
        '--hardcore_mode',
        action='store_true',
        help='Enable hardcore mode for increased difficulty'
    )

    parser.add_argument(
        '--battle_date',
        type=str,
        required=True,
        help='Battle date in YYYY-MM-DD format'
    )

    args = parser.parse_args()

    try:
        validate_arguments(args)

        print("=" * 80)
        print("🏰 DUNGEON BATTLE SIMULATOR 🏰")
        print("=" * 80)
        print(f"Player: {args.player_name}")
        print(f"Class: {args.hero_class}")
        print(f"Level: {args.level}")
        print(f"Hardcore Mode: {'ON' if args.hardcore_mode else 'OFF'}")
        print(f"Battle Date: {args.battle_date}")
        print("=" * 80)
        print()

        hero = Hero(args.player_name, args.hero_class, args.level, args.hardcore_mode)
        enemy = Enemy(args.level, args.hardcore_mode)

        simulator = BattleSimulator(hero, enemy)
        victory = simulator.simulate_battle()

        print("\n" + "=" * 80)
        print("📁 GENERATING REPORTS...")
        print("=" * 80)

        ReportGenerator.save_text_log(simulator.battle_log)
        ReportGenerator.generate_html_report(
            hero, enemy, victory, simulator.battle_log, args.battle_date
        )

        print("\n" + "=" * 80)
        print("✅ SIMULATION COMPLETE")
        print("=" * 80)

        sys.exit(0 if victory else 1)

    except ValueError as e:
        print(f"❌ Validation Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
