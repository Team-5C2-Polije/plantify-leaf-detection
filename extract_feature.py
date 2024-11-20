import os
import numpy as np
import pandas as pd
import cv2
import mahotas as mt

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

def list_files_in_folder(folder_path):
    print(f"Listing files in folder: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(f"File: {os.path.join(root, file)}")

# Fungsi untuk memproses semua gambar dalam folder
def process_dataset(dataset_folder):
    features = []
    labels = []
    filenames = []  # Tambahkan list untuk menyimpan nama file
    label_names = []  # Tambahkan list untuk menyimpan label name
    list_files_in_folder(dataset_folder)
    
    label_mapping = {0: "Sakit", 1: "Sehat"}  # Peta label ke nama

    for label, category in enumerate(os.listdir(dataset_folder)):
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
                    print(f"Fitur berhasil diekstraksi untuk: {file_path}")
                    features.append(feature + [label])  # Tambahkan label di akhir
                    filenames.append(filename)  # Simpan hanya nama file
                    label_names.append(label_mapping[label])  # Simpan nama label
                else:
                    print(f"Gagal mengekstraksi fitur dari: {file_path}")

    return np.array(features), filenames, label_names

# Path ke folder dataset
dataset_folder = r"C:\dev\python\tomato-leaf-sistem\dataset\train"  # Ganti dengan path dataset Anda

# Proses dataset
features, filenames, label_names = process_dataset(dataset_folder)

# Konversi ke DataFrame untuk disimpan ke Excel
columns = ['R', 'G', 'B', 'Kontras', 'Homogenitas', 'Energi', 'Korelasi', 'Label']
df = pd.DataFrame(features, columns=columns)
df['LabelName'] = label_names  # Tambahkan kolom nama label
df['Nama File'] = filenames  # Tambahkan kolom nama file

# Simpan ke file Excel
output_file = "extractions\extracted_features_2_name.xlsx"
df.to_excel(output_file, index=False)
print(f"Data fitur disimpan ke {output_file}")
