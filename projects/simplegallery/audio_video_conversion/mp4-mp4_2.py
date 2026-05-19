import cv2


def process_frame(frame):
    """
    Example processing function for large video files.
    Modify this to apply your custom image processing logic.
    """
    # Example: Convert frame to grayscale
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return processed_frame


def process_large_video(input_video_path, output_video_path):
    """
    Process large MP4 video files efficiently.
    """
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get video properties: FPS, resolution
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define codec and create VideoWriter object for saving processed video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # You can change codec if needed
    out = cv2.VideoWriter(
        output_video_path, fourcc, fps, (width, height), isColor=False
    )

    frame_count = 0  # Track number of processed frames
    print("Processing video...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Break if no more frames are available

        # Process the frame (apply image transformation)
        processed_frame = process_frame(frame)

        # Write the processed frame to output video
        out.write(processed_frame)

        frame_count += 1
        if frame_count % 100 == 0:  # Print status every 100 frames
            print(f"Processed {frame_count} frames...")

    # Release resources
    cap.release()
    out.release()

    print("Processing complete.")


# Example usage
input_video = "/Users/steven/Pictures/2025/Heritage-of-Hate_-The-White-Supremacist--2024-09-07.mp4"
output_video = "output_heritage_of_hate_processed.mp4"

process_large_video(input_video, output_video)
