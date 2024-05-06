
def get_assistant_avatar(filename):
    avatar_path = f"media/avatars/{filename}"
    return avatar_path

def are_all_fields_filled(responses):
    for key, value in responses.items():
        if not value:
            return False
    return True