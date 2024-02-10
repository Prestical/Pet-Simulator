from typing import Type

# Check the value types
def enforce_type(type_: Type, value):
    if not isinstance(value, type_):
        raise TypeError(f"Expected {type_.__name__}, got {type(value).__name__}")

class character:
    def __init__(self, name: str, hunger: float, status: str, coin: float):
        enforce_type(str, name)
        enforce_type(float, hunger)
        enforce_type(str, status)
        enforce_type(float, coin)

        self.name = name
        self.hunger = hunger
        self.status = status
        self.coin = coin

    def __str__(self):
        return f"Name: {self.name}, Hunger: {self.hunger}/100.0, Status: {self.status}"
    
    # ASCII art part
    def checkImage(self):
        cases = {
            "Happy":"""
                     /^^^^^^\\
                    | -    - |
                    |  \__/  |
                     \______/ """,
            "Sad": """
                     /^^^^^^\\
                    | -    - |
                    |  /˜˜\  |
                     \______/ """,
            "Dead": """
                     /^^^^^^\\
                    | X    X |
                    |  ----  |
                     \______/ """,
            "Default":"""
                     /^^^^^^\\
                    | -    - |
                    |   --   |
                     \______/ """ 
        }
        return cases.get(self.status)
