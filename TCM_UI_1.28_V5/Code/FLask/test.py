import os

folder_id = "111"
file_patterns = ["步态记录", "舌相抓取", "面部识别", "患者自述"]
base_path = r"C:\Users\Djctionary\Downloads"

max_files = {}

for root, dirs, files in os.walk(base_path):
    for file in files:
        for file_pattern in file_patterns:
            if file.startswith(f"{folder_id}_{file_pattern}") and file.endswith(".mp4"):
                current_key = (folder_id, file_pattern)
                current_file_path = os.path.join(root, file)

                if current_key not in max_files or os.path.getmtime(current_file_path) > os.path.getmtime(max_files[current_key]):
                    max_files[current_key] = current_file_path

if not max_files:
    print("未找到符合条件的文件")

for key, file_path in max_files.items():
    print(f"找到符合条件的文件路径: {file_path}")
