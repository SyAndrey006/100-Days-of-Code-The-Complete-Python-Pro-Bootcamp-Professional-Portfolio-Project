import pyautogui
from PIL import ImageGrab
import time

dino_x = 700
dino_y = 260

time.sleep(3)

while True:
    img = ImageGrab.grab(
        bbox=(
            dino_x + 110,
            dino_y + 10,
            dino_x + 130,
            dino_y + 30
        )
    )

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            if r > 50:
                pyautogui.press("space")
                break
        else:
            continue
        break

    time.sleep(0.01)


# from PIL import ImageGrab
# import time
#
# dino_x = 700
# dino_y = 260
#
# time.sleep(3)
# while True:
#     img = ImageGrab.grab(
#         bbox=(
#             dino_x + 60,
#             dino_y + 20,
#             dino_x + 90,
#             dino_y + 50
#         )
#     )
#     print(img.getpixel((10, 10)))
#     time.sleep(0.1)