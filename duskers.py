import random, time, argparse, os, json
from datetime import datetime


TITLE = """
░█████╗░██████╗░███████╗███╗░░██╗
██╔══██╗██╔══██╗██╔════╝████╗░██║
██║░░██║██████╔╝█████╗░░██╔██╗██║
██║░░██║██╔═══╝░██╔══╝░░██║╚████║
╚█████╔╝██║░░░░░███████╗██║░╚███║
░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚══╝
+++++++++++++++++++++++++++++++++
"""

ROBOT_IMAGE = """  $   $$$$$$$   $  
  $$$$$     $$$$$  
      $$$$$$$      
     $$$   $$$     
     $       $     """

ADD_ROBOT = """|  $   $$$$$$$   $  
|  $$$$$     $$$$$  
|      $$$$$$$      
|     $$$   $$$     
|     $       $     """

LINE = "+==============================================================================+"

HUB_DOWN = """+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+
"""

MENU_SCREEN = """
                          |==========================|
                          |            MENU          |
                          |                          |
                          | [Back] to game           |
                          | Return to [Main] Menu    |
                          | [Save] and exit          |
                          | [Exit] game              |
                          |==========================|
"""

SAVE_SCREEN = """
                        |==============================|
                        |    GAME SAVED SUCCESSFULLY   |
                        |==============================|"""

LOAD_SCREEN = """
                        |==============================|
                        |   GAME LOADED SUCCESSFULLY   |
                        |==============================|"""

SHOP_SCREEN = """
                       |================================|
                       |          UPGRADE STORE         |
                       |                         Price  |
                       | [1] Titanium Scan         250  |
                       | [2] Enemy Encounter Scan  500  |
                       | [3] New Robot            1000  |
                       |                                |
                       | [Back]                         |
                       |================================|
"""

OVER_SCREEN = """
                        |==============================|
                        |          GAME OVER!          |
                        |==============================|
"""


