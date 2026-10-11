import os

os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_REGION"] = "ap-south-1"
os.environ["TABLE_NAME"] = "JalRakshakIncidents"
os.environ["ALERTS_TOPIC_ARN"] = "arn:aws:sns:ap-south-1:000000000000:JalRakshak-SevereWaterlog-Alerts"

from flask import Flask, request
from flask_cors import CORS
import lambda_handler

app = Flask(__name__)
CORS(app)


def invoke(path):
    event = {"httpMethod": request.method, "path": path,
             "body": request.get_data(as_text=True)}
    r = lambda_handler.handler(event, None)
    return r["body"], r["statusCode"], {"Content-Type": "application/json"}


@app.route("/hotspots", methods=["GET", "OPTIONS"])
def hotspots():
    return invoke("/hotspots")


@app.route("/report", methods=["POST", "OPTIONS"])
def report():
    return invoke("/report")


if __name__ == "__main__":
    app.run(port=5000)