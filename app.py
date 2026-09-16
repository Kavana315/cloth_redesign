import os
import json
import numpy as np
import streamlit as st
from PIL import Image
import tensorflow as tf

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Old Cloth Redesign Assistant",
    page_icon="👕",
    layout="wide"
)

# ============================================================
# CONSTANTS
# ============================================================
IMG_SIZE = 224
url="https://drive.google.com/file/d/1qJfZm_EpptB_meVZdLK4HpSV5jylTYgW/view?usp=sharing"
MODEL_PATH = "cloth_classifier.keras"
CLASS_NAMES_PATH = "class_names.json"
ASSETS_DIR = "assets"

# ============================================================
# REDESIGN IDEAS + IMAGE MAPPING
# ============================================================
REDESIGN_IDEAS = {
    "Tshirt": [
        {"title": "Tote Bag", "difficulty": "Easy", "time": "30 min",
         "image": "Tshirt_tote_bag.jpg",
         "materials": ["Thread", "Needle", "Scissors"],
         "steps": [
             "Cut off sleeves and neckline.",
             "Turn inside out and stitch the bottom closed.",
             "Cut two strips from sleeves for handles.",
             "Attach handles to the top edge."]},
        {"title": "Cushion Cover", "difficulty": "Easy", "time": "20 min",
         "image": "Tshirt_cushion_cover.jpg",
         "materials": ["Thread", "Needle", "Cushion insert"],
         "steps": [
             "Cut the T-shirt into two equal squares.",
             "Place right sides together and stitch 3 edges.",
             "Turn inside out and insert cushion.",
             "Hand-stitch the final edge."]},
        {"title": "Cleaning Cloths", "difficulty": "Very Easy", "time": "5 min",
         "image": "Tshirt_cleaning_cloths.jpg",
         "materials": ["Scissors"],
         "steps": [
             "Cut the T-shirt into 6 equal squares.",
             "Use directly as dust cloths."]}
    ],
    "Shirt": [
        {"title": "Apron", "difficulty": "Medium", "time": "45 min",
         "image": "Shirt_apron.jpg",
         "materials": ["Thread", "Needle", "Ribbon"],
         "steps": [
             "Cut the shirt open at the back.",
             "Remove sleeves and collar.",
             "Hem all raw edges.",
             "Attach ribbon ties at waist level."]},
        {"title": "Pillow Cover", "difficulty": "Easy", "time": "30 min",
         "image": "Shirt_pillow_cover.jpg",
         "materials": ["Thread", "Needle", "Buttons"],
         "steps": [
             "Cut front and back panels to pillow size.",
             "Stitch right sides together on 3 edges.",
             "Add buttons to the open edge.",
             "Turn inside out and insert pillow."]},
        {"title": "Patchwork Quilt", "difficulty": "Hard", "time": "3 hours",
         "image": "Shirt_patchwork_quilt.jpg",
         "materials": ["Thread", "Batting", "Backing fabric"],
         "steps": [
             "Cut shirt into equal squares.",
             "Arrange squares into a pattern.",
             "Stitch squares into rows, then rows together.",
             "Layer with batting and backing, quilt together."]}
    ],
    "Jeans": [
        {"title": "Denim Tote Bag", "difficulty": "Medium", "time": "1 hour",
         "image": "Jeans_denim_tote_bag.jpg",
         "materials": ["Thread", "Needle", "Ribbon"],
         "steps": [
             "Cut off the legs at the crotch.",
             "Stitch the bottom closed.",
             "Use leg fabric for handles.",
             "Attach handles securely."]},
        {"title": "Denim Shorts", "difficulty": "Easy", "time": "20 min",
         "image": "Jeans_denim_shorts.jpg",
         "materials": ["Scissors", "Needle", "Thread"],
         "steps": [
             "Mark desired length.",
             "Cut off the legs below the mark.",
             "Fold and hem the raw edges.",
             "Add distress if desired."]},
        {"title": "Pouch or Pencil Case", "difficulty": "Easy", "time": "25 min",
         "image": "Jeans_pouch_or_pencil_case.jpg",
         "materials": ["Thread", "Zipper"],
         "steps": [
             "Cut a rectangle from the leg.",
             "Fold in half, stitch sides.",
             "Attach zipper at the top.",
             "Turn inside out."]}
    ],
    "Dress": [
        {"title": "Skirt", "difficulty": "Medium", "time": "45 min",
         "image": "Dress_skirt.jpg",
         "materials": ["Thread", "Elastic"],
         "steps": [
             "Cut the dress at the waist.",
             "Create a casing for elastic at the top.",
             "Insert elastic and stitch closed.",
             "Hem the bottom."]},
        {"title": "Scarf", "difficulty": "Very Easy", "time": "10 min",
         "image": "Dress_scarf.jpg",
         "materials": ["Scissors"],
         "steps": [
             "Cut the dress into long strips.",
             "Sew strips end-to-end.",
             "Hem all edges."]},
        {"title": "Fabric Coasters", "difficulty": "Easy", "time": "20 min",
         "image": "Dress_fabric_coasters.jpg",
         "materials": ["Thread", "Needle"],
         "steps": [
             "Cut 8 circles of equal size.",
             "Pair circles right sides together.",
             "Stitch around, leaving a small gap.",
             "Turn inside out and close the gap."]}
    ],
    "Jacket": [
        {"title": "Backpack", "difficulty": "Hard", "time": "2 hours",
         "image": "Jacket_backpack.jpg",
         "materials": ["Thread", "Straps", "Zipper"],
         "steps": [
             "Cut the jacket at the waist.",
             "Stitch bottom closed.",
             "Attach straps at the back.",
             "Add a zipper at the top."]},
        {"title": "Laptop Sleeve", "difficulty": "Medium", "time": "45 min",
         "image": "Jacket_laptop_sleeve.jpg",
         "materials": ["Thread", "Velcro", "Foam padding"],
         "steps": [
             "Measure your laptop and add 2 cm.",
             "Cut two panels from the jacket.",
             "Add foam padding between panels.",
             "Stitch 3 sides and add Velcro closure."]},
        {"title": "Vest", "difficulty": "Medium", "time": "1 hour",
         "image": "Jacket_vest.jpg",
         "materials": ["Thread", "Needle"],
         "steps": [
             "Cut off the sleeves.",
             "Hem the armholes.",
             "Adjust the fit if needed.",
             "Add buttons or keep open."]}
    ]
}

