from ultralytics import YOLO
import pyautogui
import threading
import time
from PIL import Image

from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy
    
import keyboard


def record_screen(stop_event, model, record=False):
    pyautogui.FAILSAFE = False      # this basically removes your ability to move your mouse
    screen_width, screen_height = list(pyautogui.size())
    
    count=0
    while not stop_event.is_set():
        screenshot = pyautogui.screenshot()
        screenshot_result = model(screenshot)  # return a list of Results objects
        class_names = screenshot_result[0].names

        detected_classes = list(map(int, screenshot_result[0].boxes.cls.tolist()))
        detected_confidence = screenshot_result[0].boxes.conf.tolist()
        detected_bbox = screenshot_result[0].boxes.xywh.tolist()
        
        if record:
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.axes.xaxis.set_ticklabels([])
            ax.axes.yaxis.set_ticklabels([])


            ax.imshow(screenshot)

            temp=copy.deepcopy(detected_bbox)
            for i in range(len(temp)):
                temp[i]+=[class_names[detected_classes[i]], detected_confidence[i]]
            for x, y, w, h, i, j, in temp:
                rect = Rectangle((x-w/2,y-h/2), w, h, linewidth=1,edgecolor='r',facecolor='none')
                ax.add_patch(rect)
                ax.text(x-w/2,y-h/2-15, f'{i}| conf: {j:.2f}', bbox=dict(facecolor='red', alpha=0.5))
            fig.savefig(f'hi/{count}')
            count+=1
            
        for bbox, cls, conf in zip(detected_bbox, detected_classes, detected_confidence):
            cls_name = class_names[cls]
            if cls_name == "fruit" and conf > 0.5:
                pyautogui.moveTo(bbox[0]-bbox[2]/2, bbox[1]-bbox[3]/2)
                pyautogui.drag(bbox[2], bbox[3], button='left', duration=0.01)
                

model = YOLO("Models/best.pt")
model.to("cuda")


time.sleep(2)

stop_event = threading.Event()

# starts record your screen
record_thread = threading.Thread(target=record_screen, args=(stop_event, model, True))
record_thread.start()

keyboard.wait("q")

stop_event.set()

record_thread.join()