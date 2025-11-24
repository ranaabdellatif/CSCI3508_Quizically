"""
AI Trivia Generator using Gemini Model with Tkinter GUI
Author: Rana Abdellatif
Date: November 2025
"""
import tkinter as tk
from tkinter import messagebox
import google.generativeai as genai

#load API key from .env file
from dotenv import load_dotenv
import os

load_dotenv()
#configure Gemini API key
genai.configure(api_key=os.getenv("API_KEY"))
#model = genai.GenerativeModel("models/gemini-flash-latest")
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")


#~~~FUNCTION TO GENERATE TRIVIA~~~
def generate_trivia():
    topic = topic_entry.get()
    num_questions = num_entry.get()
    #validate inputs
    if not topic.strip():
        messagebox.showerror("Error", "Please enter a topic.")
        return

    try:
        num_questions = int(num_questions)
    except:
        messagebox.showerror("Error", "Number of questions must be an integer.")
        return
    #construct prompt
    prompt = (
        f"Generate {num_questions} trivia questions and answers about: {topic}.\n"
        f"Format exactly as:\n"
        f"Q1: ...\nA1: ...\nQ2: ...\nA2: ...\n"
    )
    #call gemini model
    try:
        response = model.generate_content(prompt)
        result = response.text

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Gemini Error", str(e))


#~~~TKINTER GUI~~~
root = tk.Tk()
root.title("AI Trivia Generator (Gemini)")
root.geometry("700x600")

#input fields
tk.Label(root, text="Topic (ex: age-friendly, 2010's pop music):").pack()
topic_entry = tk.Entry(root, width=60)
topic_entry.pack()

#number of questions
tk.Label(root, text="Number of Questions:").pack()
num_entry = tk.Entry(root, width=10)
num_entry.insert(0, "10")
num_entry.pack()

#generate button
generate_button = tk.Button(root, text="Generate Trivia", command=generate_trivia)
generate_button.pack(pady=10)

#output box
output_box = tk.Text(root, wrap="word", height=25, width=80)
output_box.pack()

#run gui loop
root.mainloop()
