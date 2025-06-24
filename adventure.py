"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from adventure_game_entity import AdventureGame
from game_entities import Player
from adventure_helper import (DROPOUT_NUMBER, GAMEOVER_CONSTANT, SLEEPY_NUMBER, menu_function,
                              ending, non_menu_function_int, non_menu_function_str, pickup_event)
from proj1_event_logger import Event, EventList

if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 3)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "energy", "wallet", "undo", "log",
            "quit"]  # Regular menu options available at each location
    choice = None
    create_new_event = True

    while game.ongoing:
        if game.current_player_state.energy <= 0:
            game.current_location_id = SLEEPY_NUMBER

        current_location = game.get_location()  # gets current location object

        if create_new_event:
            event_id = current_location.id_num
            event_desc = current_location.descriptions[0]
            event_player = Player(game.current_player_state.inventory.copy(), game.current_player_state.energy,
                                  game.current_player_state.score, game.current_player_state.wallet)
            event_location_items = game.get_location().items.copy()
            game_log.add_event(Event(event_id, event_desc, event_player, event_location_items), choice)

        if current_location.id_num >= DROPOUT_NUMBER:
            ending(game, game.current_player_state)
            quit()

        if current_location.visited:
            print("LOCATION: ", current_location.name)
            print(current_location.descriptions[0])

        else:
            print("LOCATION: ", current_location.name)
            print(current_location.descriptions[1])
            current_location.visited = True

        print()

        pickup_commands = {}
        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, energy, wallet, undo, log, quit")
        print("At this location, you can also:")
        for action in current_location.available_commands:
            print("-", action)
        for item in current_location.items:
            print("- pick up", item)
            pickup_commands["pick up " + item] = item

        print("\nEnergy remaining: ", game.current_player_state.energy)
        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in current_location.available_commands and choice not in menu and \
                choice not in pickup_commands:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            create_new_event = menu_function(game, choice, current_location, game_log)

            if game.current_location_id == GAMEOVER_CONSTANT:
                game.ongoing = False

        elif choice in pickup_commands:
            create_new_event = True
            pickup_event(game, pickup_commands, choice)

        else:
            result = current_location.available_commands[choice]
            if isinstance(result, int):
                create_new_event = non_menu_function_int(result, game, current_location, game.current_player_state)
            else:
                create_new_event = non_menu_function_str(result, game, game.current_player_state)

        print("========")
