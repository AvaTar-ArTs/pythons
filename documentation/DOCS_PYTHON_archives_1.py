import os
import tarfile

# List of directories to include in the tar.gz archive
directories = [
    "/Users/steven/Pictures/other-07-25-05:32.csv",
    "/Users/steven/Pictures/audio-07-25-05:31.csv",
    "/Users/steven/Pictures/docs-07-25-05:31.csv",
    "/Users/steven/Pictures/image_data-07-25-05:32.csv",
    "/Users/steven/Pictures/vids-07-25-05:34.csv",
]

# Output tar.gz file
output_filename = "/Users/steven/Pictures/data_archive.tar.gz"


# Function to create tar.gz archive
def create_tar_gz(output_filename, directories):
    with tarfile.open(output_filename, "w:gz") as tar:
        for dir_path in directories:
            for root, _, files in os.walk(os.path.dirname(dir_path)):
                for file in files:
                    fullpath = os.path.join(root, file)
                    tar.add(
                        fullpath,
                        arcname=os.path.relpath(
                            fullpath,
                            os.path.dirname(directories[0]),
                        ),
                    )
    print(f"Archive {output_filename} created successfully.")


# Create the tar.gz archive
create_tar_gz(output_filename, directories)
