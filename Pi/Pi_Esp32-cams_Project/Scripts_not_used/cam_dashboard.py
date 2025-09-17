from flask import Flask, render_template_string

app = Flask(__name__)

CAM_IP = "192.168.4.2"  # Replace with your ESP32-CAM's IP

@app.route("/")
def index():
    html = f'''
<h1>ESP32-CAM Stream</h1>
<iframe src="http://{CAM_IP}/stream" width="640" height="480" frameborder="0"></iframe>
'''

    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
