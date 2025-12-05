from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("sign_language_model_final.h5")

# Load class mapping
with open("class_mapping.json", "r") as f:
    class_names = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img_bytes = file.read()

    # Process image
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))  # Change if your model uses another size
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    preds = model.predict(img)
    idx = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))

    return jsonify({
        "class": class_names[str(idx)],
        "confidence": round(confidence, 3)
    })

if __name__ == "__main__":
    app.run(debug=True)
