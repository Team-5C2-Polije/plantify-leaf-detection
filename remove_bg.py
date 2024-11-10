import os
from rembg import remove
from PIL import Image
import io

input_folder = r"C:\dev\python\tomato-leaf-sistem\raw_image\train\sehat"
output_folder = r"C:\dev\python\tomato-leaf-sistem\testgbar\sehat"

os.makedirs(output_folder, exist_ok=True)  # Buat folder output jika belum ada

for filename in os.listdir(input_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Hapus latar belakang menggunakan rembg
        with open(input_path, "rb") as input_file:
            input_image = input_file.read()
            output_image = remove(input_image)
        
        # Buka gambar hasil tanpa latar belakang
        with Image.open(io.BytesIO(output_image)).convert("RGBA") as img:
            # Tambahkan latar putih
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))  # Warna putih
            white_background = Image.alpha_composite(background, img).convert("RGB")
            
            # Simpan gambar dengan latar putih
            white_background.save(output_path)

        print(f"Processed: {input_path} -> {output_path}")

print("Proses selesai. Gambar disimpan di folder:", output_folder)
