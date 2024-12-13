class Observer:
    def __init__(self):
        pass

class Scoreboard(Observer):
    def __init__(self):
        self.score = 0


class Timer(Observer):
    def __init__(self):
        self.time = 0

class Game:
    """
    The Ping pong's logic or rules for each rounds 🔮
    """
    def __init__(self):
        self.playground = None
        self.observers = []

    def scoring(self) -> None:
        pass

    def timer(self) -> None:
        pass

    def num_players(self) -> None:
        pass

    def map(self) -> None:
        pass

if __name__ == "__main__":
      game = Game()

      # TODO:
      # ! Planning to apply Observer design pattern for this