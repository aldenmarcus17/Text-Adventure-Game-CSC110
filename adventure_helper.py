"""CSC111 Project 1: Text Adventure Game - Adventure Helper Functions

===============================

This Python module contains the helper_functions required to run 'adventure.py' and 'proj1_simulation.py'.

===============================
"""
from typing import Any
from adventure_game_entity import AdventureGame
from game_entities import Location, Player, Item
from proj1_event_logger import EventList


# module-level constants
INTERACTION_NUMBER = -5
GAMEOVER_CONSTANT = -100
PICKUP_CONSTANT = 5
DROPOUT_NUMBER = 91
FANFIC_NUMBER = 92
SLEEPY_NUMBER = 93
SADIA_NUMBER = 100


def interaction_manager_helper(chosen_item: Item, s_player_state: Player) -> None:
    """Adjusts current player state depending on what interaction they chose. This is a helper function
    made to make readability easire of the actual interaction_manager function.

    Preconditions:
        - All imported objects have valid instance attributes
        - isinstance(chosen_item.cost, (str, int))

    >>> ex_adventure_game = AdventureGame("game_data.json", 3)
    >>> ex_adventure_game.current_player_state.wallet = 4
    >>> interaction_manager_helper(ex_adventure_game.get_item("matcha"), ex_adventure_game.current_player_state)
    It seems your broke and can't afford this... Oh well.
    >>> "matcha" in ex_adventure_game.current_player_state.inventory
    False

    >>> ex_adventure_game.current_player_state.wallet = 10
    >>> interaction_manager_helper(ex_adventure_game.get_item("matcha"), ex_adventure_game.current_player_state)
    You recieved matcha
    Yum! The matcha is perfectly iced and has some oat milk on top.

    >>> ex_adventure_game.current_player_state.wallet == 2
    True

    """
    if isinstance(chosen_item.cost, int):  # checks if item costs money/item cost is an int
        if chosen_item.commands == {}:  # checks if the Item.commands is empty, if it is this is the incorrect
            # answer for student interaction.
            print("The student gives you a ", chosen_item.name)
            print(chosen_item.itemget_description)
        elif chosen_item.cost > s_player_state.wallet:  # checks if player does not have enough money
            print("It seems your broke and can't afford this... Oh well.")
            s_player_state.energy += 1
        else:  # player has enough money/can recieve the item
            print("You recieved", chosen_item.name)
            print(chosen_item.itemget_description)
            s_player_state.wallet -= chosen_item.cost
            s_player_state.score += PICKUP_CONSTANT
            s_player_state.inventory[chosen_item.name] = chosen_item

    else:  # checks if cost was a string (implying either no cost, or "toonie" cost)
        if chosen_item.cost == "":
            s_player_state.inventory[chosen_item.name] = chosen_item
            print("You recieved ", chosen_item.name)
            print(chosen_item.itemget_description)
            s_player_state.score += PICKUP_CONSTANT

        elif chosen_item.cost in s_player_state.inventory:
            s_player_state.inventory.pop(chosen_item.cost)
            s_player_state.inventory[chosen_item.name] = chosen_item
            print("You recieved ", chosen_item.name)
            print(chosen_item.itemget_description)
            s_player_state.score += PICKUP_CONSTANT

        else:
            print("You do not have the required item to do this.")


def interaction_manager(s_game: AdventureGame, location: Location, s_player_state: Player) -> None:
    """Deals with special interaction within locations. There are two types of interactions: selection interactions
    and dialogue interactions. Outputs UI and updates player_state, specifically the inventory.

    Preconditions
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 1)
    >>> ex_adventure_game.current_player_state.inventory["stuffie"] = ex_adventure_game.get_item("stuffie")
    >>> interaction_manager(ex_adventure_game, ex_adventure_game.get_location(), ex_adventure_game.current_player_state)
    You already helped this person!
    """
    print(location.interaction_info[0])
    if "human" in location.interaction_info[1] and "stuffie" in s_player_state.inventory:  # Prevents helping x2
        print("You already helped this person!")

    if location.interaction_info[1] == {}:  # dialogue interaction, no user selection
        print("Type 'continue' to continue")
        sub_choice = input("\nEnter action: ").lower().strip()
        while sub_choice != 'continue':
            print("That was an invalid option; try again.")
            sub_choice = input("\nEnter action: ").lower().strip()

    else:  # selection interaction, deals with selecting new option/action
        print("What to do? Choose from: ")
        for sub_action in location.interaction_info[1]:
            print("-", sub_action)

        sub_choice = input("\nEnter action: ").lower().strip()
        while sub_choice not in location.interaction_info[1]:
            print("That was an invalid option; try again.")
            sub_choice = input("\nEnter action: ").lower().strip()

        chosen_item = s_game.get_item(location.interaction_info[1][sub_choice])
        interaction_manager_helper(chosen_item, s_player_state)


