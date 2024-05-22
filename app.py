from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)


def generate_qr_code(data, fill_color='black', back_color='white'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img


@app.route("/", methods=["GET", "POST"])
def index():
    img_data = None
    if request.method == "POST":
        data = request.form["data"]
        fill_color = request.form.get("fill_color", "black")
        back_color = request.form.get("back_color", "white")

        img = generate_qr_code(data, fill_color, back_color)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_data = base64.b64encode(img_io.getvalue()).decode('ascii')

    return render_template("index.html", img_data=img_data)


if __name__ == "__main__":
    app.run(debug=True)
