from abc import ABC
from homework_02.exceptions import LowFuelError, CargoOverload, NotEnoughFuel
class Vehicle(ABC):

    def __init__(self, weight=10, fuel=5, fuel_consumption=4):
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption
        self.started = False

    def start(self, started=False):
        if not started and (self.fuel > 0):
            self.started = True
        else:
            raise LowFuelError

    def move(self, dist):
        if self.fuel < self.fuel_consumption * dist:
            raise NotEnoughFuel
        self.fuel = self.fuel - self.fuel_consumption * dist