def inventory_actions(s_game: AdventureGame, location: Location) -> bool:
    """Deals with inventory actions along with adjusting player states depending on what the user does.
    Returns a boolean containing whether the action counted as an event.

    Preconditions
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 3)
    >>> inventory_actions(ex_adventure_game, ex_adventure_game.get_location())
    There is nothing in your inventory.
    False

    """
    food_energy = 10

    if s_game.current_player_state.inventory == {}:
        print("There is nothing in your inventory.")
        return False
    else:
        print("Choose item to interact with:")
        for item in s_game.current_player_state.inventory:
            print("-", item)

        item_choice = input("\nEnter item: ").lower().strip()
        while item_choice not in s_game.current_player_state.inventory:
            print("That was an invalid option; try again.")
            item_choice = input("\nEnter item: ").lower().strip()

        item_obj = s_game.get_item(item_choice)

        print("Choose action:")
        for command in item_obj.commands:
            print("-", command)

        action_choice = input("\nEnter action: ").lower().strip()
        while action_choice not in item_obj.commands:
            print("That was an invalid option; try again.")
            action_choice = input("\nEnter action: ").lower().strip()

        if action_choice == "look":
            print(item_obj.commands[action_choice])
            return False

        elif action_choice == "eat":
            print("This sweet treat will go a long way. Your energy has been increased by ", food_energy)
            s_game.current_player_state.energy += food_energy
            s_game.current_player_state.inventory.pop(item_obj.name)
            return False

        elif action_choice == "drop":
            s_game.get_location().items += [s_game.current_player_state.inventory.pop(item_obj.name).name]
            s_game.current_player_state.energy -= 1
            return True

        elif action_choice == "show" and location.id_num == 32:
            s_game.current_location_id = 92
            return True

        else:
            print("No one here cares about your book. Literally no one. Wrong crowd.")
            return False


def menu_function(m_game: AdventureGame, m_choice: str, m_current_location: Location, m_game_log: EventList) -> bool:
    """Deals with menu actions. Updates the UI and also adjusts player_state, game_log, or the current_location
    depending on the action taken by the user. Returns a boolean that confirms whether the action should be counted
    as an event.

    Preconditions:
        - m_choice in ["look", "inventory", "score", "energy", "wallet", "undo", "log", "quit"]
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 1)
    >>> ex_adventure_game.current_player_state.energy = 5
    >>> ex_events = EventList()
    >>> menu_function(ex_adventure_game, "energy", ex_adventure_game.get_location(), ex_events)
    current energy: 5
    energy can be increased by eating food or drinking a drink.
    False

    >>> menu_function(ex_adventure_game, "inventory", ex_adventure_game.get_location(), ex_events)
    There is nothing in your inventory.
    False
    """
    if m_choice == "look":
        print(m_current_location.descriptions[1])
        return False

    elif m_choice == "inventory":
        count_as_event = inventory_actions(m_game, m_current_location)
        return count_as_event

    elif m_choice == "score":
        print("current score: ", m_game.current_player_state.score)
        print("score increases based on items picked up, items possessed at the end of the game, and energy ",
              "at the end of the game.")
        return False

    elif m_choice == "energy":
        print("current energy:", m_game.current_player_state.energy)
        print("energy can be increased by eating food or drinking a drink.")
        return False

    elif m_choice == "wallet":
        print("current bank account: $", m_game.current_player_state.wallet)
        return False

    elif m_choice == "undo" and m_game_log.last != m_game_log.first:
        m_game_log.remove_last_event()
        m_game.current_location_id = m_game_log.last.id_num
        m_game.get_location().items = m_game_log.last.location_items
        m_game.current_player_state = m_game_log.last.player_state
        return False

    elif m_choice == "log":
        m_game_log.display_events()
        return False

    elif m_choice == "quit":
        print("fine... give up then ig :( ")
        m_game.current_location_id = -100
        return False

    return False


