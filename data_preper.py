import os
import shutil
import random
from PIL import Image
from random import randint

#dataset=https://www.kaggle.com/datasets/hasibalmuzdadid/shoe-vs-sandal-vs-boot-dataset-15k-images
def extract_data():
    filename="shoes.zip"
    extract_dir="shoes_unzipped"    
    os.makedirs(extract_dir , exist_ok=True)
    shutil.unpack_archive(filename, extract_dir)


def split_images(source_folder, train_folder, validation_folder, test_folder):
    # Make sure destination folders exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(validation_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

   # Get a list of files in the source folder
    files = os.listdir(source_folder)
    
    # Shuffle the files randomly
    random.shuffle(files)

    # Calculate the number of images for validation and test sets (10% each)
    total_images = len(files)
    validation_size = (0.1 * total_images)
    test_size = (0.2 * total_images)

    # Counters for each set
    validation_count = 0
    test_count = 0

    # Iterate through the files and copy them to the appropriate folders
    for file in files:
        source_path = os.path.join(source_folder, file)

        # Determine the destination folder based on counters
        if validation_count < validation_size:
            destination_path = os.path.join(validation_folder, file)
            validation_count += 1
        elif test_count < test_size:
            destination_path = os.path.join(test_folder, file)
            test_count += 1
        else:
            destination_path = os.path.join(train_folder, file)

        shutil.copy(source_path, destination_path)
    
    

def augment_images(input_folder, output_folder, num_augmented_images_per_original=3):
    
    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        ############################
        image_path = os.path.join(input_folder, image_file)
        input_image = Image.open(image_path)

        # Define the new size (width, height)
        new_size = (64, 64)

        # Resize the image
        resized_image = input_image.resize(new_size)

        # Save the resized image, overwriting the original file
        resized_image.save(image_path)

        # Close the image files
        input_image.close()
        ############################
        
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        
        
        
        # Load the image using PIL
        original_image = Image.open(image_path)

        # Apply augmentation to the image
        for idx in range(num_augmented_images_per_original):
            augmented_image = apply_random_augmentation(original_image)
            output_file = f"{image_file.split('.')[0]}_aug_{idx + 1}.{image_file.split('.')[1]}"
            output_path = os.path.join(output_folder, output_file)

            # Save augmented image
            augmented_image.save(output_path)

def apply_random_augmentation(image):
    # Randomly select an augmentation type
    augmentation_type = randint(1, 2)

    if augmentation_type == 1:
        # Random rotation
        rotation_angle = randint(-25, 25)
        augmented_image = image.rotate(rotation_angle)
    elif augmentation_type == 2:
        # Random flip (horizontal or vertical)
        flip_type = randint(1, 2)
        augmented_image = image.transpose(Image.FLIP_LEFT_RIGHT) if flip_type == 1 else image.transpose(Image.FLIP_TOP_BOTTOM)
   

    return augmented_image

def rename_files(directory_path, prefix1,prefix2,prefix3):
   files = os.listdir(directory_path)
   prefixes=[prefix1,prefix2,prefix3]
   for prefix in prefixes:
       for index, old_filename in enumerate(files, start=1):
           if old_filename.startswith(prefix):
               _, extension = os.path.splitext(old_filename)
               new_filename = f"{prefix}_{index}{extension}"
            
               old_path = os.path.join(directory_path, old_filename)
               new_path = os.path.join(directory_path, new_filename)

               os.rename(old_path, new_path)

def data_preper():
    extract_data()
    augment_images("shoes_unzipped/shoes", "shoes_unzipped/shoes")
    rename_files("shoes_unzipped/shoes","boot","Sandal","Shoe")
    split_images("shoes_unzipped/shoes","shoes_unzipped/train_folder",
                 "shoes_unzipped/validation_folder","shoes_unzipped/test_folder")
    


