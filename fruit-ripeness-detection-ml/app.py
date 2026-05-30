from flask import Flask, render_template, request
import os
from predict import detect_all

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        ripeness, result_img = detect_all(filepath)

        return render_template('index.html',
                               prediction=ripeness,
                               image_path=result_img)

    return "Error"

if __name__ == "__main__":
    app.run(debug=True)