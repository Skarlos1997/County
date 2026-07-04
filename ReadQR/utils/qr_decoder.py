import io
from typing import List

from PIL import Image

try:
    from pyzbar.pyzbar import decode as zbar_decode
except Exception:
    zbar_decode = None


def decode_qr(image_bytes: bytes) -> List[str]:
    """Decode QR codes from image bytes and return list of decoded strings.

    Returns an empty list when nothing is found. Depends on `pyzbar` (zbar).
    """
    if zbar_decode is None:
        raise RuntimeError("pyzbar is not available. Install pyzbar and libzbar0 on Debian.")

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        # Try to handle when callers pass a file-like object
        if hasattr(image_bytes, "read"):
            img = Image.open(image_bytes).convert("RGB")
        else:
            raise

    decoded = zbar_decode(img)
    results = []
    for d in decoded:
        try:
            s = d.data.decode("utf-8")
        except Exception:
            s = d.data.decode(errors="ignore")
        results.append(s)

    # return unique preserving order
    seen = set()
    uniq = []
    for r in results:
        if r not in seen:
            uniq.append(r)
            seen.add(r)

    return uniq
