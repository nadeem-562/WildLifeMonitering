import folium

def mark_species_on_map(latitude, longitude, popup_text, add_circle=False):
    """
    Marks a location on a map and optionally adds a circle around it.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        popup_text (str): Text to display in the popup for the marker.
        add_circle (bool): If True, adds a circle around the marker.
    
    Returns:
        folium.Map: A map with the specified marker (and circle if enabled).
    """
    # Create a map centered at the provided coordinates
    species_map = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Add a marker to the map
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_text,
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(species_map)

    # Add a circle around the marker if specified
    if add_circle:
        folium.Circle(
            location=[latitude, longitude],
            radius=3000,  # Radius of the circle in meters
            color='blue',  # Circle border color
            fill=True,  # Enable filling the circle
            fill_color='blue',  # Fill color
            fill_opacity=0.4  # Opacity of the fill
        ).add_to(species_map)

    return species_map
