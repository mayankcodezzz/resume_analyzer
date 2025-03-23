import os

def save_text_to_file(text, output_path):
    """Save text to a file with UTF-8 encoding."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

def remove_file(file_path):
    """Remove a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)