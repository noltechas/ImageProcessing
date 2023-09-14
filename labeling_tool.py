import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Define the initial positions of body joints
body_joints = {
    "Head": (100, 50),
    "Neck": (100, 100),
    "Left Shoulder": (75, 100),
    "Right Shoulder": (125, 100),
    "Left Elbow": (75, 150),
    "Right Elbow": (125, 150),
    "Left Wrist": (75, 200),
    "Right Wrist": (125, 200),
    "Left Hip": (85, 250),
    "Right Hip": (115, 250),
    "Left Knee": (85, 300),
    "Right Knee": (115, 300),
    "Left Ankle": (85, 350),
    "Right Ankle": (115, 350),
    "Left Finger Tip": (50, 220),
    "Right Finger Tip": (150, 220),
    "Left Toe": (85, 380),
    "Right Toe": (115, 380)
}

# Define the body parts as connections between joints
body_parts = [
    ("Head", "Neck"),
    ("Neck", "Left Shoulder"),
    ("Neck", "Right Shoulder"),
    ("Left Shoulder", "Left Elbow"),
    ("Right Shoulder", "Right Elbow"),
    ("Left Elbow", "Left Wrist"),
    ("Right Elbow", "Right Wrist"),
    ("Neck", "Left Hip"),
    ("Neck", "Right Hip"),
    ("Left Hip", "Left Knee"),
    ("Right Hip", "Right Knee"),
    ("Left Knee", "Left Ankle"),
    ("Right Knee", "Right Ankle"),
    ("Left Wrist", "Left Finger Tip"),
    ("Right Wrist", "Right Finger Tip"),
    ("Left Ankle", "Left Toe"),
    ("Right Ankle", "Right Toe")
]

# Initialize the Tkinter window
window = tk.Tk()
window.title("Body Parts Labeling Tool")
window.geometry("800x600")

# Load your image
image_path = 'images/base_image.jpg'
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = Image.fromarray(img)
img_tk = ImageTk.PhotoImage(image=img)

# Create a canvas to display the image
canvas = tk.Canvas(window, width=img.size[0], height=img.size[1])
canvas.pack()

# Function to draw body parts and joints
def draw_body():
    for part1, part2 in body_parts:
        x1, y1 = body_joints[part1]
        x2, y2 = body_joints[part2]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    for joint, (x, y) in body_joints.items():
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        canvas.create_text(x, y - 10, text=joint, fill="red")

# Function to handle click-and-drag
def on_drag_start(event):
    x, y = event.x, event.y
    for joint, (px, py) in body_joints.items():
        if px - 5 <= x <= px + 5 and py - 5 <= y <= py + 5:
            canvas.bind("<Motion>", lambda e, j=joint: on_drag(e, j))
            canvas.bind("<ButtonRelease-1>", on_drag_end)
            break

def on_drag(event, joint):
    x, y = event.x, event.y
    body_joints[joint] = (x, y)
    redraw_canvas()

def on_drag_end(event):
    canvas.unbind("<Motion>")
    canvas.unbind("<ButtonRelease-1>")

def redraw_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    draw_body()

# Draw the initial body
draw_body()

# Bind mouse events for dragging
canvas.bind("<Button-1>", on_drag_start)

# Run the Tkinter main loop
window.mainloop()
