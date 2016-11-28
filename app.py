import os, subprocess
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

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
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('failure.html')
        f = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if f.filename == '' or not allowed_file(f.filename):
            return render_template('failure.html')

        secure = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure)
        f.save(path)
        result = subprocess.call([app.config['SCRIPT'], path, app.config['FILTER'], os.path.join(app.config['OUT_FOLDER'], secure)])
        if result:
            flash("Invalid image :(", "Error")
            return render_template('home.html')
        return render_template(send_from_directory(directory=app.config['OUT_FOLDER'], filename=secure)
    return render_template('home.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
