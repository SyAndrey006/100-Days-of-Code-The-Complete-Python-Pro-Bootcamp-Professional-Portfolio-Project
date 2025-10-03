import tkinter as tk
import random

root = tk.Tk()
root.title("Breakout")

# Window
window_width = 600
window_height = 400
canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black")
canvas.pack()

# Bricks
brick_rows = 3
brick_cols = 10
brick_width = window_width / brick_cols
brick_height = 20
top_offset = 40
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        x1 = col * brick_width
        y1 = top_offset + row * brick_height
        x2 = x1 + brick_width - 2
        y2 = y1 + brick_height - 2
        brick = canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
        bricks.append(brick)

# Moving Platform
paddle_width = 100
paddle_height = 10
paddle_speed = 20
paddle = canvas.create_rectangle(
    (window_width - paddle_width)/2,
    window_height - 25,
    (window_width + paddle_width)/2,
    window_height - 25 + paddle_height,
    fill="white")

def move_left(event):
    paddle_x1, paddle_y1, paddle_x2, paddle_y2 = canvas.coords(paddle)
    if paddle_x1 - paddle_speed >= 0:
        canvas.move(paddle, -paddle_speed, 0)

def move_right(event):
    paddle_x1, paddle_y1, paddle_x2, paddle_y2 = canvas.coords(paddle)
    if paddle_x2 + paddle_speed <= window_width:
        canvas.move(paddle, paddle_speed, 0)

canvas.bind_all("<Left>", move_left)
canvas.bind_all("<Right>", move_right)

# Ball
ball_radius = 5
ball_speed = 3
ball_dx_speed = ball_speed * random.choice([-1, 1])
ball_dy_speed = -ball_speed

ball_starting_x1 = window_width/2 - ball_radius
ball_starting_y1 = window_height - 25 - 5 - 2*ball_radius
ball_starting_x2 = ball_starting_x1 + 2*ball_radius
ball_starting_y2 = ball_starting_y1 + 2*ball_radius

ball = canvas.create_oval(
    ball_starting_x1,
    ball_starting_y1,
    ball_starting_x2,
    ball_starting_y2,
    fill="gray")

def ball_to_start():
    global ball_dx_speed, ball_dy_speed
    canvas.coords(ball, ball_starting_x1, ball_starting_y1, ball_starting_x2, ball_starting_y2)
    ball_dx_speed = ball_speed * random.choice([-1, 1])
    ball_dy_speed = -ball_speed

def move_ball():
    global ball_dx_speed, ball_dy_speed
    canvas.move(ball, ball_dx_speed, ball_dy_speed)
    ball_x1, ball_y1, ball_x2, ball_y2 = canvas.coords(ball)

    if not bricks:
        canvas.delete("all")
        canvas.create_text(300, 200, text="Game Over", fill="yellow", font=("Arial", 40))
        return

    if ball_x1 <= 0 or ball_x2 >= window_width:
        ball_dx_speed = -ball_dx_speed
    if ball_y1 <= 0:
        ball_dy_speed = -ball_dy_speed
    if ball_y2 >= window_height:
        ball_to_start()

    paddle_x1, paddle_y1, paddle_x2, paddle_y2 = canvas.coords(paddle)
    if ball_x2 >= paddle_x1 and ball_x1 <= paddle_x2 and ball_y2 >= paddle_y1 and ball_y1 <= paddle_y2:
        ball_dy_speed = -ball_dy_speed

    for brick in bricks[:]:
        brick_x1, brick_y1, brick_x2, brick_y2 = canvas.coords(brick)
        if ball_x2 >= brick_x1 and ball_x1 <= brick_x2 and ball_y2 >= brick_y1 and ball_y1 <= brick_y2:
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy_speed = -ball_dy_speed
            break

    root.after(20, move_ball)

move_ball()
root.mainloop()