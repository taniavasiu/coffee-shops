from typing import Iterable, List, Tuple

from .shop import Shop


def closest_shops(
    shops: Iterable[Shop], user_x: float, user_y: float, limit: int = 3
) -> List[Tuple[Shop, float]]:
    """Return the `limit` shops closest to the user, sorted ascending by distance.
    """
    
    with_distance = [(s, s.distance_to(user_x, user_y)) for s in shops]
    with_distance.sort(key=lambda pair: pair[1])

    return with_distance[:limit]
