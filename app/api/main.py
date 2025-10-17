from flask import Flask, request, send_file, render_template
from app.ml.model import generate_image
import io

app = Flask(__name__, static_folder='../static', template_folder='../templates')

@app.route('/healthz')
def healthz():
    return {"status": "ok"}, 200

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')
    if not prompt:
        return {"error": "Prompt not provided"}, 400

    image = generate_image(prompt)
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