# ============================================================
# LOAD MODEL + CLASS NAMES (cached)
# ============================================================
@st.cache_resource(show_spinner=False)
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_data(show_spinner=False)
def load_class_names():
    if not os.path.exists(CLASS_NAMES_PATH):
        return None
    with open(CLASS_NAMES_PATH, "r") as f:
        return json.load(f)

# ============================================================
# HEADER
# ============================================================
st.title("👕 Old Cloth Redesign Assistant")
st.caption("Upload a photo of your old clothing — get redesign ideas with visual previews powered by AI.")

# ============================================================
# LOAD RESOURCES
# ============================================================
model = load_model()
class_names = load_class_names()

if model is None or class_names is None:
    st.error("⚠️ Model files not found. Make sure `cloth_classifier.keras` "
             "and `class_names.json` are in the same folder as `app.py`.")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("⚙️ Options")
    st.write("**Supported garment types:**")
    for name in class_names:
        st.write(f"• {name}")
    st.divider()
    st.write("**Tip:** Use a clear, well-lit photo of a single garment.")
    st.divider()
    st.caption("Capstone Project 2026")

# ============================================================
# UPLOAD SECTION
# ============================================================
uploaded_file = st.file_uploader(
    "📸 Upload an image of an old garment",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption="Your Uploaded Garment", use_container_width=True)

    # ---------- Predict ----------
    with st.spinner("Analyzing garment..."):
        img_resized = image.resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img_resized) / 255.0
        arr = np.expand_dims(arr, axis=0)

        preds = model.predict(arr, verbose=0)[0]
        top_idx = int(np.argmax(preds))
        predicted_class = class_names[top_idx]
        confidence = float(preds[top_idx]) * 100

    with col2:
        st.subheader("🔍 Prediction")
        st.success(f"**{predicted_class}**")
        st.metric("Confidence", f"{confidence:.1f}%")

        st.write("**Top predictions:**")
        for i in np.argsort(preds)[::-1][:3]:
            st.write(f"- {class_names[i]}: {preds[i]*100:.1f}%")

    st.divider()

    # ---------- Redesign Ideas with Visual Previews ----------
    st.subheader("💡 Redesign Ideas")
    st.write(f"Here's how your **{predicted_class}** could be transformed:")

    ideas = REDESIGN_IDEAS.get(predicted_class, [])

    if not ideas:
        st.info("No redesign suggestions available for this category.")
    else:
        for idea in ideas:
            with st.expander(
                f"✨ {idea['title']}  —  {idea['difficulty']}  •  {idea['time']}",
                expanded=False
            ):
                col_img, col_text = st.columns([1, 1.5])

                # ---------- Image Preview ----------
                with col_img:
                    img_path = os.path.join(ASSETS_DIR, idea["image"])
                    if os.path.exists(img_path):
                        st.image(
                            img_path,
                            caption=f"Preview: {idea['title']}",
                            use_container_width=True
                        )
                    else:
                        # Placeholder box if image is missing
                        st.info(
                            f"📷 Preview image not found.\n\n"
                            f"Expected: `assets/{idea['image']}`"
                        )

                # ---------- Instructions ----------
                with col_text:
                    st.write("**🧵 Materials needed:**")
                    for m in idea["materials"]:
                        st.write(f"- {m}")

                    st.write("**📝 Step-by-step guide:**")
                    for idx, step in enumerate(idea["steps"], 1):
                        st.write(f"{idx}. {step}")

    st.divider()

    # ---------- Environmental Impact ----------
    st.subheader("🌱 Environmental Impact")
    st.info(
        "By upcycling one garment instead of discarding it, you save approximately "
        "**2,700 liters of water** and reduce **~6 kg of CO₂ emissions** "
        "(source: UNEP). Every reused item counts!"
    )

else:
    st.info("👆 Upload an image to get started.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption(
    "Old Cloth Redesign Assistant • Capstone Project 2026 • "
    "Powered by TensorFlow & Streamlit"
)