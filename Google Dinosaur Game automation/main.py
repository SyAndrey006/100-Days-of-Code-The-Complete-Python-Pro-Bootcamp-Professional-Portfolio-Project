import pyautogui
from PIL import ImageGrab
import time

dino_x = 700
dino_y = 260

print("Program starts in 3 seconds, switch to window...")
time.sleep(3)

while True:
    #for big cactus
    img = ImageGrab.grab(
        bbox=(
            dino_x + 40,
            dino_y + 3,
            dino_x + 140,
            dino_y + 33
        )
    )

    bg_r, bg_g, bg_b = img.getpixel((0, 0))
    is_obstacle_detected = False

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            diff = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)

            if diff > 100:
                pyautogui.press("space")
                # time.sleep(0.215 )
                # pyautogui.keyDown ("down")
                # time.sleep(0.1)
                # pyautogui.keyUp( "down")
                is_obstacle_detected = True
                break

        if is_obstacle_detected:
            break

    if is_obstacle_detected:
        time.sleep(0.004)
        continue

    #for flying dino
    img = ImageGrab.grab(
        bbox=(
            dino_x + 40,
            dino_y - 10,
            dino_x + 120,
            dino_y - 8
        )
    )

    bg_r, bg_g, bg_b = img.getpixel((0, 0))
    is_obstacle_detected = False

    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            diff = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)

            if diff > 100:
                pyautogui.keyDown("down")
                time.sleep(0.25)
                pyautogui.keyUp("down")
                is_obstacle_detected = True
                break

        if is_obstacle_detected:
            break

    time.sleep(0.004)


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