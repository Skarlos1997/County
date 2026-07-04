import io
from PIL import Image

from utils.qr_decoder import decode_qr


def test_decode_empty_image_returns_empty_list():
    # create a blank white image
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    results = decode_qr(buf.getvalue())
    assert isinstance(results, list)
    assert results == []
