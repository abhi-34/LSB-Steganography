import streamlit as st
from PIL import Image
import io
import time

# ------------------------ Functions ------------------------
def encode_image(image, secret_msg):
    encoded = image.copy()
    width, height = image.size
    pixels = encoded.load()

    secret_msg += "###"
    binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg)
    msg_index = 0

    for y in range(height):
        for x in range(width):
            if msg_index < len(binary_msg):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_msg[msg_index])
                msg_index += 1
                pixels[x, y] = (r, g, b)
            else:
                return encoded
    return encoded


def decode_image(image):
    binary_data = ""
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ""
    for byte in all_bytes:
        decoded += chr(int(byte, 2))
        if decoded.endswith("###"):
            return decoded[:-3]
    return "No hidden message found."


# ------------------------ Page Config ------------------------
st.set_page_config(page_title="Cyber Steganography", layout="centered")

# ------------------------ Custom Styling ------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    .stApp {
        background: linear-gradient(135deg, #0E0E10 0%, #1A1B1E 100%);
    }

    .main {
        background: rgba(30, 30, 32, 0.85);
        padding: 2.5rem;
        border-radius: 18px;
        text-align: center;
        border: 1px solid #2C2C2E;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.4);
    }

    h1, h2, h3 {
        color: #F1F1F1;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C2C2E 0%, #1A1A1C 100%);
        color: #E0E0E0;
        border-right: 1px solid #333;
    }

    .stButton>button, .stDownloadButton>button {
        background: #2F2F31;
        border: 1px solid #444;
        color: #EAEAEA;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: 0.2s ease-in-out;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #3B3B3E;
        border-color: #666;
    }

    textarea, input, .stTextInput>div>div>input {
        background-color: #1E1E20 !important;
        color: #EAEAEA !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
    }

    .stFileUploader {
        background: rgba(50, 50, 52, 0.5);
        border-radius: 10px;
        padding: 1rem;
    }

    pre {
        background-color: #1E1E20 !important;
        border-radius: 8px;
        padding: 1rem;
        color: #EAEAEA;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------ Header ------------------------
st.markdown("<div class='main'><h1>Cyber Steganography</h1><p>Hide and reveal messages within images using LSB encoding.</p></div>", unsafe_allow_html=True)

# ------------------------ Sidebar ------------------------
st.sidebar.markdown("### Controls")
st.sidebar.write("Choose a mode to begin encoding or decoding your message securely.")
menu = st.sidebar.radio("Navigation", ["Encode Message", "Decode Message"])

# Initialize state keys
for key in ["uploaded_image_bytes", "uploaded_image_name", "encoded_image_bytes"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ------------------------ Encode Section ------------------------
if menu == "Encode Message":
    st.header("Encode a Secret Message")

    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="encode")

    # persist bytes on upload
    if uploaded is not None:
        uploaded_bytes = uploaded.getvalue()
        if uploaded_bytes and uploaded.name != st.session_state["uploaded_image_name"]:
            st.session_state["uploaded_image_bytes"] = uploaded_bytes
            st.session_state["uploaded_image_name"] = uploaded.name
            st.session_state["encoded_image_bytes"] = None

    image = None
    if st.session_state["uploaded_image_bytes"]:
        try:
            image = Image.open(io.BytesIO(st.session_state["uploaded_image_bytes"])).convert("RGB")
            st.image(image, caption="Uploaded Image Preview", use_container_width=True)
        except Exception:
            st.error("Failed to load uploaded image.")

    if image:
        width, height = image.size
        capacity_bits = width * height
        max_chars = max((capacity_bits // 8) - 3, 0)
        st.markdown(f"*Image capacity:* **{max_chars}** characters (approx)")

    secret_msg = st.text_area("Enter your secret message:", key="secret_msg_text")

    # --- Encode button ---
    if st.button("Encode Message", key="encode_btn"):
        if image is None:
            st.error("Please upload an image before encoding.")
        elif not secret_msg:
            st.error("Please enter a secret message to encode.")
        elif len(secret_msg) > max_chars and max_chars > 0:
            st.error(f"Message too long for this image. Max {max_chars} chars.")
        else:
            with st.spinner("Encoding message..."):
                time.sleep(0.8)
                result = encode_image(image, secret_msg)
                buf = io.BytesIO()
                result.save(buf, format="PNG")
                buf.seek(0)
                st.session_state["encoded_image_bytes"] = buf.getvalue()
                st.success("Message encoded successfully!")

    # --- Show single preview of encoded image if available ---
    if st.session_state["encoded_image_bytes"]:
        encoded_preview = Image.open(io.BytesIO(st.session_state["encoded_image_bytes"]))
        st.image(encoded_preview, caption="Encoded Image", use_container_width=True)
        st.download_button("Download Encoded Image", st.session_state["encoded_image_bytes"],
                           "encoded.png", "image/png", key="download_btn")

# ------------------------ Decode Section ------------------------
elif menu == "Decode Message":
    st.header("Decode a Hidden Message")
    uploaded_dec = st.file_uploader("Upload encoded image", type=["png", "jpg", "jpeg"], key="decode")

    img_dec = None
    if uploaded_dec is not None:
        try:
            img_dec = Image.open(uploaded_dec).convert("RGB")
            st.image(img_dec, caption="Uploaded Encoded Image", use_container_width=True)
        except Exception:
            st.error("Failed to load uploaded image.")

    if st.button("Decode Message"):
        if img_dec is None:
            st.error("Please upload an encoded image first.")
        else:
            with st.spinner("Decoding hidden message..."):
                time.sleep(0.8)
                decoded_msg = decode_image(img_dec)
                st.success("Hidden Message Found:")
                st.code(decoded_msg)
