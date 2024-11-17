import os
from rembg import remove
from PIL import Image
import io

input_folder = r"C:\dev\python\tomato-leaf-sistem\dataset\test\sakit"
output_folder = r"C:\dev\python\tomato-leaf-sistem\dataset\test\sakit"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        with open(input_path, "rb") as input_file:
            input_image = input_file.read()
            output_image = remove(input_image)
        
        with Image.open(io.BytesIO(output_image)).convert("RGBA") as img:
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            white_background = Image.alpha_composite(background, img).convert("RGB")
            
            white_background.save(output_path)

        print(f"Processed: {input_path} -> {output_path}")

print("Proses selesai. Gambar disimpan di folder:", output_folder)
