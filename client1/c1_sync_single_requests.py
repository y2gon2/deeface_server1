import requests
import time


PATH = '../small_dataset/total/'

def afe_request():
    for i in range(1, 101):
        file_path = PATH + '%i.jpg' % i
        with open(file_path, 'rb') as f:
            # print(type(f))
            upload = {'image': f}
            print(upload)
            res = requests.post('http://192.168.0.49:8000/afe', files=upload)
            print(res.headers)
            print(res.json())

if __name__ =="__main__":
    start = time.time()
    afe_request()
    end = time.time()
    duration = end - start
    print("Latency for 100 pics : %0.5f sec" %duration)
