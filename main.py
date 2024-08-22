import tkinter as tk
import random

window = tk.Tk()
window.title("Breakout Game")
window.resizable(False, False)

canvas = tk.Canvas(window, width=500, height=400, bg="black")
canvas.pack()

paddle = canvas.create_rectangle(0, 390, 80, 400, fill="white")
paddle_speed = 20

ball = canvas.create_oval(240, 240, 260, 260, fill="red")
ball_speed_x = random.choice([-4, -3, -2, 2, 3, 4])
ball_speed_y = -4

bricks = [canvas.create_rectangle(j * (500 // 7), i * 20, (j + 1) * (500 // 7), (i + 1) * 20, fill="blue") for i in
          range(5) for j in range(7)]


def move_paddle(event):
    direction = -paddle_speed if event.keysym == "Left" else paddle_speed
    canvas.move(paddle, direction, 0)
    paddle_pos = canvas.coords(paddle)
    if paddle_pos[0] < 0:
        canvas.move(paddle, -paddle_pos[0], 0)
    elif paddle_pos[2] > 500:
        canvas.move(paddle, 500 - paddle_pos[2], 0)


window.bind("<Left>", move_paddle)
window.bind("<Right>", move_paddle)


def move_ball():
    global ball_speed_x, ball_speed_y
    canvas.move(ball, ball_speed_x, ball_speed_y)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    if ball_pos[0] <= 0 or ball_pos[2] >= 500:
        ball_speed_x = -ball_speed_x
    if ball_pos[1] <= 0:
        ball_speed_y = -ball_speed_y
    if ball_pos[3] >= 400:
        canvas.create_text(250, 200, text="Game Over", fill="white", font=("Helvetica", 24))
        return

    if paddle_pos[0] <= ball_pos[2] <= paddle_pos[2] and paddle_pos[1] <= ball_pos[3] <= paddle_pos[3]:
        ball_speed_y = -ball_speed_y

    for brick in bricks:
        brick_pos = canvas.coords(brick)
        if brick_pos[0] <= ball_pos[2] <= brick_pos[2] and brick_pos[1] <= ball_pos[3] <= brick_pos[3]:
            canvas.delete(brick)
            bricks.remove(brick)
            ball_speed_y = - ball_speed_y
            break

    if not bricks:
        canvas.create_text(250, 200, text="You Win!", fill="white", font=("Helvetica", 24))
        return

    window.after(20, move_ball)


move_ball()
window.mainloop()
