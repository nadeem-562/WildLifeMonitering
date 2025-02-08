from flask import Flask, request, render_template, send_from_directory, jsonify
from utils.detection import detect_and_mark
from utils.geotagging import get_geotags, convert_to_degrees
from utils.mapping import mark_species_on_map
import os
import cv2
from ultralytics import YOLO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs/marked_images'
MAP_FOLDER = 'outputs/maps'

# Configure application folders
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAP_FOLDER'] = MAP_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(MAP_FOLDER, exist_ok=True)

# Load the YOLO model
model = YOLO("models/best.pt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Process the image
    image = cv2.imread(filepath)
    marked_image, detections = detect_and_mark(image, model)  # Get the detections from YOLO
    geotags = get_geotags(filepath)

    if not geotags:
        return jsonify({'error': 'No geolocation data found'}), 400

    latitude = convert_to_degrees(geotags["GPSLatitude"])
    longitude = convert_to_degrees(geotags["GPSLongitude"])

    # Save marked image
    output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], file.filename)
    cv2.imwrite(output_image_path, marked_image)

    # Save map file with a circle around the location
    map_path = os.path.join(app.config['MAP_FOLDER'], f"{file.filename.split('.')[0]}_map.html")
    forest_map = mark_species_on_map(latitude, longitude, "Detected Location", add_circle=True)
    forest_map.save(map_path)
    map_url = f"/maps/{file.filename.split('.')[0]}_map.html"

    # Log for debugging
    print(f"Generated Map URL: {map_url}")

    # Return response with map URL
    return jsonify({
        'image_url': f"/marked_images/{file.filename}",
        'map_url': map_url  # Send the map URL for iframe
    })

@app.route('/marked_images/<filename>')
def serve_marked_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/maps/<filename>')
def serve_map(filename):
    return send_from_directory(app.config['MAP_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
