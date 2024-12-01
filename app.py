from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw, ImageFont
import os
from image_proc import process_image
from predict import predict_single_image
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="PIL")

# membuat folder output
output_folder = "crops"
os.makedirs(output_folder, exist_ok=True)
output_folder_procs = "crops_procs"
os.makedirs(output_folder_procs, exist_ok=True)

# setting font untuk bounding box
font_path = "poppins_bold.ttf"
try:
    font = ImageFont.truetype(font_path, size=20)
except IOError:
    print(f"Font '{font_path}' tidak ditemukan, menggunakan default font.")
    font = ImageFont.load_default()

# list color bounding box
color_list = ["red", "blue", "purple", "navy", "magenta"]

# input gambar
image_input = r"C:\dev\python\tomato-leaf-sistem\dataset_test_7\train\sakit\tomato-train-sakit-01.jpg"
image = Image.open(image_input)

# copy gambar untuk membuat bounding box
annotated_image = image.copy()
draw = ImageDraw.Draw(annotated_image)

# memanggil api yolov7
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="MIebZflR9bJdmpmXovTj"
)
result = result = CLIENT.infer(image_input, model_id="tomato-leaf-disease-rxcft/3?confidence=0.20")

print("PAYLOAD : ", result)

# membaca data predictions dibagian lokasi daun
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
    process_image(crop_output_path, output_folder_procs, filename)
    label = predict_single_image(crop_output_path, r"models\test\decision_tree_7.pkl")

    # add bounding box
    color = random.choice(color_list)
    draw.rectangle([(left, top), (right, bottom)], outline=color, width=3)
    label_position = (left, top - 25)
    draw.text(label_position, label, fill=color, font=font)

# save image with bounding box
annotated_output_path = "predict_result.png"
annotated_image.save(annotated_output_path)

print(f"Annotated image with bounding boxes and labels saved at: {annotated_output_path}")
