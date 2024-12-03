from location import Location
from game_object import GameObject
from board import Board

class Grasshopper(GameObject):
    def __init__(self, location, color):

        super().__init__(location, color)  # Call the parent class constructor

        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        
        self._location = location

    def __repr__(self):
        return f"Grasshopper at {self.get_location()}"
    
    def get_next_possible_locations(self, board: Board):
        newLocations = []

        loc = self.get_location()
        x = loc.get_x()
        y = loc.get_y()
        
        #if there is an element above and right
        if (board.get_object(Location(x+1, y+1)) is not None):
            new_x = x
            new_y = y
            while (board.get_object(Location(x+1, y+1)) is not None):
                new_x += 1
                new_y += 1
            newLocations.append(Location(new_x,new_y))
            

        #if there is an element above and left
        if (board.get_object(Location(x-1, y+1)) is not None):
            new_x = x
            new_y = y
            while (board.get_object(Location(x-1, y+1)) is not None):
                new_x -= 1
                new_y += 1
            newLocations.append(Location(new_x,new_y))

        #if there is an element bottom and right
        if (board.get_object(Location(x+1, y-1)) is not None):
            new_x = x
            new_y = y
            while (board.get_object(Location(x+1, y-1)) is not None):
                new_x += 1
                new_y -= 1
            newLocations.append(Location(new_x, new_y))

        #if there is an element bottom and left
        if (board.get_object(Location(x-1, y-1)) is not None):
            new_x = x
            new_y = y
            while (board.get_object(Location(x-1, y-1)) is not None):
                new_x -= 1
                new_y -= 1
            newLocations.append(Location(new_x, new_y))

        #if there is an element to the right
        if (board.get_object(Location(x+2, y)) is not None):
            new_x = x + 2
            new_y = y
            while (board.get_object(Location(x-1, y-1)) is not None):
                new_x += 2
            newLocations.append(Location(new_x, new_y))

        #if there is an element to the left
        if (board.get_object(Location(x-2, y)) is not None):
            new_x = x - 2
            new_y = y
            while (board.get_object(Location(x-1, y-1)) is not None):
                new_x -= 2
            newLocations.append(Location(new_x, new_y))

        return newLocations
