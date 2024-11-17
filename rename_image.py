import os

def rename_files(folder_path, dataset, category):
    files = os.listdir(folder_path)
    files = [f for f in files if f.endswith((".jpg", ".jpeg", ".png"))] 

    for idx, filename in enumerate(files, start=1):
        new_name = f"tomato-{dataset}-{category}-{idx:02d}.jpg"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # Rename file
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")

base_folder = r"C:\dev\python\tomato-leaf-sistem\dataset\test"

# Rename file dalam folder "sehat"
rename_files(os.path.join(base_folder, "sehat"), "test", "sehat")

# Rename file dalam folder "sakit"
rename_files(os.path.join(base_folder, "sakit"), "test", "sakit")