class Duskers:
    def __init__(self, locations: list, max_time: int, waiting_time: int):
        self.player = ""
        self.menu_display = ["[New]  Game", "[Load] Game", "[High] Scores", "[Help]", "[Exit]"]
        self.all_locations = locations
        self.max_time = max_time
        self.waiting_time = waiting_time
        self.titanium = 0
        self.saved_games = {"1": {'saved': False}, "2": {'saved': False}, "3": {'saved': False}}
        self.show_titanium = False
        self.show_encounter = False
        self.num_robots = 3

    def menu(self) -> None:
        print(TITLE)
        print(*self.menu_display, sep="\n")
        game_status = True
        menu_actions = {
            "new": self.play_option,
            "load": self.load_option,
            "high": self.high_scores,
            "help": self.help_option,
            "exit": self.exit_option
        }

        while game_status:
            menu_choice = self.valid_command(["new", "load", "exit", "high", "help"])
            game_status = menu_actions[menu_choice]()

    @staticmethod
    def exit_option() -> bool:
        print("Thanks for playing, bye!")
        return False  # the return value is for game_status

    @staticmethod
    def valid_command(commands: list) -> str:
        while True:
            command = input("\nYour command:").lower()
            if command in commands:
                return command
            print("Invalid input")

    # This is the option for new game:
    def play_option(self) -> bool:
        self.player = input("Enter your name:")
        print(f"\nGreetings, commander {self.player}!")

        while True:
            print("Are you ready to begin?\n[Yes] [No] Return to Main[Menu]")
            play_choice = self.valid_command(["yes", "no", "menu"])
            if play_choice == "yes":
                action = self.hub_option()
                return action
            elif play_choice == "no":
                print("How about now.")
            elif play_choice == "menu":
                self.menu()

    def load_option(self) -> bool:
        while True:
            self.show_saved()

            load_choice = self.valid_command(["back", "1", "2", "3"])
            if load_choice == "back":
                self.menu()
                break
            elif self.saved_games[load_choice]['saved']:
                self.player = self.saved_games[load_choice]['player']
                self.titanium = self.saved_games[load_choice]['Titanium']
                self.num_robots = self.saved_games[load_choice]['Robots']
                self.show_titanium = self.saved_games[load_choice]['Show Titanium']
                self.show_encounter = self.saved_games[load_choice]['Show Chance of Encounter']
                print(LOAD_SCREEN)
                print(f" Welcome back, commander {self.player}!")
                action = self.hub_option()
                return action
            else:
                print("Empty slot!\n")
                continue

    def high_scores(self) -> None:
        if os.path.isfile("high_scores.json"):
            print("\n	HIGH SCORES\n")
            with open("high_scores.json", 'r') as scores_file:
                scores_dict = json.load(scores_file)
                sorted_scores = dict(sorted(scores_dict.items(), key=lambda item: item[1], reverse=True))

                players = [key.split('|')[1] for key in sorted_scores.keys()]
                scores = list(sorted_scores.values())
                for i in range(min(len(sorted_scores), 10)):
                    print(f"({i + 1}) {players[i]} {scores[i]}")
                print("\n	[Back]")

        else:
            print("No scores to display.\n	[Back]")
        score_choice = self.valid_command(["back"])
        if score_choice == "back":
            self.menu()

    @staticmethod
    def help_option() -> bool:
        print("Coming SOON! Thanks for playing!")
        return False  # the return value is for game_status

    def explore_option(self) -> bool:
        n_search = random.randint(1, 9)
        searched_locations = {}

        for i in range(1, n_search + 1):
            self.waiting_for_action("Searching")
            location = random.choice(self.all_locations)
            searched_locations[str(i)] = {"name": location.replace("_", " "),
                                          "titanium": random.randint(10, 100),
                                          "encounter": random.random()}
            for loc_index in searched_locations:
                print(f"[{loc_index}] {searched_locations[loc_index]['name']}", end="")
                if self.show_titanium:
                    print(f" Titanium: {searched_locations[loc_index]['titanium']}", end="")
                if self.show_encounter:
                    print(f" Encounter rate: {round(searched_locations[loc_index]['encounter'] * 100, 0)}%", end="")
                print()

            print("\n[S] to continue searching")
            ex_choice = self.valid_command(["back", "s"] + list(searched_locations.keys()))
            if ex_choice == "back":
                action = self.hub_option()
                return action
            elif ex_choice == "s":
                continue
            else:
                action = self.ex_location(searched_locations[ex_choice]['name'],
                                          searched_locations[ex_choice]['titanium'],
                                          searched_locations[ex_choice]['encounter'])

                return action

        print("Nothing more in sight.\n       [Back]")
        back_choice = self.valid_command(["back"] + list(searched_locations.keys()))
        if back_choice == "back":
            action = self.hub_option()
        else:
            action = self.ex_location(searched_locations[back_choice]['name'],
                                      searched_locations[back_choice]['titanium'],
                                      searched_locations[back_choice]['encounter'])
            # add the number of robots
        return action

    def upgrade_option(self) -> bool:
        print(SHOP_SCREEN)
        while True:
            up_choice = self.valid_command(["back", "1", "2", "3"])
            if up_choice == "1":
                if self.titanium > 250:
                    self.titanium -= 250
                    self.show_titanium = True
                    print("Purchase successful. You can now see how much titanium you can get from each found location.")
                    break
                else:
                    print("Purchase unsuccessful. You don't have enough titanium.")
                    continue
            elif up_choice == "2":
                if self.titanium > 500:
                    self.titanium -= 500
                    self.show_encounter = True
                    print("Purchase successful. You will now see how likely you will encounter an enemy at each found location.")
                    break
                else:
                    print("Purchase unsuccessful. You don't have enough titanium.")
                    continue

            elif up_choice == "3":
                if self.titanium > 500:
                    self.titanium -= 1000
                    self.num_robots += 1
                    print("Purchase successful. You now have an additional robot.")
                    break
                else:
                    print("Purchase unsuccessful. You don't have enough titanium.")
                    continue

            else:
                break

        action = self.hub_option()
        return action

    def save_option(self) -> bool:
        while True:
            self.show_saved()

            save_choice = self.valid_command(["back", "1", "2", "3"])
            if save_choice == "back":
                self.menu()
                break
            else:
                self.saved_games[save_choice]['saved'] = True
                self.saved_games[save_choice]['player'] = self.player
                self.saved_games[save_choice]['Titanium'] = self.titanium
                self.saved_games[save_choice]['Robots'] = self.num_robots
                self.saved_games[save_choice]['Last save'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.saved_games[save_choice]['Show Titanium'] = self.show_titanium
                self.saved_games[save_choice]['Show Chance of Encounter'] = self.show_encounter
                with open("save_file.txt", "w") as json_file:
                    json.dump(self.saved_games, json_file)
                print(SAVE_SCREEN)
                action = self.hub_option()
                return action

    def menu_option(self) -> bool:
        print(MENU_SCREEN)
        choice = self.valid_command(["back", "main", "save", "exit"])

        choice_actions = {
            "back": self.hub_option,
            "main": self.menu,
            "save": self.save_option,
            "exit": self.exit_option
        }
        action = choice_actions[choice]()
        return action

    def hub_option(self) -> bool:
        print(LINE)
        if self.num_robots >= 1:
            self.show_robots(self.num_robots)
        print(LINE)
        print("| Titanium:", str(self.titanium).ljust(66), "|")
        print(HUB_DOWN)
        game_choice = self.valid_command(["ex", "up", "save", "m"])

        game_actions = {
            "ex": self.explore_option,
            "up": self.upgrade_option,
            "save": self.save_option,
            "m": self.menu_option
        }

        action = game_actions[game_choice]()
        return action

    def ex_location(self, location_name: str, location_titanium: int, encounter: float) -> bool:
        self.waiting_for_action("Deploying robots")
        meet = random.random()
        if meet < encounter:
            self.num_robots -= 1
            if self.num_robots <= 0:
                print("Enemy encounter!!!\nMission aborted, the last robot lost...")
                time_key = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_score = {f"{time_key}|{self.player}": self.titanium}

                # save the player and score in "high_scores.json"
                if os.path.isfile('high_scores.json'):
                    with open('high_scores.json', 'r') as score_file:
                        file_data = json.load(score_file)
                        file_data.update(new_score)
                    with open('high_scores.json', 'w') as write_file:
                        json.dump(file_data, write_file)
                else:
                    with open('high_scores.json', 'w') as score_file:
                        json.dump(new_score, score_file)

                print(OVER_SCREEN)
                self.player = ""
                self.num_robots = 3
                self.titanium = 0
                self.show_titanium = False
                self.show_encounter = False
                self.menu()
                # return False

            else:
                print("Enemy encounter\nfirst explored successfully, 1 robot lost...")
                print(f"Acquired {location_titanium} lumps of titanium")
                self.titanium += location_titanium
                action = self.hub_option()
                return action

        else:
            print(f"{location_name} explored successfully, with no damage taken.")
            print(f"Acquired {location_titanium} lumps of titanium")
            self.titanium += location_titanium
            action = self.hub_option()
            return action

    def waiting_for_action(self, phrase: str) -> None:
        print(phrase, end='')
        if self.max_time > 0:
            for _ in range(self.waiting_time):
                print(".", end='', flush=True)
                time.sleep(0.5)
        print()

    @staticmethod
    def show_robots(num: int) -> None:
        robot_list = [ROBOT_IMAGE] + [ADD_ROBOT] * (num - 1)

        # Split each multiline string by newline
        robots_by_column = [s.split('\n') for s in robot_list]
        robots_by_line = zip(*robots_by_column)

        for parts in robots_by_line:
            for line in parts:
                print(''.join(line), end='')
            print()

    def show_saved(self) -> None:
        if os.path.isfile("save_file.txt"):
            with open("save_file.txt", 'r') as json_file:
                self.saved_games = json.load(json_file)

        print("   Select save slot:")
        for slot, game in self.saved_games.items():
            if game["saved"]:
                print(f"    [{slot}] {game['player']}", end=" ")
                for key, value in game.items():
                    print(f"{key}: {value}", end=" ")
                print()
            else:
                print(f"    [{slot}] empty")


def main():
    default_locations = "Gondobar,Gondothlimbar,Gondolin,Gwarestrin,Gar_hurion,Loth,Lothengriol"
    parser = argparse.ArgumentParser()
    parser.add_argument('random_seed', type=str, default="10", nargs="?")
    parser.add_argument('min_time', type=int, default=0, nargs="?")
    parser.add_argument('max_time', type=int, default=7, nargs="?")
    parser.add_argument('locations', type=str, default=default_locations, nargs="?")

    args = parser.parse_args()
    locations = args.locations.split(",")

    if args.min_time > args.max_time > 0:
        print("The minimum time should be smaller than the maximum time")
    else:
        waiting_time = random.randint(args.min_time, args.max_time)
        random.seed(args.random_seed)

        duskers = Duskers(locations, args.max_time, waiting_time)
        duskers.menu()


if __name__ == "__main__":
    main()
