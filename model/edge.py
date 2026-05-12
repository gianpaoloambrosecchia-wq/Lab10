from dataclasses import dataclass

from model.country import Country


@dataclass
class Edge:
    country1: Country
    country2: Country

    def __hash__(self):
        return hash((self.country1, self.country2))

    def __eq__(self, other):
        return self.country1 == other.country1 and self.country2 == other.country2