def non_menu_function_int(game_value: int, sub_game: AdventureGame, sub_current_location: Location,
                          sub_player_state: Player) -> bool:
    """Deals with non-menu actions where the call (game_value) is an integer. This will specifically deal with movement
    of locations, and defining what the location id is, along with updating energy. Returns a boolean of whether this
    action should create an event.

    Preconditions
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 2)
    >>> sub_player = ex_adventure_game.current_player_state
    >>> non_menu_function_int(22, ex_adventure_game, ex_adventure_game.get_location(), sub_player)
    True
    >>> ex_adventure_game.current_location_id == 22
    True

    >>> ex_adventure_game.current_location_id = 31
    >>> non_menu_function_int(SADIA_NUMBER, ex_adventure_game, ex_adventure_game.get_location(), sub_player)
    You're missing one or more of the following items: usb, charger, lucky mug.
    False
    """
    if game_value == INTERACTION_NUMBER:  # special interaction
        interaction_manager(sub_game, sub_current_location, sub_player_state)
        sub_game.current_player_state.energy -= 1
        return True

    elif game_value < DROPOUT_NUMBER:  # regular movement
        sub_game.current_location_id = game_value
        sub_game.current_player_state.energy -= 1
        return True

    elif game_value == SADIA_NUMBER:
        if "usb" in sub_player_state.inventory and "charger" in sub_player_state.inventory and "lucky mug" \
                in sub_player_state.inventory:
            sub_game.current_location_id = game_value
            sub_game.current_player_state.energy -= 1
            return True
        else:
            print("You're missing one or more of the following items: usb, charger, lucky mug.")
            return False

    elif game_value == DROPOUT_NUMBER:
        sub_game.current_location_id = game_value
        sub_game.current_player_state.energy -= 1
        return True

    return False


def non_menu_function_str(game_value: str, sub_game: AdventureGame, sub_player_state: Player) -> bool:
    """Deals with non-menu actions that have a call (game_value) that is a string, specifically interactions and item
    pickups. Will update the current player state to reflect the new inventory, and also adjust the player's energy.
    Returns a boolean of whether this action should create an event.

    Preconditions
        - sub_game.get_item(game_value).commands == {} or sub_game.get_item(game_value).name == "hotdog"
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 23)
    >>> sub_player = ex_adventure_game.current_player_state
    >>> non_menu_function_str("life advice", ex_adventure_game, sub_player)
    You ask for life advice, and they give you a look up and down and frown. Ouch.
    True

    >>> ex_adventure_game.current_location_id = 2
    >>> non_menu_function_str("hotdog", ex_adventure_game, sub_player)
    Yummy! Don't forget to add toppings!
    True
    """
    if sub_game.get_item(game_value).commands == {}:  # special dialogue
        print(sub_game.get_item(game_value).itemget_description)
        sub_game.current_player_state.energy -= 1
        return True

    else:  # hotdog pick up
        new_item = sub_game.get_item(game_value)
        if new_item.cost > sub_player_state.wallet:
            print("You can't afford this!")
            return False
        elif new_item.name in sub_player_state.inventory:
            print("You already have one... eat it first. And don't try to drop it then buy one then",
                  "pick it up, some other person is gonna steal the one you dropped.")
            return False
        else:
            sub_player_state.inventory[game_value] = new_item
            sub_player_state.score += PICKUP_CONSTANT
            sub_game.current_player_state.wallet -= new_item.cost
            print(new_item.itemget_description)
            sub_game.current_player_state.energy -= 1
            return True


