# Image Tampering Detection using ELA & CNN

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

An AI-powered digital forensics tool designed to expose image manipulations—such as splicing and copy-move forgeries—using **Error Level Analysis (ELA)** and a trained **Convolutional Neural Network (CNN)**.

## 🚀 Overview
Digital images are easily manipulated but difficult to verify with the naked eye. This project bridges that gap by analyzing compression artifacts. When an image is modified and resaved, the tampered regions exhibit different error levels compared to the original areas. Our system detects these inconsistencies with **93.36% accuracy**.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Deep Learning:** TensorFlow / Keras
- **Image Processing:** PIL (Pillow), NumPy
- **Frontend:** HTML5, **Tailwind CSS** (Custom Neon-Forensic UI)
- **Dataset:** CASIA 2.0

## 🧪 How It Works
1. **ELA Preprocessing:** The uploaded image is re-compressed at 90% quality. The pixel-wise difference between the original and re-compressed version is calculated to highlight compression inconsistencies.
2. **CNN Inference:** The 128x128 ELA map is fed into a 3-block CNN.
3. **Forensic Report:** The system outputs a classification (Authentic/Tampered) and a confidence percentage via a responsive Tailwind dashboard.
