"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations

from adventure_helper import (DROPOUT_NUMBER, GAMEOVER_CONSTANT, SLEEPY_NUMBER, sim_non_menu_function_int,
                              sim_non_menu_function_str, simulation_pickup_event, simulation_menu_function)
from proj1_event_logger import Event, EventList
from game_entities import Player, Location
from adventure_game_entity import AdventureGame


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)
        self._events.add_event(Event(initial_location_id, self._game.get_location().descriptions[0],
                                     self._game.current_player_state, self._game.get_location().items))
        self.generate_events(commands, self._game.get_location())

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game

        """

        menu = ["look", "inventory", "score", "energy", "wallet", "undo", "log",
                "quit"]  # Regular menu options available at each location
        self._game.ongoing = True

        index = 0
        while index < len(commands) and self._game.ongoing:
            pickup_commands = {}
            for item in current_location.items:
                pickup_commands["pick up " + item] = item

            if commands[index] in menu:
                data_menu = simulation_menu_function(self._game, current_location, self._events, commands, index)
                create_new_event = data_menu[0]
                index = data_menu[1]

                if self._game.current_location_id == GAMEOVER_CONSTANT:
                    self._game.ongoing = False
                    break

            elif commands[index] in pickup_commands:
                create_new_event = True
                simulation_pickup_event(self._game, pickup_commands, commands[index])

            else:
                result = current_location.available_commands[commands[index]]

                if isinstance(result, int):
                    info = sim_non_menu_function_int(result, self._game, current_location, commands, index)
                else:
                    info = sim_non_menu_function_str(result, self._game, index)
                create_new_event = info[0]
                index = info[1]

                if self._game.current_player_state.energy <= 0:
                    self._game.current_location_id = SLEEPY_NUMBER

            if create_new_event:
                event_id = self._game.current_location_id
                event_desc = self._game.get_location().descriptions[0]
                event_player = Player(self._game.current_player_state.inventory.copy(),
                                      self._game.current_player_state.energy,
                                      self._game.current_player_state.score, self._game.current_player_state.wallet)
                event_location_items = self._game.get_location().items.copy()
                self._events.add_event(Event(event_id, event_desc, event_player, event_location_items), commands[index])
                if current_location.id_num >= DROPOUT_NUMBER:
                    break

            current_location = self._game.get_location()
            index += 1

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # WIN WALKTHROUGHS
    # There are multiple ways to "win" the game as I coded multiple endings. Each ending depends on the kind
    # of items brought to Sadia at the end of the game, or if you followed a side quest. In terms of good
    # endings, there are 3 of them.

    # Win 1: Regular Schmegular Computer Science Student
    # This win is doing the bare minimum, bringing the required items to Sadia.
    baseline_win_walkthrough = ["go west", "go west", "go south", "pick up charger", "go north", "exit building",
                                "go north", "go west", "go up", "pick up usb", "go down", "exit building", "go south",
                                "go south", "go east", "go east", "pick up lucky mug", "go west", "exit building",
                                "go west", "go up", "go up", "go up", "submit project to sadia"]
    expected_log = [3, 2, 22, 24, 24, 22, 2, 1, 12, 11, 11, 12, 1, 2, 4, 41, 42, 42, 41, 4, 34, 33, 32, 31, 100]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, baseline_win_walkthrough).get_id_log()

    # Win 2: Sadia's Favourite Student
    # This win requires you to explore and talk with all the characters in the game in order to figure out what
    # items Sadia likes. You then must gather the supplies and purchase them at the three different vendor locations,
    # then make your way back to Bahen 4F.
    true_win_walkthrough = ["go west", "go south", "go west", "pick up toonie", "exit building",
                            "talk to market vendor", "purchase bandana", "go east", "go east", "pick up lucky mug",
                            "go west", "exit building", "go north", "go west", "buy from vending machine",
                            "buy sour patch kids", "go south", "pick up charger", "go north", "exit building",
                            "go north", "go west", "go up", "pick up usb", "purchase food from starbucks",
                            "buy matcha", "go down", "exit building", "go south", "go south", "go west", "go up",
                            "go up", "go up", "submit project to sadia"]
    expected_log = [3, 2, 4, 34, 34, 4, 4, 41, 42, 42, 41, 4, 2, 22, 22, 24, 24, 22, 2, 1, 12, 11, 11, 11, 12, 1, 2, 4,
                    34, 33, 32, 31, 100]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, true_win_walkthrough).get_id_log()

    # Win 3: Super Saiyann
    # This win requires you to notice that on Bahen 3F, the fan fiction club is looking for a purple book. The vendor
    # sells a vintage book which once you "look" at it, is purple. Show it to the fan fiction club and you get a
    # secret ending.
    secret_win_walkthrough = ["go west", "go south", "talk to market vendor", "purchase vintage book", "go west",
                              "go up", "go up", "inventory", "vintage book", "show"]
    expected_log = [3, 2, 4, 4, 34, 33, 32, 92]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, secret_win_walkthrough).get_id_log()

    # =================================================================================================================

    # LOSE WALKTHROUGHS
    # There are three ways to lose. Each way depends on doing certain interactions within the game.

    # Lose 1: Math Major for Life (used up all your energy)
    # This lose requires the player to do a move 45 times without purchasing and eating anything (as to not replenish
    # energy status). This will cause the player to run out of moves.
    timeout_demo = ["go west", "go east", "go west", "go east", "go west", "go east", "go west", "go east",
                    "go west", "go east", "go west", "go east", "go west", "go east", "go west", "go east",
                    "go west", "go east", "go west", "go east", "go west", "go east", "go west", "go east",
                    "go west", "go east", "go west", "go east", "go west", "go east", "go west", "go east",
                    "go west", "go east", "go west", "go east", "go west", "go east", "go west", "go east",
                    "go west", "go east", "go west", "go east", "go west"]
    expected_log = [3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2,
                    3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 93]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, timeout_demo).get_id_log()

    # Lose 2: Stranded in Toronto (dropout)
    # This lose requires you to go to guidance then ask to dropout of school. It will immediately end the game.
    dropout_walkthrough = ["go west", "go west", "go west", "go south", "ask to dropout"]
    expected_log = [3, 2, 22, 21, 23, 91]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, dropout_walkthrough).get_id_log()

    # Lose 3: You (Almost) Killed Your Prof
    # This lose requires you to go throughout the game to retrieve all the mandatory items in the game and an
    # egg sandwich and bring it to Sadia. She's allergic.
    allergic_walkthrough = ["go west", "go north", "go west", "go up", "pick up usb", "purchase food from starbucks",
                            "buy egg sandwich", "go down", "exit building", "go south", "go west", "go south",
                            "pick up charger", "go north", "exit building", "go south", "go east", "go east",
                            "pick up lucky mug", "go west", "exit building", "go west", "go up", "go up", "go up",
                            "submit project to sadia"]
    expected_log = [3, 2, 1, 12, 11, 11, 11, 12, 1, 2, 22, 24, 24, 22, 2, 4, 41, 42, 42, 41, 4, 34, 33, 32, 31, 100]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, allergic_walkthrough).get_id_log()

    # =================================================================================================================

    # FEATURES/ENHANCEMENT

    # Inventory/Drop/Pick Up Demo
    inventory_demo = ["pick up plan", "go west", "buy hotdog", "go west", "go south", "pick up charger", "go north",
                      "go west", "inventory", "hotdog", "drop", "go east", "go west", "pick up hotdog", "go east",
                      "exit building", "go north", "go west", "go up", "purchase food from starbucks", "buy pink drink",
                      "pick up usb", "inventory", "plan", "look", "quit"]
    expected_log = [3, 3, 2, 2, 22, 24, 24, 22, 21, 21, 22, 21, 21, 22, 2, 1, 12, 11, 11, 11]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, inventory_demo).get_id_log()

    # Score Demo (increasing score by picking up three objects)
    score_demo = ["pick up plan", "go west", "buy hotdog", "go south", "go west", "pick up toonie", "score", "quit"]
    expected_log = [3, 3, 2, 2, 4, 34, 34]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, score_demo).get_id_log()

    # Energy Demo (increasing number of moves by eating a consumable)
    energy_demo = ["go west", "go south", "go west", "pick up toonie", "exit building", "go north", "go west",
                   "buy from vending machine", "buy welches", "energy", "inventory", "welches", "eat", "energy",
                   "quit"]
    expected_log = [3, 2, 4, 34, 34, 4, 2, 22, 22]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, energy_demo).get_id_log()

    # Money/Wallet Demo (purchasing items until insufficient funds)
    money_demo = ["go west", "buy hotdog", "wallet", "go south", "talk to market vendor", "purchase socks", "wallet",
                  "go north", "go north", "go west", "go up", "purchase food from starbucks", "buy coffee", "wallet",
                  "quit"]
    expected_log = [3, 2, 2, 4, 4, 2, 1, 12, 11, 11]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, money_demo).get_id_log()

    # Quiz Interaction Demo (recieving a stuffie for helping a npc)
    quiz_demo = ["go west", "go north", "talk to student", "human", "inventory", "stuffie", "look", "quit"]
    expected_log = [3, 2, 1, 1]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, quiz_demo).get_id_log()

    # All Interactions Demo
    interactions_demo = ["go west", "go west", "go west", "go south", "ask for life advice",
                         "ask if they know anything about sadia", "go north", "go east", "exit building", "go north",
                         "go west", "talk to student", "continue", "exit building", "go south", "go south", "go east",
                         "talk with buddy", "continue", "quit"]
    expected_log = [3, 2, 22, 21, 23, 23, 23, 21, 22, 2, 1, 12, 12, 1, 2, 4, 41, 41]
    assert expected_log == AdventureGameSimulation('game_data.json', 3, interactions_demo).get_id_log()
