import cv2
import os
import json  # Importing json for saving collected data


# Define directories for storing images and data

smile_dir = "data/smile"
no_smile_dir = "data/no_smile"
hand_dir = "data/hand_gestures"

os.makedirs(smile_dir, exist_ok=True)
os.makedirs(no_smile_dir, exist_ok=True)
os.makedirs(hand_dir, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0
data_collection = []  # List to store collected data

label = input("Enter label (smile/no_smile/gesture): ")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Data Collection", frame)

    # Save image
    file_name = f"{label}_{count}.jpg"  # File name for the collected image
    data_collection.append({"label": label, "file_name": file_name})  # Save label and file name

    if label == "smile":
        cv2.imwrite(os.path.join(smile_dir, file_name), frame)
    elif label == "no_smile":
        cv2.imwrite(os.path.join(no_smile_dir, file_name), frame)
    else:
        cv2.imwrite(os.path.join(hand_dir, file_name), frame)

    count += 1

    # Press 'q' to stop capturing
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save collected data to a JSON file
with open("collected_data.json", "w") as json_file:
    json.dump(data_collection, json_file)

cap.release()  # Release the video capture

cv2.destroyAllWindows()
