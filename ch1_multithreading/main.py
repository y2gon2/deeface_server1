from deepface import DeepFace
from fastapi import FastAPI, File, WebSocket
from starlette.websockets import WebSocketDisconnect
from pydantic import BaseModel
from logging import info
import time
import json
import uvicorn
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pipe

NUM_OF_DEEPLEARNING_PROCESS: int = 5


class Analysis(BaseModel):
    face: bool
    emotion: str
    exp: str


class Statistic:
    def __init__(self):
        self.current_latency: float = 0.0
        self.accumulated_duration: float = 0.0
        self.times: int = 0
        self.average_latency: float = 0.0
        # self.start: float = 0.0
        # self.per_minute: float = 0.0

    def get(self):
        data = {
            'current latency': self.current_latency,
            'accumulated duration': self.accumulated_duration,
            'times': self.times,
            'average latency': self.average_latency
        }
        return data


    def set(self, current_latency: float):
        self.current_latency = current_latency
        self.accumulated_duration += current_latency
        self.times += 1

        if self.times != 0:
            self.average_latency = self.accumulated_duration / self.times

    def show(self):
        print("==============================================")
        print("* Current Latency: %.5f sec" % self.current_latency)
        print("* Average Latency: %.5f sec" % self.average_latency)
        print("==============================================")




def classify_emotion(emotion) -> str:
    # print(emotion)
    # Group emotions in broad categories.
    positive = emotion.get("happy")
    negative = emotion.get("angry") + emotion.get("disgust") + emotion.get("fear") + emotion.get("sad")
    neutral = emotion.get("neutral")

    if positive >= 80.0:
        return "positive"
    if negative >= 95.0:
        return "negative"

    return "neutral"

# --------------------------------------------------
app = FastAPI()

# --------------------------------------------------

@app.post("/afe")
async def analyze_facial_expression(image: bytes = File()) -> Analysis:
    start = time.time()
    try:
        output = DeepFace.analyze(
            img_path=image,
            actions=['emotion'],
        )

        # Avoid processing multiple faces.
        if len(output) > 1:
            return Analysis(face=False, emotion="", exp="Multiple face detected.")

        # Analyze the facial expression.
        emotion_analysis = classify_emotion(output[0].get("emotion"))
        end = time.time()
        statistic.set(end - start)
        # statistic.show()
        return Analysis(face=True, emotion=emotion_analysis, exp="Succeed")
    except ValueError:
        end = time.time()
        statistic.set(end - start)
        # statistic.show()
        return Analysis(face=False, emotion="Unable to detect any face.", exp="Failed")


@app.get("/result")
async def result():
    data = statistic.get()
    json_data = json.dumps(data)
    return json_data

# --------------------------------------------------
async def deeplearning(image):
    try:
        output = DeepFace.analyze(
            img_path=image,
            actions=['emotion'],
        )

        # Avoid processing multiple faces.
        if len(output) > 1:

            return Analysis(face=False, emotion="", exp="Multiple face detected.")

        # Analyze the facial expression.
        emotion_analysis = classify_emotion(output[0].get("emotion"))
        end = time.time()
        statistic.set(end - start)
        # statistic.show()
        return Analysis(face=True, emotion=emotion_analysis, exp="Succeed")
    except ValueError:
        end = time.time()
        statistic.set(end - start)
        # statistic.show()
        return Analysis(face=False, emotion="Unable to detect any face.", exp="Failed")



# --------------------------------------------------

if __name__=="__main__":
    statistic = Statistic()
    deeplearning_conn1, broker_conn1 = Pipe()
    deeplearning_conn2, broker_conn2 = Pipe()
    deeplearning_conn3, broker_conn3 = Pipe()
    deeplearning_conn4, broker_conn4 = Pipe()
    deeplearning_conn5, broker_conn5 = Pipe()

    with ThreadPoolExecutor(10) as executor:
        executor.submit(broker, ())
        executor.submit(deeplearning, )
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
