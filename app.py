import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from PIL import Image, ImageChops, ImageEnhance
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Load model
model = load_model("best_model.keras")


# ================================
# CHECK FILE TYPE
# ================================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================================
# ELA FUNCTION
# ================================
def ela_image(path):
    img = Image.open(path).convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, "JPEG", quality=90)
    buffer.seek(0)

    comp = Image.open(buffer)
    ela = ImageChops.difference(img, comp)

    extrema = ela.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1

    scale = 255.0 / max_diff
    ela = ImageEnhance.Brightness(ela).enhance(scale)
    ela = ela.resize((128,128))

    return np.array(ela) / 255.0


# ================================
# HOME PAGE
# ================================
@app.route("/")
def home():
    return render_template("home.html")


# ================================
# DETECT PAGE
# ================================
@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        file = request.files.get("file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            img = ela_image(filepath)
            img = np.expand_dims(img, axis=0)

            pred = model.predict(img)[0][0]

            # Threshold tuning
            if pred > 0.6:
                prediction = f"Tampered 🛑 ({pred*100:.2f}%)"
            else:
                prediction = f"Authentic ✅ ({(1-pred)*100:.2f}%)"

            return render_template(
                "result.html",
                prediction=prediction,
                img_path=filepath
            )

        else:
            return render_template(
                "result.html",
                prediction="Invalid file type! Upload JPG/PNG.",
                img_path=None
            )

    return render_template("detect.html")


# ================================
# ABOUT PAGE
# ================================
@app.route("/about")
def about():
    return render_template("about.html")


# ================================
# HOW IT WORKS PAGE
# ================================
@app.route("/how")
def how():
    return render_template("how.html")


# ================================
# RUN APP
# ================================
if __name__ == "__main__":
    app.run(debug=True)
