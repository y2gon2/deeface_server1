import asyncio
import aiohttp
from time import time
import copy
import aiofiles

URL = 'http://192.168.0.49:8000/afe'
PATH = '../small_dataset/total/'
PATH1 = '../small_dataset/total/1.jpg'
FILE1 = {'image': open(PATH1, "rb")}

def file_open(num):
    file_path = PATH + str(num) + '.jpg'
    file = {"image" : open(file_path, "rb")}
    return file


async def file_upload(file):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data=file) as resp:
            print(await resp.text())


tasks = []
for i in range(1, 101):
    file = file_open(i)
    tasks.append(file_upload(file))

start = time()
asyncio.run(asyncio.wait(tasks))
end = time()

print("Latency for 100 pics : %.5f sec" %(end - start))