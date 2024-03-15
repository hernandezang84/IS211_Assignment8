import random
import time
import argparse

random.seed(0)

class Game:

    def __init__(self):
        self.player_scores = [0, 0]
        self.player_names = ["Player 1", "Player 2"]
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self, player_name, current_score, is_human=True):
        turn_total = 0
        while True:
            print(f"{player_name}'s turn:")
            roll = self.roll_dice()
            print(f"Rolled: {roll}")

            if roll == 1:
                print("Sorry, no points this turn.")
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total} Game total: {current_score + turn_total}")

                if is_human:
                    decision = input("Choose 'r' to roll again or 'h' to hold: ").strip().lower()
                else:
                    decision = computer_strategy(current_score, turn_total)

                if decision == 'h':
                    break

        return turn_total
    
    def get_current_player(self):
        return self.player_names[self.current_player_index], self.player_scores[self.current_player_index]
    
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def is_game_over(self):
        return any(score >= 100 for score in self.player_scores)
    
    def declare_winner(self):
        winner_index = self.player_scores.index(max(self.player_scores))
        print(f"{self.player_names[winner_index]} wins with {self.player_scores[winner_index]} points!")

def computer_strategy(current_score, turn_total):
    if turn_total >= 25 or current_score + turn_total >= 100:
        return 'h'
    return 'r'

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()
    
    def play_game(self):
        while not self.game.is_game_over():
            player_name, current_score = self.game.get_current_player()
            turn_total = self.game.play_turn(player_name, current_score, is_human=(player_name == 'Player 1'))
            self.game.player_scores[self.game.current_player_index] += turn_total
            if self.game.is_game_over() or time.time() - self.start_time >= 60:
                print("Time's up!")
                self.game.declare_winner()
                break
            self.game.switch_player()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Play the Timed Pig game.")
    parser.add_argument('--timed', action='store_true', help="Enable timed mode.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    game = Game()

    if args.timed:
        game = TimedGameProxy(game)

    game.play_game()

if __name__ == "__main__":
    main()