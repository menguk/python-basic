"""
создайте класс `Plane`, наследник `Vehicle`
"""
from homework_02.base import Vehicle
from homework_02.exceptions import LowFuelError, CargoOverload, NotEnoughFuel


class Plane(Vehicle):
    def __init__(self, weight, fuel, fuel_consumption, max_cargo=10):
        super().__init__(weight, fuel, fuel_consumption)
        self.cargo = 0
        self.max_cargo = max_cargo

    def load_cargo(self, number):
        if (number + self.cargo) > self.max_cargo:
            raise CargoOverload
        self.cargo = self.cargo + number
        return self.cargo

    def remove_all_cargo(self):
        previos = self.cargo
        self.cargo = 0
        return previos


