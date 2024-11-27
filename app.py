from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw, ImageFont
import os
from image_proc import process_image
from predict import predict_single_image
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="PIL")

# Inisialisasi klien API Roboflow
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="MIebZflR9bJdmpmXovTj"
)

# Input gambar
image_input = r"raw_image\test\test4.png"
image = Image.open(image_input)
result = result = CLIENT.infer(image_input, model_id="tomato-leaf-disease-rxcft/3?confidence=0.20")

print("Prediction result:", result)

# Folder output
output_folder = "crops"
os.makedirs(output_folder, exist_ok=True)

# Salin gambar input untuk ditambahkan bounding box
annotated_image = image.copy()  # Salin gambar input
draw = ImageDraw.Draw(annotated_image)

# Tentukan font untuk label
font_path = "poppins_bold.ttf"  # Pastikan font tersedia di sistem Anda, gunakan font lain jika tidak ada
try:
    font = ImageFont.truetype(font_path, size=20)  # Ukuran font diperbesar (20 px)
except IOError:
    print(f"Font '{font_path}' tidak ditemukan, menggunakan default font.")
    font = ImageFont.load_default()

# Iterasi setiap prediksi untuk menggambar bounding box dan label
for idx, prediction in enumerate(result["predictions"]):
    x = prediction["x"]
    y = prediction["y"]
    width = prediction["width"]
    height = prediction["height"]
    
    # leaf position
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2

    # croped image by leaf pos
    cropped_image = image.crop((left, top, right, bottom))
    filename = f"crop_{idx + 1:02d}.png"
    crop_output_path = os.path.join(output_folder, filename)
    cropped_image.save(crop_output_path)

    # preprocessing and predict
    print('preprocessing image : ' + crop_output_path)
    process_image(crop_output_path, r'crop_procs', filename)
    label = predict_single_image(crop_output_path, r"models\test\decision_tree_3.pkl")

    # add bounding box
    color_list = ["red", "blue", "purple", "navy", "magenta"]
    color = random.choice(color_list)
    draw.rectangle([(left, top), (right, bottom)], outline=color, width=3)
    label_position = (left, top - 25)
    draw.text(label_position, label, fill=color, font=font)

# save image with bounding box
annotated_output_path = "predict_result.png"
annotated_image.save(annotated_output_path)

print(f"Annotated image with bounding boxes and labels saved at: {annotated_output_path}")
