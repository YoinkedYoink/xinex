if __name__=='__main__':
    from ultralytics import YOLO

    # Load a model
    model = YOLO('yolov8n.yaml')  # build a new model from YAML
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
    model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

    # Train the model

    results = model.train(data=r'C:\Users\Nord\Downloads\Enemy Finder.v3i.yolov8/data.yaml', epochs=300, imgsz=640, batch=8, project='v1Pink', device=0)