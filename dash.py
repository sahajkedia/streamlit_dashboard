import sqlite3
import random
import os
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import streamlit as st

class ImageSelection(BaseModel):
    id: Optional[int] = None  
    image1_path: str
    image2_path: str
    selected_image_path: str

def init_db():
    conn = sqlite3.connect("image_selection.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imageselection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image1_path TEXT NOT NULL,
            image2_path TEXT NOT NULL,
            selected_image_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_selection(image1_path: str, image2_path: str, selected_image_path: str):
    selection = ImageSelection(image1_path=image1_path, image2_path=image2_path, selected_image_path=selected_image_path)
    
    conn = sqlite3.connect("image_selection.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imageselection (image1_path, image2_path, selected_image_path) VALUES (?, ?, ?)
    ''', (selection.image1_path, selection.image2_path, selection.selected_image_path))
    conn.commit()
    conn.close()

init_db()

image_dir = "./1"  # Update this to your images directory

image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if len(image_files) >= 2:
    img1_file, img2_file = random.sample(image_files, 2)
else:
    st.error("Not enough images in the directory.")
    st.stop()

img1_path = os.path.join(image_dir, img1_file)
img2_path = os.path.join(image_dir, img2_file)

image1 = Image.open(img1_path)
image2 = Image.open(img2_path)

st.title("Image Comparison")
col1, col2 = st.columns(2)

selected_image = None

with col1:
    st.image(image1, caption="Image 1")
    if st.button('Select Image 1'):
        selected_image = img1_path
        st.write("You selected Image 1")

with col2:
    st.image(image2, caption="Image 2")
    if st.button('Select Image 2'):
        selected_image = img2_path
        st.write("You selected Image 2")

if selected_image:
    store_selection(img1_path, img2_path, selected_image)
