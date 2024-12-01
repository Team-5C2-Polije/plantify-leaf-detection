import os
import io
from rembg import remove
from PIL import Image, ImageEnhance

def process_image(input_path, output_path, filename):
    # Buka gambar dari file path
    with Image.open(input_path).convert("RGB") as img:
        # Resize gambar ke 512x512
        resized_image = img.resize((512, 512))
        
        # Gabungkan output folder dengan nama file
        output_file_path = os.path.join(output_path, filename)

        # Pastikan folder tujuan ada sebelum menyimpan file
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Simpan gambar yang sudah di-resize
        resized_image.save(output_file_path)
        
    print(f"Processed: {input_path} -> {output_file_path}")

# def process_image(input_path, output_path, filename):
#     with open(input_path, "rb") as input_file:
#         input_image = input_file.read()
#         output_image = remove(input_image)  # Remove background

#     # Remove background dan konversi gambar
#     with Image.open(io.BytesIO(output_image)).convert("RGBA") as img:
#         # Ubah background menjadi putih
#         background = Image.new("RGBA", img.size, (255, 255, 255, 255))
#         white_background = Image.alpha_composite(background, img).convert("RGB")
        
#         # Resize gambar ke 512x512
#         resized_image = white_background.resize((512, 512))
        
#         # Gabungkan output folder dengan nama file
#         output_file_path = os.path.join(output_path, filename)  # Correct the file path

#         # Pastikan folder tujuan ada sebelum menyimpan file
#         os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

#         resized_image.save(output_file_path)  # Save the resized image
        
#     print(f"Processed: {input_path} -> {output_file_path}")

# Metode untuk memproses semua gambar dalam folder
def process_folder(input_folder, output_folder):
    # Membuat folder output jika belum ada
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_folder, filename)
            process_image(input_path, output_folder, filename)  # Proses gambar

# Folder input dan output
input_folder_train_sehat = r"C:\dev\python\tomato-leaf-sistem\dataset_raw_old\train\sehat"
input_folder_train_sakit = r"C:\dev\python\tomato-leaf-sistem\dataset_raw_old\train\sakit"
input_folder_test_sehat =  r"C:\dev\python\tomato-leaf-sistem\dataset_raw_old\test\sehat"
input_folder_test_sakit =  r"C:\dev\python\tomato-leaf-sistem\dataset_raw_old\test\sakit"

output_folder_train_sehat = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\train\sehat"
output_folder_train_sakit = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\train\sakit"
output_folder_test_sehat  = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\test\sehat"
output_folder_test_sakit  = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\test\sakit"

# Proses keempat folder
# process_folder(input_folder_train_sehat, output_folder_train_sehat)
# process_folder(input_folder_train_sakit, output_folder_train_sakit)
# process_folder(input_folder_test_sehat, output_folder_test_sehat)
# process_folder(input_folder_test_sakit, output_folder_test_sakit)

print("Proses selesai untuk semua folder.")
