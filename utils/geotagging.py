from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_geotags(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        return None

    gps_data = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for gps_tag, gps_value in value.items():
                gps_name = GPSTAGS.get(gps_tag, gps_tag)
                gps_data[gps_name] = gps_value
    return gps_data

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)
