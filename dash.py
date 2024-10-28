import random
import os
# from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from PIL import Image
import streamlit as st

engine = create_engine("sqlite:///image_selection.db", echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class ImageSelection(Base):
    __tablename__ = 'imageselection'
    id = Column(Integer, primary_key=True)
    image1_path = Column(String)
    image2_path = Column(String)
    selected_image_path = Column(String)


Base.metadata.create_all(engine)


def store_selection(image1_path: str, image2_path: str, selected_image_path: str):
    with Session() as session:
        selection = ImageSelection(image1_path=image1_path, image2_path=image2_path, selected_image_path=selected_image_path)
        session.add(selection)
        session.commit()

st.title("Image Comparison")

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
