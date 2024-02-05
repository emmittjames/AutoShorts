import os
import glob

def clear_files_in_subdirectories(subdirectories):
    current_directory = os.getcwd()

    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(current_directory, subdirectory)
        if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
            files = glob.glob(os.path.join(subdirectory_path, '*'))
            for file_path in files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

subdirectories = ["Voiceovers", "Scripts", "Screenshots", "OutputVideos"]

clear_files_in_subdirectories(subdirectories)