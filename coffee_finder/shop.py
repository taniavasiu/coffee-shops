from dataclasses import dataclass

@dataclass(frozen=True)
class Shop:
    """A coffee shop with a name and (x, y) coordinates on a plane."""
    name: str
    x: float
    y: float

    def distance_to(self, x: float, y: float) -> float:
        """Euclidean distance from this shop to the given point.
        """
        # sqrt((x2-x1)^2 + (y2-y1)^2) — using **0.5 instead of math.sqrt
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