def ending(e_game: AdventureGame, e_player: Player) -> None:
    """Handles the ending sequences. Uses e_game to use current_id along with e_player.score to select a correct
    ending. Prints ending, description of ending, and score.

    Preconditions
        - All imported objects have valid instance attributes
        - e_game.current_location_id >= 91 or e_game.current_location_id < 0

    >>> ex_adventure_game = AdventureGame("game_data.json", 31)
    >>> ex_adventure_game.current_location_id = 100
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sub_player.energy = 50
    >>> sub_player.score = 100
    >>> ending(ex_adventure_game, sub_player)
    <BLANKLINE>
    Ending: Sadia's Favourite Student
    You got Sadia all of her favourite things! She nepo-babied you and now you are the youngest prof at UofT!
    Score: 110

    """
    e_player.score += e_player.energy // 5

    for e_item in e_player.inventory:
        e_player.score += e_player.inventory[e_item].target_points

    if e_game.current_location_id == DROPOUT_NUMBER:
        print("\nEnding: Stranded in Toronto")
        print(e_game.get_location().descriptions[1])
        print("Score:", e_player.score)

    elif e_game.current_location_id == SADIA_NUMBER:
        if e_player.score >= 100:
            print("\nEnding: Sadia's Favourite Student")
            print("You got Sadia all of her favourite things! She nepo-babied you and now you are the youngest",
                  "prof at UofT!")
            print("Score:", e_player.score)

        elif e_player.score < 100 and e_player.score > 0:
            print("\nEnding: Regular Shmegular Computer Science Student")
            print(e_game.get_location().descriptions[1])
            print("Score:", e_player.score)

        elif e_player.score < 0:
            print("\nEnding: You (Almost) Killed Your Prof")
            print("Didn't you know that your professor is allergic to eggs!?!? Bringing an egg sandwich to her",
                  "office? Great, you passed the course but at what cost, she's literally in the hospital!1!!!")
            print("Score:", e_player.score)

    elif e_game.current_location_id == FANFIC_NUMBER:
        print("\nEnding: Super Saiyann")
        print(e_game.get_location().descriptions[1])
        print("Score: Over 9000")

    elif e_game.current_location_id == SLEEPY_NUMBER:
        print("\nEnding: Math Major for Life")
        print(e_game.get_location().descriptions[1])
        print("Score:", e_player.score)


def pickup_event(p_game: AdventureGame, p_commands: dict[str: str], p_choice: str) -> None:
    """Deals with pickup actions within the game, adjusts the users current inventory and the items inside of
    a location.

    Preconditions
        - All imported objects have valid instance attributes
        - p_choice in p_commands
        - isinstance(p_commands[p_choice], Item)

    >>> ex_adventure_game = AdventureGame("game_data.json", 3)
    >>> ex_commands = {"pick up plan": "plan"}
    >>> sub_player = ex_adventure_game.current_player_state
    >>> pickup_event(ex_adventure_game, ex_commands, "pick up plan")
    You pick up your plan, perfect for reviewing!
    >>> "plan" in sub_player.inventory
    True
    """
    p_game.current_player_state.inventory[p_commands[p_choice]] = p_game.get_item(p_commands[p_choice])
    p_game.get_location().items.remove(p_commands[p_choice])
    print(p_game.get_item(p_commands[p_choice]).itemget_description)
    p_game.current_player_state.energy -= 1


def simulation_interaction_manager(s_game: AdventureGame, location: Location, s_player_state: Player,
                                   commands: list[str], index: int) -> int:
    """Deals with special interaction within locations. There are two types of interactions: s
    election interactions and dialogue interactions. Adjusts current player state (ie. wallet, energy, etc.)
    Returns integer representing current index within list of commands. FOR SIMULATION ONLY.

    Preconditions
        - All imported objects have valid instance attributes
        - index < len(command)

    >>> ex_adventure_game = AdventureGame("game_data.json", 22)
    >>> ex_actions = ["go west", "buy from vending machine", "buy welches", "go south"]
    >>> ex_location = ex_adventure_game.get_location()
    >>> ex_index = 1
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sub_player.inventory = {"toonie": ex_adventure_game.get_item("toonie")}
    >>> simulation_interaction_manager(ex_adventure_game, ex_location, sub_player, ex_actions, ex_index)
    2
    >>> "welches" in sub_player.inventory
    True
    """
    index += 1

    if commands[index] in location.interaction_info[1]:
        chosen_item = s_game.get_item(location.interaction_info[1][commands[index]])
        if isinstance(chosen_item.cost, int):  # checks if item costs money/item cost is an int
            if chosen_item.cost > s_player_state.wallet:  # checks if player does not have enough money
                s_player_state.energy += 1
                return index
            else:  # player has enough money/can recieve the item
                s_player_state.wallet -= chosen_item.cost
                s_player_state.score += PICKUP_CONSTANT
                s_player_state.inventory[chosen_item.name] = chosen_item
                return index

        else:  # checks if cost was a string (implying either no cost, or "toonie" cost)
            if chosen_item.cost == "":
                s_player_state.inventory[chosen_item.name] = chosen_item
                s_player_state.score += PICKUP_CONSTANT
                return index

            elif chosen_item.cost in s_player_state.inventory:
                s_player_state.inventory.pop(chosen_item.cost)
                s_player_state.inventory[chosen_item.name] = chosen_item
                s_player_state.score += PICKUP_CONSTANT
                return index

            return index

    else:  # dialogue interaction, no user selection
        return index


