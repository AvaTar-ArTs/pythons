import os
from opus_replica import OpusReplica

# 1. Setup - Using provided video
test_video = "IMG_2319.MOV.mp4" 

if not os.path.exists(test_video):
    print(f"Error: Could not find '{test_video}'. Please ensure it's in this directory.")
    exit(1)

# 2. Run Pipeline
pipeline = OpusReplica(test_video)
pipeline.get_transcript()
clips = pipeline.identify_clips()

if not clips:
    print("No clips identified. Check API response or transcript content.")
else:
    for clip in clips:
        print(f"Processing: {clip['title']}")
        pipeline.extract_and_assemble(clip)

print("Test complete.")
