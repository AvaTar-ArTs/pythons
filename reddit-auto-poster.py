import time

from AskReddit import gen_video_from_hot

delay = 60 * 60 * 12

while True:
    gen_video_from_hot()
    time.sleep(delay)
