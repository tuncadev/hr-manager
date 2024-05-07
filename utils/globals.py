import os


def get_assistant_avatar(filename):
    avatar_path = f"media/avatars/{filename}"
    return avatar_path

def are_all_fields_filled(responses):
    for key, value in responses.items():
        if not value:
            return False
    return True

def check_and_delete_temp_files():
    temp_dir = "temp"
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        os.remove(file_path)
        print(f"Deleted file: {file_path}")