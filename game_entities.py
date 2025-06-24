"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - self.id_num: the id corresponding to this instance of Location
        - self.name: string containing name of location
        - self.descriptions: tuple containing brief and long descriptions of location
        - self.available_commands: a dictionary containing commands along with the corresponding new location or item
                                   for that command
        - self.interaction_info: tuple containing interaction dialogue and possible interaction commands
        - self.items: list of items that are found at current location
        - self.visited: boolean of whether location has been visited at an earlier time by player

    Representation Invariants:
        - -5 <= self.id_num <= 100
        - self.interaction != "" or self.interaction_commands == {}
        - [isinstance(item, str) for item in self.available_commands]
        - [isinstance(item, str) for item in self.interaction_commands]
    """
    id_num: int
    name: str
    descriptions: tuple[str, str]
    available_commands: dict[str: int | str]
    interaction_info: tuple[str, dict[str: int | str]]
    items: list[str]
    visited: bool

    def __init__(self, compounded: list) -> None:
        """Initialize a new location. Auto-set visited to False. Interaction corresponds to whether there is an
        interaction at this location, and contains a string with dialogue. Similarly, interaction_commands
        contains a dictionary with actions that can be taken for each interaction.

        Note that the two description will be stored in one description tuple, where descriptions[0] is the brief
        and descriptions[1] is the long.

        Also note that similarly, the interaction info will be stored in one tuple, where the interaction itself
        is interaction_info[0] and the interaction commands are interaction_info[1].

        Preconditions:
            - compounded == [location_id, name, brief_description, long_description, avalaible_commands, interaction,
                             interaction_commands, items]
            - self.descriptions == [brief_description, long_description]
            - self.interaction_info == [interaction, interaction_commands]
        """

        self.id_num = compounded[0]
        self.name = compounded[1]
        self.descriptions = compounded[2], compounded[3]
        self.available_commands = compounded[4]
        self.interaction_info = compounded[5], compounded[6]
        self.items = compounded[7]
        self.visited = False


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name associated with instance of Item
        - cost: int representing required amount of money or string representing required item to get item
        - itemget_description: string containing description for when item is first gotten
        - commands: dictionary mapping commands with outcomes for each item
        - start_position: int or "" representing where the item is first picked up
        - target_points: int or "" representing points given when item is brought to end location

    Representation Invariants:
        - isinstance(self.cost, (int, str))
        - isinstance(self.start_position, (int, str))
        - isinstance(self.target_points, (int, str))
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    cost: Any
    itemget_description: str
    commands: dict
    start_position: Any
    target_points: Any


@dataclass
class Player:
    """
    A capture of the Player at a specific state of the game.

    Instance Attributes:
        - inventory: dictionary mapping name of item to the Item object
        - energy: int representing the energy of the player
        - score: int representing score of the player
        - wallet: int representing wallet of the player
    """
    inventory: dict[str: Item]
    energy: int
    score: int
    wallet: int


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