def simulation_inventory_actions(s_game: AdventureGame, location: Location, lst_command: list[str],
                                 index: int) -> tuple[bool, int]:
    """Deals with inventory actions along with adjusting player states depending on what the user does.
    Returns a tuple with a boolean containing whether the action counted as an event and an int representing the current
    index of the commands list. FOR SIMULATION ONLY.

    Preconditions
        - All imported objects have valid instance attributes
        - index < len(list_command)

    >>> ex_adventure_game = AdventureGame("game_data.json", 22)
    >>> ex_actions = ["inventory", "hotdog", "eat"]
    >>> ex_location = ex_adventure_game.get_location()
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sub_player.energy = 20
    >>> sub_player.inventory = {"hotdog": ex_adventure_game.get_item("hotdog")}
    >>> simulation_inventory_actions(ex_adventure_game, ex_location, ex_actions, 0)
    (False, 2)
    >>> sub_player.energy
    30
    """
    food_energy = 10
    index += 1

    if s_game.current_player_state.inventory == {}:
        return False, index
    else:
        item_obj = s_game.get_item(lst_command[index])
        index += 1
        action_choice = lst_command[index]

        if action_choice == "look":
            return False, index

        elif action_choice == "eat":
            s_game.current_player_state.energy += food_energy
            s_game.current_player_state.inventory.pop(item_obj.name)
            return False, index

        elif action_choice == "drop":
            s_game.get_location().items += [s_game.current_player_state.inventory.pop(item_obj.name).name]
            s_game.current_player_state.energy -= 1
            return True, index

        elif action_choice == "show" and location.id_num == 32:
            s_game.current_location_id = 92
            s_game.current_player_state.energy -= 1
            return True, index

        else:
            return False, index


def simulation_menu_function(m_game: AdventureGame, m_current_location: Location,
                             m_game_log: EventList, commands: list[str], index: int) -> tuple[bool, int]:
    """Deals with menu interactions with the user. Adjusts player_state, game_log, or the current_location depending
     on the action taken by the user. Returns a tuple of a boolean that confirms whether the action should be counted
     as an event and an int of the current index of commands. FOR SIMULATION ONLY.

    Preconditions:
        - commands[index] in ["look", "inventory", "score", "energy", "wallet", "undo", "log", "quit"]
        - index < len(list_command)
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 42)
    >>> ex_actions = ["go west", "go north", "go north", "inventory", "socks", "look", "energy"]
    >>> ex_location = ex_adventure_game.get_location()
    >>> ex_events = EventList()
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sub_player.inventory = {"socks": ex_adventure_game.get_item("socks")}
    >>> simulation_menu_function(ex_adventure_game, ex_location, ex_events, ex_actions, 3)
    (False, 5)
    >>> simulation_menu_function(ex_adventure_game, ex_location, ex_events, ex_actions, 6)
    (False, 6)
    """
    m_choice = commands[index]
    if m_choice == "look":
        return False, index

    elif m_choice == "inventory":
        info = simulation_inventory_actions(m_game, m_current_location, commands, index)
        count_as_event = info[0]
        new_index = info[1]
        return count_as_event, new_index

    elif m_choice == "score":
        return False, index

    elif m_choice == "energy":
        return False, index

    elif m_choice == "wallet":
        return False, index

    elif m_choice == "undo" and m_game_log.last != m_game_log.first:
        m_game_log.remove_last_event()
        m_game.current_location_id = m_game_log.last.id_num
        m_game.get_location().items = m_game_log.last.location_items
        m_game.current_player_state = m_game_log.last.player_state
        return False, index

    elif m_choice == "log":
        return False, index

    elif m_choice == "quit":
        m_game.current_location_id = -100
        return False, index

    return False, index


