import os
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'dataset')

IMAGES_URL = 'http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar'
ANOT_URL = 'http://vision.stanford.edu/aditya86/ImageNetDogs/annotation.tar'


# Check if the directory exists, if not, create it
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created directory: {DATA_FOLDER}")


# Download the dataset
import urllib.request
import zipfile
import shutil

def download_package(url):
    # Define the file name and path
    filename = os.path.join(DATA_FOLDER, url.split('/')[-1])
    
    # Download the file
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    
    # Unzip the downloaded file
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(DATA_FOLDER)
    
    # Remove the zip file after extraction
    os.remove(filename)
    print(f"Downloaded and extracted {filename}")

if __name__ == '__main__':
    download_package(IMAGES_URL)