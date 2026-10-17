import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PAGE = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CyberLab</title>
</head>
<body>
    <h2>CyberLab — مختبر أمن الويب</h2>
    <p>اختاري ملفاً تجريبياً لإرساله إلى الخادم.</p>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">إرسال الملف</button>
    </form>
    <p>{{ message }}</p>
    <small>الحد الأقصى للملف 10 ميغابايت.</small>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        uploaded = request.files.get("file")

        if uploaded and uploaded.filename:
            original_name = secure_filename(uploaded.filename)

            if not original_name:
                return "اسم الملف غير صالح", 400

            saved_name = f"{uuid4().hex}_{original_name}"
            uploaded.save(UPLOAD_DIR / saved_name)
            message = "نجح رفع الملف إلى الخادم."

    return render_template_string(PAGE, message=message)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)