from flask import Flask, render_template, request
import os
import cv2
from src.detect_rotten import detect_rotten_area
from src.detect_ripeness import detect_ripeness

# folders
UPLOAD_FOLDER = "static/uploads/"
RESULT_FOLDER = "static/results/"

# app config
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# home route
@app.route('/')
def home():
    return render_template('index.html')

# prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file uploaded"

    file = request.files['image']

    if file.filename == '':
        return "No selected file"

    # save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ripeness detection
    ripeness = detect_ripeness(filepath)

    # rotten detection (draw box)
    result_path = os.path.join(RESULT_FOLDER, file.filename)
    detect_rotten_area(filepath, result_path)

    return render_template('index.html',
                           prediction=ripeness,
                           image_path=result_path)

# run app
if __name__ == "__main__":
    app.run(debug=True)