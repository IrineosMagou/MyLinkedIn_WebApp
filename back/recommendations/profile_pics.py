import os
import shutil
import random


source_directory =  "/mnt/c/Users/User/Desktop/ΕΚΠΑ/ΤΕΔι/201700208_ΤΕΔ24/profile_pics"
 # Directory with the 10 random profile pictures
destination_directory = "/mnt/c/Users/User/Desktop/ΕΚΠΑ/ΤΕΔι/201700208_ΤΕΔ24/back/pictures"
  # Directory where you want to copy the pictures


# Make sure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Get a list of the files in the source directory
files = os.listdir(source_directory)

# Filter to get only image files (optional, based on your needs)
image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))]

# Shuffle the list to randomize the order of the pictures if desired
random.shuffle(image_files)

# Copy and rename the images
for i in range(1, 501):
    # Select a random image from the available ones
    # Use modulus to ensure you cycle through available images
    image_to_copy = image_files[(i - 1) % len(image_files)]
    
    # Define the source and destination paths
    src_path = os.path.join(source_directory, image_to_copy)
    dst_path = os.path.join(destination_directory, f"{i}.jpg")  # Use .jpg or appropriate extension

    # Copy the image to the destination directory with the new name
    shutil.copy(src_path, dst_path)