def sim_non_menu_function_int(game_value: Any, sub_game: AdventureGame, sub_current_location: Location,
                              lst_command: list[str], index: int) -> tuple[bool, int]:
    """Deals with non-menu actions where the call (game_value) is an integer. This will specifically deal with movement
    of locations, and defining what the location id is, along with updating energy. Returns a tuple with a boolean of
    whether this action should create an event, and an integer representing the current index in lst_command. FOR
    SIMULATION ONLY.

    Preconditions
        - All imported objects have valid instance attributes
        - index < len(list_command)

    >>> ex_adventure_game = AdventureGame("game_data.json", 41)
    >>> ex_actions = ["go west"]
    >>> ex_location = ex_adventure_game.get_location()
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sim_non_menu_function_int(4, ex_adventure_game, ex_location, ex_actions, 0)
    (True, 0)

    """
    if game_value == INTERACTION_NUMBER:  # special interaction
        new_index = simulation_interaction_manager(sub_game, sub_current_location, sub_game.current_player_state,
                                                   lst_command, index)
        sub_game.current_player_state.energy -= 1
        return True, new_index

    elif game_value < DROPOUT_NUMBER:  # regular movement
        sub_game.current_location_id = game_value
        sub_game.current_player_state.energy -= 1
        return True, index

    elif game_value == SADIA_NUMBER:
        if ("usb" in sub_game.current_player_state.inventory and "charger" in
                sub_game.current_player_state.inventory and "lucky mug" in sub_game.current_player_state.inventory):
            sub_game.current_location_id = game_value
            sub_game.current_player_state.energy -= 1
            return True, index
        else:
            return False, index

    elif game_value == DROPOUT_NUMBER:
        sub_game.current_location_id = game_value
        sub_game.current_player_state.energy -= 1
        return True, index

    return False, index


def sim_non_menu_function_str(game_value: Any, sub_game: AdventureGame, index: int) -> tuple[bool, int]:
    """Deals with non-menu actions that have a call (game_value) that is a string, specifically interactions and item
    pickups. Will update the current player state to reflect the new inventory, and also adjust the player's energy.
    Returns a tuple containing a boolean of whether this action should create an event and an integer representing
    the index of inside of the main commands list we are in (seen inside of 'proj1_simulation.py). FOR SIMULATION
    ONLY.

    Preconditions
        - sub_game.get_item(game_value).commands == {} or sub_game.get_item(game_value).name == "hotdog"
        - All imported objects have valid instance attributes

    >>> ex_adventure_game = AdventureGame("game_data.json", 2)
    >>> ex_location = ex_adventure_game.get_location()
    >>> sub_player = ex_adventure_game.current_player_state
    >>> sub_player.inventory = {"hotdog": ex_adventure_game.get_item("hotdog")}
    >>> sim_non_menu_function_str("hotdog", ex_adventure_game, 24)
    (False, 24)
    >>> ex_adventure_game.current_location_id = 23
    >>> sim_non_menu_function_str("sadia fact", ex_adventure_game, 25)
    (True, 25)
    """
    if sub_game.get_item(game_value).commands == {}:  # special dialogue
        sub_game.current_player_state.energy -= 1
        return True, index

    else:  # hotdog pick up
        new_item = sub_game.get_item(game_value)
        if new_item.cost > sub_game.current_player_state.wallet:
            return False, index
        elif new_item.name in sub_game.current_player_state.inventory:
            return False, index
        else:
            sub_game.current_player_state.inventory[game_value] = new_item
            sub_game.current_player_state.wallet -= new_item.cost
            sub_game.current_player_state.score += PICKUP_CONSTANT
            sub_game.current_player_state.energy -= 1
            return True, index


def simulation_pickup_event(p_game: AdventureGame, p_commands: dict[str: str], p_choice: str) -> None:
    """Deals with pickup actions within the game, adjusts the users current inventory and the items inside of
    a location. FOR SIMULATION ONLY.

    Preconditions
        - All imported objects have valid instance attributes
        - p_choice in p_commands
        - isinstance(p_commands[p_choice], Item)

    >>> ex_adventure_game = AdventureGame("game_data.json", 3)
    >>> ex_commands = {"pick up plan": "plan"}
    >>> sub_player = ex_adventure_game.current_player_state
    >>> simulation_pickup_event(ex_adventure_game, ex_commands, "pick up plan")
    >>> "plan" in sub_player.inventory
    True
    """
    p_game.current_player_state.inventory[p_commands[p_choice]] = p_game.get_item(p_commands[p_choice])
    p_game.get_location().items.remove(p_commands[p_choice])
    p_game.current_player_state.energy -= 1


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
