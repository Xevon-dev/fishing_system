"""View-функції каталогу, розкладені за темами.

`catalog/urls.py` імпортує цей пакет як `views`, тож назви функцій
мають залишатися незмінними.
"""

from .fish_advice import fish_advice_view
from .forecast import advice_view, weather_view
from .home import home
from .methods import methods_view
from .tackle import tackle_view
from .water_bodies import (
    water_bodies_geojson,
    water_bodies_view,
    water_body_geojson,
)

__all__ = [
    "home",
    "water_bodies_view",
    "water_bodies_geojson",
    "water_body_geojson",
    "fish_advice_view",
    "methods_view",
    "tackle_view",
    "weather_view",
    "advice_view",
]
