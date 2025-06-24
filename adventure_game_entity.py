"""CSC111 Project 1: Text Adventure Game Entity - Class AdventureGame

===============================

This Python module contains the class 'AdventureGame' which is called by both 'adventure.py' and
'proj1_simulation.py'.

===============================
"""

from __future__ import annotations
import json
from typing import Optional
from game_entities import Location, Item, Player


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_player_state: Player object that stores the current state of the player
        - current_location_id: an int corresponding to the current location
        - ongoing: boolean that signifies whether the game is ongoing or not

    Representation Invariants:
        - -5 <= self.current_location_id <= 100
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_player_state: Player
    current_location_id: int
    ongoing: bool

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        starting_money = 15
        energy = 45
        initial_score = 0

        self._locations, self._items = self._load_game_data(game_data_file)
        self.current_player_state = Player({}, energy, initial_score, starting_money)
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], dict[str, Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects.

        Preconditions:
        - filename is the filename of a valid game data JSON file
        """

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location([loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['interaction'],
                                    loc_data['interaction_commands'], loc_data['items']])
            locations[loc_data['id']] = location_obj

        items = {}
        for item_data in data['items']:  # Go through each element associated with the 'locations' key in the file
            item_obj = Item(item_data['name'], item_data['cost'], item_data['itemget_description'],
                            item_data['commands'], item_data['start_position'],
                            item_data['target_points'])
            items[item_data['name']] = item_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.

        Preconditions:
        - loc_id in self._items
        """
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item:
        """Return Item object associated with provided item name.

        Preconditions:
        - item_name in self._items
        """
        return self._items[item_name]


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
