# ReadQR — Bill QR Scanner

This small Streamlit app accepts a photo of a bill (upload or camera) and decodes any QR codes inside, extracting URLs and logging them.

Quick start (Debian):

1. Install system dependency:

```bash
sudo apt update
sudo apt install -y libzbar0
```

2. Create a virtualenv and install Python deps:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

Open the Streamlit URL in a browser on another machine and upload or capture a photo.

Logs are appended to `data/decoded_links.csv` and `data/decoded_links.jsonl`.
