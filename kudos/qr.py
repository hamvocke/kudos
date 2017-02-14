from io import BytesIO

import qrcode
from flask import url_for


def create_qr_code(feedback_id):
    img = qrcode.make(url_for('feedback', feedback_id=feedback_id, _external=True))
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    return img_io.getvalue()
