from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import ssl

app = Flask(__name__)

# HiveMQ Cloud connection details
MQTT_BROKER = "efff4f0d50144b6d92ab49737f0971b7.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "fingerprint/cmd"
MQTT_USERNAME = "Test35" # Replace with your HiveMQ username
MQTT_PASSWORD = "Ab123456" # Replace with your HiveMQ password

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Enable TLS for HiveMQ Cloud
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud Broker")
    else:
        print(f"❌ Connection failed with code {rc}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.route("/fingerprint", methods=["POST"])
def fingerprint():
    try:
        data = request.json
        if not data or "cmd" not in data or "id" not in data:
            return jsonify({"status": "error", "message": "Invalid JSON payload. 'cmd' and 'id' are required."}), 400
            
        cmd = data.get("cmd")
        fid = data.get("id")
        
        message = f"{cmd},{fid}"
        client.publish(MQTT_TOPIC, message)
        
        print(f"Published message: {message} to topic: {MQTT_TOPIC}")
        
        return jsonify({"status": "success", "message": "MQTT message published successfully"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": "An internal server error occurred"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
