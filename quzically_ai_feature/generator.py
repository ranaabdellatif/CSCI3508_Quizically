"""
AI Trivia Generator using Gemini Model with Tkinter GUI
Author: Rana Abdellatif
Date: November 2025
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import PhotoImage
import random
import google.generativeai as genai
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

#config gemini API key
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")


# --- confetti yayyyy ---
CONFETTI_COLORS = ["#f89829", "#ffde00", "#d80c8c", "#4cae43", "#0397d6"]
confetti_shapes = []

def generate_confetti():
    """Generate random decorative shapes."""
    confetti_canvas.delete("all")
    confetti_shapes.clear()

    width = root.winfo_width()
    height = root.winfo_height()

    for _ in range(45):
        color = random.choice(CONFETTI_COLORS)
        x = random.randint(10, width - 10)
        y = random.randint(10, height - 10)
        shape_type = random.choice(["square", "circle", "plus", "dash"])

        if shape_type == "square":
            size = random.randint(8, 16)
            confetti_canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline=color)

        elif shape_type == "circle":
            size = random.randint(8, 16)
            confetti_canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)

        elif shape_type == "plus":
            size = 12
            confetti_canvas.create_line(x, y, x+size, y, fill=color, width=3)
            confetti_canvas.create_line(x+size/2, y-size/2, x+size/2, y+size/2, fill=color, width=3)

        elif shape_type == "dash":
            size = random.randint(10, 20)
            confetti_canvas.create_line(x, y, x+size, y, fill=color, width=3)

def on_resize(event):
    generate_confetti()


# --- main window ---
root = tk.Tk()
root.title("Quizically AI Trivia Generator - Gemini Model")
root.geometry("700x600")
root.configure(bg="#13163f")

# Create confetti canvas FIRST (so all widgets appear above it)
confetti_canvas = tk.Canvas(root, bg="#13163f", highlightthickness=0)
confetti_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

root.bind("<Configure>", on_resize)
generate_confetti()


# rounded rectangle function to make it cuter
def round_rect(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# --- generation logic ---
def generate_trivia():
    topic = topic_entry.get()
    num_questions = num_entry.get()

    if not topic.strip():
        messagebox.showerror("Error", "Please enter a topic.")
        return

    try:
        num_questions = int(num_questions)
    except:
        messagebox.showerror("Error", "Number of questions must be an integer.")
        return

    prompt = (
        f"Generate {num_questions} trivia questions and answers about: {topic}.\n"
        f"Format exactly as:\n"
        f"Q1: ...\nA1: ...\nQ2: ...\nA2: ...\n"
    )

    try:
        response = model.generate_content(prompt)
        result = response.text
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result)
        store_mongo(topic, num_questions, result)

    except Exception as e:
        messagebox.showerror("Gemini Error", str(e))


def store_mongo(topic, num_questions, result):
    try:
        mongo_client = MongoClient(os.getenv("MONGO_URI"))
        db = mongo_client["trivia_db"]
        collection = db["questions"]

        collection.insert_one({
            "topic": topic,
            "num_questions": num_questions,
            "trivia": result
        })

        messagebox.showinfo("Saved", "Trivia stored in MongoDB Atlas!")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# --- UI stuff ---
custom_font = font.Font(family="Itim", size=12)

#quizically logo
logo = PhotoImage(file="quizically_ai_feature/quizicallylogo.png")
logo_label = tk.Label(root, image=logo, bg="#13163f")
logo_label.pack(pady=(10, 20))

#accent lines
accent_colors = ["#f89829", "#ffde00", "#d80c8c", "#4cae43", "#0397d6"]

accent_frame = tk.Frame(root, bg="#13163f")  
accent_frame.pack(fill="x", pady=(0, 25))    #space between logo and accents
accent_frame.lift()                          # ensure above confetti!!!!

#creates staggered accent bars
for i, color in enumerate(accent_colors):
    tk.Frame(
        accent_frame,
        height=4,
        bg=color
    ).pack(
        fill="x",
        padx=40 + i * 15,   
        pady=3
    )


#outer frame (raised above confetti)
frame = tk.Frame(root, bg="#13163f", padx=20, pady=20)
frame.pack(fill="both", expand=True)
frame.lift()

#--- topic entry ---
tk.Label(frame, text="Topic:", font=custom_font, fg="white", bg="#13163f").pack(anchor="w")

topic_canvas = tk.Canvas(frame, width=500, height=45, bg="#13163f", highlightthickness=0)
topic_canvas.pack(pady=(0, 12))

round_rect(topic_canvas, 5, 5, 495, 40, radius=15, fill="white", outline="#fba2b5", width=3)

topic_entry = tk.Entry(
    topic_canvas, width=45, font=custom_font,
    bg="white", fg="#fba2b5", bd=0, insertbackground="#fba2b5"
)
topic_canvas.create_window(250, 22, window=topic_entry)

#--- num of questions ---
tk.Label(frame, text="Number of Questions:", font=custom_font, fg="white", bg="#13163f").pack(anchor="w")

num_canvas = tk.Canvas(frame, width=150, height=45, bg="#13163f", highlightthickness=0)
num_canvas.pack(pady=(0, 12))

round_rect(num_canvas, 5, 5, 145, 40, radius=15, fill="white", outline="#fba2b5", width=3)

num_entry = tk.Entry(
    num_canvas, width=10, font=custom_font,
    bg="white", fg="#fba2b5", bd=0, insertbackground="#fba2b5"
)
num_entry.insert(0, "10")
num_canvas.create_window(75, 22, window=num_entry)

#--- generate button ---
btn_canvas = tk.Canvas(frame, width=200, height=55, bg="#13163f", highlightthickness=0)
btn_canvas.pack(pady=15)

round_rect(btn_canvas, 5, 5, 195, 50, radius=20, fill="#fba2b5", outline="white", width=2)

generate_button = tk.Button(
    btn_canvas, text="Quizically Go!", font=custom_font,
    fg="#13163f", bg="#fba2b5", activebackground="#fba2b5",
    activeforeground="#13163f", bd=0, command=generate_trivia
)
btn_canvas.create_window(100, 27, window=generate_button)

#--- outbut box ---
output_canvas = tk.Canvas(frame, width=620, height=300, bg="#13163f", highlightthickness=0)
output_canvas.pack(pady=(0, 10))

round_rect(output_canvas, 5, 5, 615, 295, radius=20, fill="white", outline="#fba2b5", width=3)

output_box = tk.Text(
    output_canvas, wrap="word", width=70, height=15,
    bg="white", fg="#fba2b5", bd=0, font=custom_font,
    insertbackground="#fba2b5"
)
output_canvas.create_window(310, 150, window=output_box)

#lets go
root.mainloop()
