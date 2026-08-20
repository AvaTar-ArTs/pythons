import csv

from pytube import YouTube


# Function to extract video metadata
def get_video_info(url):
    yt = YouTube(url)
    video_info = {
        "Title": yt.title,
        "Views": yt.views,
        "Likes": yt.rating,
        "Length (seconds)": yt.length,
        "Description": yt.description,
    }
    return video_info


# Function to write info to CSV
def write_to_csv(video_info, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = video_info.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        writer.writerow(video_info)  # Write the video info


# Main
video_url = "https://youtu.be/VTRp7hQkZos"  # Replace with your YouTube URL
csv_file = "video_info.csv"  # Output CSV file

video_info = get_video_info(video_url)
write_to_csv(video_info, csv_file)

print(f"Video information saved to {csv_file}")
