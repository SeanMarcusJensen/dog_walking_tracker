from ultralytics import YOLO

model = YOLO("yolo11n.pt")  # Load a pretrained YOLOv8 model

results = model.train(
    data="./datasets/data.yaml",  # Path to the dataset configuration file
    epochs=20,  # Number of training epochs
    batch=16,  # Batch size
    imgsz=640,  # Input image size
    device=0,  # Device to train on (0 for GPU, 'cpu' for CPU)
    pretrained=True,  # Use pretrained weights
    project="runs/train",  # Directory to save training results
    name="hand_gesture",  # Name of the training run
    exist_ok=True,  # Overwrite existing results
    save_period=5,  # Save model every epoch
    save_json=True,  # Save JSON file with training results
    cache=True,  # Cache images for faster training
    workers=8,  # Number of worker threads for data loading
    patience=10,  # Early stopping patience
)
