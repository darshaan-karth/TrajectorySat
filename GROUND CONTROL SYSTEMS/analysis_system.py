from ultralytics import YOLO
#import storage_system
import os

model = YOLO("crater.pt")

def detect_craters(image_path, save_folder, file_name):
    numCraters = 0
    img_folder = file_name.split(".")[0]
    
    # Run prediction and save automatically
    results = model.predict(
        source=image_path,
        conf=0.1,
        save=True,                     # save annotated images
        project=save_folder,           # folder to save in
        name=img_folder,               # subfolder name
        exist_ok=True                  # overwrite if exists
    )

    with open(save_folder+img_folder+"/"+img_folder+".txt", "w") as f:
        f.write("Class Name|Confidence|x1|y1|x2|y2")
        for result in results:
            boxes = result.boxes
            numCraters+=len(boxes)
            for box in boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                class_name = model.names[class_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                f.write(f"\n{class_name}|{confidence:.2f}|{x1}|{y1}|{x2}|{y2}")

    os.rename(image_path, save_folder+img_folder+"/org_"+file_name)
    os.rename(save_folder+img_folder+"/"+file_name, save_folder+img_folder+"/analyzed_"+file_name)
    return numCraters

def analyze_data():
    image_path = "C:/Users/karthikeyan.gurunath/Documents/Darshaan_Project/TrajectorySat/DOWNLINK_DATA/Images/"
    save_path = "C:/Users/karthikeyan.gurunath/Documents/Darshaan_Project/TrajectorySat/ANALYZED_DATA/"

    if os.path.isdir(image_path):
        os.makedirs(save_path, exist_ok=True)

        img_files = os.listdir(image_path)
        for file in img_files:
            img_fl = os.path.join(image_path, file)

            num_craters = detect_craters(img_fl, save_path, file)
            print("Number of craters detected: {}".format(num_craters))

        os.rmdir(image_path)

    else:
        print("No images found to analyze.")