import os
import subprocess
from pathlib import Path

def get_folder_path():
    while True:
        # Prompt the user for a folder path
        folder_input = input("Enter the folder path containing .MOV files: ").strip()
        
        # Expand user path (handles '~' correctly)
        folder_path = Path(folder_input).expanduser().resolve()
        
        if folder_path.exists() and folder_path.is_dir():
            return folder_path
        else:
            print(f"Error: '{folder_input}' is not a valid directory. Please try again.\n")

def convert_mov_to_mp4():
    folder_path = get_folder_path()
    
    # Find all .mov and .MOV files in the specified folder
    mov_files = list(folder_path.glob("*.MOV")) + list(folder_path.glob("*.mov"))
    
    if not mov_files:
        print(f"No .MOV files found in: {folder_path}")
        return

    print(f"\nFound {len(mov_files)} .MOV file(s) to process in {folder_path}\n" + "-" * 50)

    for input_path in mov_files:
        output_path = input_path.with_suffix(".mp4")
        
        # Skip if MP4 already exists to prevent unnecessary conversion
        if output_path.exists():
            print(f"Skipping (MP4 already exists): {output_path.name}")
            continue

        cmd = [
            "ffmpeg",
            "-y",                   # Overwrite output file if forced
            "-i", str(input_path),
            "-c:v", "libx264",      # Standard H.264 video codec
            "-c:a", "aac",          # Standard AAC audio codec
            str(output_path)
        ]

        print(f"Converting: {input_path.name} -> {output_path.name}...")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"Done: {output_path.name}\n")
        except subprocess.CalledProcessError:
            print(f"Failed to convert: {input_path.name}\n")

if __name__ == "__main__":
    convert_mov_to_mp4()
