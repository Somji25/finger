from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = "10.215.102.95"
MQTT_PORT = 1883
MQTT_TOPIC = "fingerprint/cmd"

client = mqtt.Client()
client.username_pw_set("egatgo", "1234561")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

@app.route("/fingerprint", methods=["POST"])
def fingerprint():
    data = request.json
    cmd = data.get("cmd")
    fid = data.get("id")
    message = f"{cmd},{fid}"
    client.publish(MQTT_TOPIC, message)
    return jsonify({"status": "ok", "sent": message})

if __name__ == "__main__":
    app.run(debug=True)