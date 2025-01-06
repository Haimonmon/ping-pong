import time
import threading

from typing import Callable, Dict, List


class Observer:
    def __init__(self):
        pass

class Scoreboard(Observer):
    def __init__(self):
        self.score = 0


class Timer(Observer):
    def __init__(self):
        self.time = 0


class Gametype:
    """
    The Ping pong's logic or rules for each rounds 🔮
    """
    def __init__(self, playground, gametype: str):
        self.playground = playground
        self.gametype = self.select_gametype(gametype)

        # self.threading = None

        self.observers = []
        self.gametype.tell()




    def add_observer(self) -> None:
        pass

    
    def winning_condition(self) -> None:
        pass


class Rush:
    """
    Until times runout whoever score highest wins ⬆️
    """
    def __init__(self, playground: Callable):
        self.playground = playground

        self.platform: Callable = self.playground.kit["platform"]
        self.wall: Callable = self.playground.kit["wall"]
        self.paddles: List = self.playground.kit["paddles"]
        self.balls: List = self.playground.kit["balls"]

        self.time_limit = None
        self.powerups = None
        self.max_healths = None
       

    def tell(self) -> None:
        print(f'Gametype: {self.__class__.__name__}')
        print(self.platform.__class__.__name__)
        print(self.wall.__class__.__name__)
        print(self.paddles)
        print(self.balls)


    def winning_condition(self) -> None:
        pass


    def apply(self) -> None:
        pass


class Survival:
    """
    It takes healths to take you down 💖
    """
    def __init__(self, playground: Callable):
        self.playground = playground

        self.platform: Callable = self.playground.kit["platform"]
        self.wall: Callable = self.playground.kit["wall"]
        self.paddles: List = self.playground.kit["paddles"]
        self.balls: List = self.playground.kit["balls"]


    def tell(self) -> None:
        print(f'Gametype: {self.__class__.__name__}')
        print(self.platform.__class__.__name__)
        print(self.wall.__class__.__name__)
        print(self.paddles)
        print(self.balls)


    def winning_condition(self) -> None:
        pass


    def apply(self) -> None:
        pass


class DualBall:
    """
    How about 2 ball prioreties or even multiple for a round 🏓
    """

    def __init__(self, playground: Callable):
        self.playground = playground

        self.platform: Callable = self.playground.kit["platform"]
        self.wall: Callable = self.playground.kit["wall"]
        self.paddles: List = self.playground.kit["paddles"]
        self.balls: List = self.playground.kit["balls"]


    def tell(self) -> None:
        print(f'Gametype: {self.__class__.__name__}')
        print(self.platform.__class__.__name__)
        print(self.wall.__class__.__name__)
        print(self.paddles)
        print(self.balls)


    def winning_condition(self) -> None:
        pass


    def apply(self) -> None:
        pass


if __name__ == "__main__":
      game = Gametype("dual_ball")

      # TODO:
      # ! Planning to apply Observer design pattern for this