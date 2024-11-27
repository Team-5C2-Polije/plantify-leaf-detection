import os
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
        return [R, G, B, contrast, homogeneity, energy, correlation]
    except Exception as e:
        print(f"Gagal memproses {image_path}: {e}")
        return None

# Fungsi untuk memuat model dan melakukan prediksi pada satu gambar
def predict_image(image_path, model):
    # Ekstraksi fitur dari gambar
    features = extract_features(image_path)
    if features is None:
        print(f"Gagal mengekstraksi fitur dari gambar {image_path}.")
        return None

    # Daftar nama fitur sesuai pelatihan
    feature_names = ["R", "G", "B", "Kontras", "Homogenitas", "Energi", "Korelasi"]

    # Buat DataFrame dengan nama fitur
    features_df = pd.DataFrame([features], columns=feature_names)

    # Prediksi
    prediction = model.predict(features_df)
    return prediction[0]

# Fungsi untuk membaca semua gambar dalam folder dan memprediksi
def predict_folder(image_folder, model_path):
    # Load model
    model = joblib.load(model_path)
    print(f"Model berhasil dimuat dari {model_path}")

    # Baca semua gambar dalam folder
    results = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_folder, filename)
            result = predict_image(image_path, model)
            if result is not None:
                status = "Sehat" if result == 1 else "Sakit"
                results.append((filename, status))

    # Output hasil
    print("\nHasil prediksi untuk semua gambar dalam folder:")
    for filename, status in results:
        print(f"{filename}: {status}")

def predict_single_image(image_file, model_path):
    # Load model
    model = joblib.load(model_path)
    print(f"Model berhasil dimuat dari {model_path}")

    # Prediksi
    result = predict_image(image_file, model)
    if result is not None:
        label = "Sehat" if result == 1 else "Sakit"
        return label
    else:
        return "Error dalam prediksi"

if __name__ == "__main__":
    # Path model dan folder gambar
    model_path = r"models\test\decision_tree_4.pkl"
    image_folder = r"dataset_test_7\test\sakit"
    predict_folder(image_folder, model_path)
