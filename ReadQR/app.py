import os
import sys
import io
import csv
import json
from datetime import datetime

import streamlit as st

# Ensure `utils` package in path when running from this folder
HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.append(HERE)

from utils.qr_decoder import decode_qr


DATA_DIR = os.path.join(HERE, "data")
CSV_LOG = os.path.join(DATA_DIR, "decoded_links.csv")
JSONL_LOG = os.path.join(DATA_DIR, "decoded_links.jsonl")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "source", "filename", "url"])


def append_logs(source, filename, url):
    ts = datetime.utcnow().isoformat() + "Z"
    with open(CSV_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([ts, source, filename or "", url])

    with open(JSONL_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "source": source, "filename": filename, "url": url}) + "\n")


def copy_button_html(url: str) -> str:
    # simple button that uses Clipboard API
    safe_url = url.replace("'", "\\'")
    html = f"""
    <button onclick="navigator.clipboard.writeText('{safe_url}')">Copy</button>
    """
    return html


def process_image_file(uploaded, source_label="upload"):
    if uploaded is None:
        return []
    image_bytes = uploaded.read()
    results = []
    try:
        decoded = decode_qr(image_bytes)
    except Exception as e:
        st.error(f"Decoding failed: {e}")
        return []

    for url in decoded:
        append_logs(source_label, getattr(uploaded, "name", None), url)
        results.append(url)

    return results


def main():
    st.title("ReadQR — Bill QR Scanner")
    st.write("Upload a bill photo or use your camera to scan a QR code.")

    ensure_data_dir()

    uploaded = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg", "webp"])
    cam_image = st.camera_input("Or take a photo with your camera")

    results = []
    if uploaded is not None:
        results = process_image_file(uploaded, "upload")

    if cam_image is not None and (uploaded is None):
        results = process_image_file(cam_image, "camera")

    if results:
        st.success(f"Found {len(results)} QR result(s)")
        for url in results:
            st.markdown(f"[{url}]({url})")
            st.components.v1.html(copy_button_html(url), height=40)
    else:
        st.info("No QR codes detected yet.")


if __name__ == "__main__":
    main()
