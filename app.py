ALLOWED_IMAGE_TYPES = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

def allowed_image(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_IMAGE_TYPES
    )
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract
import os
import zipfile
import qrcode

from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
COMPRESSED_FOLDER = "compressed"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# TOOL PAGES
# =========================

@app.route("/compress-page")
def compress_page():
    return render_template("compress.html")

@app.route("/watermark-page")
def watermark_page():
    return render_template("watermark.html")


@app.route("/unlock-pdf-page")
def unlock_pdf_page():
    return render_template("unlock_pdf.html")

@app.route("/unlock-pdf", methods=["POST"])
def unlock_pdf():

    file = request.files["pdf"]

    password = request.form["password"]

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(pdf_path)

    reader = PdfReader(pdf_path)

    if reader.is_encrypted:

        result = reader.decrypt(password)

        if result == 0:
            return "Incorrect PDF password"

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "unlocked.pdf"
    )

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return send_file(
        output_path,
        as_attachment=True,
        download_name="unlocked.pdf"
    )




@app.route("/protect-pdf-page")
def protect_pdf_page():
    return render_template("protect_pdf.html")

@app.route("/rotate-pdf-page")
def rotate_pdf_page():
    return render_template("rotate_pdf.html")

@app.route("/rotate-pdf", methods=["POST"])
def rotate_pdf():

    file = request.files["pdf"]

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(pdf_path)

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    for page in reader.pages:

        page.rotate(90)

        writer.add_page(page)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "rotated.pdf"
    )

    with open(output_path, "wb") as output_file:

        writer.write(output_file)

    return send_file(
        output_path,
        as_attachment=True
    )


@app.route("/crop-image-page")
def crop_image_page():
    return render_template("crop_image.html")

@app.route("/crop-image", methods=["POST"])
def crop_image():

    file = request.files["image"]

    left = int(request.form["left"])
    top = int(request.form["top"])
    right = int(request.form["right"])
    bottom = int(request.form["bottom"])

    img = Image.open(file)

    cropped = img.crop((left, top, right, bottom))

    output = BytesIO()
    cropped.save(output, format="PNG")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="cropped_image.png",
        mimetype="image/png"
    )


@app.route("/qr-generator-page")
def qr_generator_page():
    return render_template("qr_generator.html")

# =========================
# MERGE PDF FUNCTION
# =========================

# =========================
# MERGE PDF FUNCTION
# =========================

@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():

    files = request.files.getlist("pdfs")

    merger = PdfMerger()

    for file in files:

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        merger.append(filepath)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "merged.pdf"
    )

    merger.write(output_path)

    merger.close()

    return send_file(
        output_path,
        as_attachment=True
    )
@app.route("/image-to-pdf-page")
def image_to_pdf_page():
    return render_template("image_to_pdf.html")


@app.route("/merge-pdf-page")
def merge_pdf_page():
    return render_template("merge_pdf.html")


@app.route("/pdf-to-images-page")
def pdf_to_images_page():
    return render_template("pdf_to_images.html")


@app.route("/resize-page")
def resize_page():
    return render_template("resize.html")


# =========================
# IMAGE COMPRESSOR
# =========================

@app.route("/generate-qr", methods=["POST"])
def generate_qr():

    text = request.form.get("qr_text")

    qr = qrcode.make(text)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "qr_code.png"
    )

    qr.save(output_path)

    return send_file(
        output_path,
        as_attachment=True
    )
@app.route("/add-watermark", methods=["POST"])
def add_watermark():

    file = request.files["image"]

    watermark_text = request.form.get("watermark")

    input_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(input_path)

    image = Image.open(input_path)

    draw = ImageDraw.Draw(image)

    width, height = image.size

    font = ImageFont.load_default()

    draw.text(
        (width // 3, height // 2),
        watermark_text,
        fill=(255, 255, 255),
        font=font
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "watermarked.png"
    )

    image.save(output_path)

    return send_file(
        output_path,
        as_attachment=True
    )
@app.route("/compress", methods=["POST"])
def compress_image():

    file = request.files["image"]
    quality = int(
    request.form.get(
        "quality",
        80
    )
)

    input_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(input_path)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "compressed.jpg"
    )

    img = Image.open(input_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(
        output_path,
        "JPEG",
        optimize=True,
        quality=quality
)

    return send_file(
        output_path,
        as_attachment=True
    )


# =========================
# IMAGE TO PDF
# =========================

@app.route("/image-to-pdf", methods=["POST"])
def image_to_pdf():

    files = request.files.getlist("images")

    images = []

    for file in files:

        path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(path)

        img = Image.open(path).convert("RGB")

        images.append(img)

    pdf_path = os.path.join(
        OUTPUT_FOLDER,
        "converted.pdf"
    )

    images[0].save(
        pdf_path,
        save_all=True,
        append_images=images[1:]
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )


# =========================
# MERGE PDFs
# =========================

# =========================
# PDF TO IMAGES
# =========================

@app.route("/pdf-to-images", methods=["POST"])
def pdf_to_images():

    file = request.files["pdf"]

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(pdf_path)

    images = convert_from_path(pdf_path)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w"
    ) as zipf:

        for i, image in enumerate(images):

            img_path = os.path.join(
                OUTPUT_FOLDER,
                f"page_{i+1}.jpg"
            )

            image.save(img_path, "JPEG")

            zipf.write(
                img_path,
                os.path.basename(img_path)
            )

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="pdf_images.zip",
        mimetype="application/zip"
    )


# =========================
# OCR TEXT EXTRACTION
# =========================
@app.route("/extract-text-page")
def extract_text_page():
    return render_template("extract_text.html")

@app.route("/extract-text", methods=["POST"])
def extract_text():

    file = request.files["image"]

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    text = pytesseract.image_to_string(
        Image.open(path)
    )

    return f"""
    <body style='background:#020617;
    color:white;
    font-family:Arial;
    padding:40px;'>

    <h1>Extracted Text</h1>

    <pre style='font-size:18px;
    white-space:pre-wrap;'>

{text}

    </pre>

    </body>
    """


# =========================
# RESIZE IMAGE
# =========================

@app.route("/resize-image", methods=["POST"])
def resize_image():

    file = request.files["image"]

    width = int(request.form.get("width"))

    height = int(request.form.get("height"))

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    img = Image.open(path)

    resized = img.resize((width, height))

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "resized.png"
    )

    resized.save(output_path)

    return send_file(
        output_path,
        as_attachment=True
    )


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)