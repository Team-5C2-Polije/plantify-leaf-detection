import joblib
import numpy as np
import cv2
import mahotas as mt
import pandas as pd

# Fungsi untuk ekstraksi fitur warna dan tekstur
def extract_features(image_path):
    try:
        # Baca gambar
        img = cv2.imread(image_path)

        # Ekstraksi fitur warna (R, G, B)
        avg_color_per_row = cv2.mean(img)[:3]  # Mendapatkan nilai rata-rata RGB
        R, G, B = avg_color_per_row

        # Konversi gambar ke grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Ekstraksi fitur tekstur (GLCM)
        glcm = mt.features.haralick(img_gray).mean(axis=0)
        contrast = glcm[1]
        homogeneity = glcm[4]
        energy = glcm[8]
        correlation = glcm[2]

        # Gabungkan semua fitur
        return np.hstack([R, G, B, contrast, homogeneity, energy, correlation])
    except Exception as e:
        print(f"Gagal mengekstraksi fitur dari gambar {image_path}: {e}")
        return None

# Fungsi untuk memuat model dan melakukan prediksi
def predict_image(image_path, model_path="random_forest_tomato_model.pkl"):
    # Load model yang telah dilatih
    model = joblib.load(model_path)
    print(f"Model berhasil dimuat dari {model_path}")

    # Ekstraksi fitur dari gambar
    features = extract_features(image_path)
    if features is None:
        print("Gagal mengekstraksi fitur. Pastikan gambar valid.")
        return

    # Reshape fitur untuk prediksi (1 sampel)
    features = features.reshape(1, -1)

    # Prediksi
    prediction = model.predict(features)
    print(f"Hasil prediksi untuk gambar {image_path}: {'Sehat' if prediction[0] == 1 else 'Sakit'}")

if __name__ == "__main__":
    # Path gambar daun tomat yang akan diuji
    image_path = r"C:\dev\python\tomato-leaf-sistem\dataset\test\sehat\tomato-test-sehat-03.jpg"
    model_path = r"models\random_forest_2.pkl"
    predict_image(image_path, model_path)
