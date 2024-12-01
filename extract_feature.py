import os
import numpy as np
import pandas as pd
import cv2
import mahotas as mt

# Fungsi untuk ekstraksi fitur warna dan tekstur
def extract_features(image_path):
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

# Fungsi untuk memproses semua gambar dalam folder
def process_dataset(dataset_folder):
    features = []
    labels = []

    label_mapping = {"sehat": 1, "sakit": 0}  # Peta label ke nama

    for category in os.listdir(dataset_folder):
        category_path = os.path.join(dataset_folder, category)  # Path ke subfolder kategori
        
        # Pastikan category_path adalah direktori
        if not os.path.isdir(category_path):
            continue

        print(f"Memproses kategori: {category}")  # Logging kategori

        # Iterasi file dalam subfolder
        for filename in os.listdir(category_path):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(category_path, filename)
                print(f"Memproses file: {file_path}")  # Logging file

                # Ekstraksi fitur
                feature = extract_features(file_path)
                if feature is not None:
                    features.append(feature + [label_mapping[category]])  # Tambahkan label di akhir
                else:
                    print(f"Gagal mengekstraksi fitur dari: {file_path}")

    return np.array(features)

# Path ke folder dataset
dataset_folder = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\train"

# Proses dataset
features = process_dataset(dataset_folder)

# Konversi ke DataFrame untuk disimpan ke Excel
columns = ['R', 'G', 'B', 'Kontras', 'Homogenitas', 'Energi', 'Korelasi', 'Label']
df = pd.DataFrame(features, columns=columns)

# Simpan ke file Excel
output_file = "extractions\extr_ftr_test_7_name.xlsx"
df.to_excel(output_file, index=False)
print(f"Data fitur disimpan ke {output_file}")
