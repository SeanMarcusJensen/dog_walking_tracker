import pandas as pd
import os
import cv2
import numpy as np
from tqdm import tqdm

base = os.path.dirname(os.path.abspath(__file__))
datafiles = os.path.join(base, "archive")


def convert_csv_to_images(csv_file, output_dir, split):
    df = pd.read_csv(csv_file)
    for i, row in tqdm(df.iterrows(), total=len(df)):
        label = str(row[0])
        pixels = np.array(row[1:]).reshape(28, 28).astype(np.uint8)
        label_dir = os.path.join(output_dir, split, label)
        os.makedirs(label_dir, exist_ok=True)
        img_path = os.path.join(label_dir, f"{i}.jpg")
        cv2.imwrite(img_path, pixels)


convert_csv_to_images("sign_mnist_train.csv", "asl_dataset", "train")
convert_csv_to_images("sign_mnist_test.csv", "asl_dataset", "val")
