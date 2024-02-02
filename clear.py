import os
import glob

def clear_files_in_subdirectories(subdirectories):
    current_directory = os.getcwd()

    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(current_directory, subdirectory)
        
        # Check if the subdirectory exists
        if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
            
            # Use glob to get a list of all files in the subdirectory
            files = glob.glob(os.path.join(subdirectory_path, '*'))
            
            # Iterate over the files and remove them
            for file_path in files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    mp3_files = glob.glob(os.path.join(current_directory, '*.mp3'))
    for file_path in mp3_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

subdirectories = ["Voiceovers", "Scripts", "Screenshots", "OutputVideos"]

clear_files_in_subdirectories(subdirectories)