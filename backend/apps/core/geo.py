"""Geolocation utilities — used to enforce the 10 KM delivery radius on the
backend (the authoritative check; the frontend check is a UX convenience
only and must never be trusted on its own)."""

import math

EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres between two lat/lon points."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def is_within_delivery_radius(
    lat: float,
    lon: float,
    restaurant_lat: float,
    restaurant_lon: float,
    radius_km: float,
) -> tuple[bool, float]:
    """Returns (is_within_radius, distance_km) for the given delivery coordinates."""
    distance = haversine_distance_km(restaurant_lat, restaurant_lon, lat, lon)
    return distance <= radius_km, round(distance, 2)
