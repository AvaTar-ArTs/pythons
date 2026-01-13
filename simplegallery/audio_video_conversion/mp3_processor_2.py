import os
import shutil

# Define the base directory
base_dir = "/Users/steven/Music/nocTurneMeLoDieS/mp4"


def organize_files():
    # Check if the base directory exists
    if not os.path.exists(base_dir):
        print(f"❌ Error: The directory '{base_dir}' does not exist.")
        return

    # List all files in the base directory
    try:
        files = os.listdir(base_dir)
    except Exception as e:
        print(f"❌ Error accessing directory '{base_dir}': {e}")
        return

    # Filter out directories and unrelated files
    valid_files = [
        file
        for file in files
        if not os.path.isdir(os.path.join(base_dir, file))
        and (
            file.endswith(".mp4")
            or file.endswith(".mp3")
            or file.endswith("_analysis.txt")
            or file.endswith("_transcript.txt")
        )
    ]

    total_files = len(valid_files)
    print(f"🔍 Found {total_files} valid files to organize.")

    # Process each file with a countdown
    for index, file in enumerate(valid_files, start=1):
        print(f"📂 Processing file {index}/{total_files}: {file}")
        file_path = os.path.join(base_dir, file)

        # Extract the base name (album name) from the file
        album_name = None
        if file.endswith(".mp4"):
            album_name = file.replace(".mp4", "")
        elif file.endswith(".mp3"):
            album_name = file.replace(".mp3", "")
        elif file.endswith("_analysis.txt"):
            album_name = file.replace("_analysis.txt", "")
        elif file.endswith("_transcript.txt"):
            album_name = file.replace("_transcript.txt", "")
        else:
            print(f"Skipping unrelated file: {file}")
            continue

        # Create a folder for the album if it doesn't exist
        album_folder = os.path.join(base_dir, album_name)
        if not os.path.exists(album_folder):
            try:
                os.makedirs(album_folder)
                print(f"✅ Created folder: {album_folder}")
            except Exception as e:
                print(f"❌ Error creating folder '{album_folder}': {e}")
                continue

        # Define destination paths for different types of files
        mp4_path = os.path.join(album_folder, f"{album_name}.mp4")
        mp3_path = os.path.join(album_folder, f"{album_name}.mp3")
        analysis_path = os.path.join(album_folder, f"{album_name}_analysis.txt")
        transcript_path = os.path.join(album_folder, f"{album_name}_transcript.txt")

        # Move the files to the corresponding folder, skipping if already done
        try:
            if file.endswith(".mp4"):
                if not os.path.exists(mp4_path):
                    shutil.move(file_path, mp4_path)
                    print(f"Moved: {file} to {mp4_path}")
                else:
                    print(f"Skipping: {file} already exists at {mp4_path}")
            elif file.endswith(".mp3"):
                if not os.path.exists(mp3_path):
                    shutil.move(file_path, mp3_path)
                    print(f"Moved: {file} to {mp3_path}")
                else:
                    print(f"Skipping: {file} already exists at {mp3_path}")
            elif file.endswith("_analysis.txt"):
                if not os.path.exists(analysis_path):
                    shutil.move(file_path, analysis_path)
                    print(f"Moved: {file} to {analysis_path}")
                else:
                    print(f"Skipping: {file} already exists at {analysis_path}")
            elif file.endswith("_transcript.txt"):
                if not os.path.exists(transcript_path):
                    shutil.move(file_path, transcript_path)
                    print(f"Moved: {file} to {transcript_path}")
                else:
                    print(f"Skipping: {file} already exists at {transcript_path}")
        except Exception as e:
            print(f"❌ Error moving file '{file}': {e}")

    print("✅ All files have been organized successfully.")


if __name__ == "__main__":
    organize_files()
