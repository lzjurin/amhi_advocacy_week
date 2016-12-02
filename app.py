import os, subprocess
from flask import Flask, flash, render_template, request, redirect, url_for, send_file, Response
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags

app = Flask(__name__)
app.debug=True

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUT_FOLDER'] = 'out'
app.config['FILTER'] = 'filters/filter_3.png'
app.config['SCRIPT'] = 'scripts/overlay'
app.secret_key ='asdlkjfho2837hlfbvhzv8o7n3af'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No image uploaded", "Error")
            return render_template("home.html.jinja")
        f = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if f.filename == '' or not allowed_file(f.filename):
            flash("File type not allowed", "Error")
            return render_template("home.html.jinja")

        secure = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure)
        f.save(path)
        if request.user_agent.platform == 'iphone':# or request.user_agent.platform == 'android':
            try:
                image = Image.open(path)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation]=='Orientation':
                        break
                exif=dict(image._getexif().items())

                if exif[orientation] == 3:
                    image=image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image=image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image=image.rotate(90, expand=True)
                image.save(path)
                image.close()

            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass
        result = subprocess.call([app.config['SCRIPT'], path, app.config['FILTER'], os.path.join(app.config['OUT_FOLDER'], secure)])

        if result:
            flash("Image overlaying failed, probably because your image dimensions aren't at least 1000x1000", "Error")
            return render_template("home.html.jinja")

        return send_file(os.path.join(app.config['OUT_FOLDER'], secure), attachment_filename=secure, as_attachment=True)
    return render_template("home.html.jinja")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
