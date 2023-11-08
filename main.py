import os
import cv2
import json
import mediapipe as mp
from Encoder import DetectionJSONEncoder

# The expected output is a JSON file containing both the timestamp and the model's raw output for each corresponding frame.

def parse(url,model=None,fps=5):
    """ 
    Takes URL of a video, processes it, passes it through
    a face detection model and returns a JSON object containing
    timestamp and the model's raw output for each corresponding 
    frame
    
    Parameters:
    url: url to the video
    model: a face detection model
    
    Returns:
    JSON object: List of objects with timestamp and model's raw output
    """    
    if(model==None):
        mp_face_detection = mp.solutions.face_detection
        # model = mp_face_detection.FaceDetection(min_detection_confidence=0.7)
        model = mp_face_detection.FaceDetection(model_selection=1)
        
    cap = cv2.VideoCapture(url)
    videoFps = cap.get(cv2.CAP_PROP_FPS)
    if(videoFps<fps):
        # if the video has lesser fps than minimum requirement
        fps = videoFps

    frame_skip = round(videoFps / fps)
    frameNumber = 0
    output = []
    while cap.isOpened():
        ret, frame = cap.read()
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        if not ret:
            break
        
        if frameNumber % frame_skip == 0:
            val = {"timestamp":timestamp,"model_output":""}
            results =  model.process(frame)
            if not results.detections:
                val["model_output"]="{}"
            else :
                detectionList = []
                for detection in results.detections:
                    detectionList.append(detection)
                val["model_output"] =detectionList


            output.append(val)
            
        frameNumber += 1
    with open("output.json", "w") as outfile:
        json.dump(output, outfile,cls=DetectionJSONEncoder)

def main():
    URL = os.environ['CONTENT_URL']
    parse(URL)
    
if __name__ == "__main__":
    main()
