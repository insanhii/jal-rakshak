import json
import os
import time
import uuid
from decimal import Decimal

import boto3

# LocalStack par chalne ke liye AWS_ENDPOINT_URL set hota hai.
# Real AWS par ye set nahi hota, to code bina badlaav ke wahan bhi chalega.
ENDPOINT = os.environ.get("AWS_ENDPOINT_URL")
REGION = os.environ.get("AWS_REGION", "ap-south-1")
TABLE_NAME = os.environ.get("TABLE_NAME", "JalRakshakIncidents")
TOPIC_ARN = os.environ.get("ALERTS_TOPIC_ARN", "")

dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
sns = boto3.client("sns", endpoint_url=ENDPOINT, region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    "Access-Control-Allow-Headers": "Content-Type",
}


def _json_default(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError


def _resp(code, body):
    return {"statusCode": code, "headers": HEADERS,
            "body": json.dumps(body, default=_json_default)}


def handler(event, context):
    method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    if method == "OPTIONS":
        return _resp(200, {"status": "OK"})

    if method == "GET" and "/hotspots" in path:
        items = table.scan().get("Items", [])
        return _resp(200, {"status": "success", "count": len(items), "data": items})

    if method == "POST" and "/report" in path:
        try:
            body = json.loads(event.get("body") or "{}")
            severity = body.get("severity", "Moderate")
            incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"

            # Rule-based risk score (Bedrock ka placeholder)
            score = 85 if severity == "Severe" else 45
            action = ("Dispatch suction tankers & alert commuters"
                      if severity == "Severe" else "Monitor drain flow")

            item = {
                "incidentId": incident_id,
                "name": body.get("location", "Unknown"),
                "depth": body.get("depth", "1.0 ft"),
                "severity": severity,
                "status": "Reported",
                "lat": Decimal(str(body.get("lat", 28.6139))),
                "lng": Decimal(str(body.get("lng", 77.2090))),
                "riskScore": score,
                "timestamp": int(time.time()),
            }
            table.put_item(Item=item)

            notified = False
            if severity == "Severe" and TOPIC_ARN:
                sns.publish(TopicArn=TOPIC_ARN,
                            Subject="JalRakshak Severe Waterlogging",
                            Message=f"{item['name']} - depth {item['depth']}. {action}")
                notified = True

            return _resp(201, {
                "status": "created", "incidentId": incident_id,
                "location": item["name"], "severity": severity,
                "riskScore": score, "actionRecommended": action,
                "snsNotificationDispatched": notified,
                "timestamp": item["timestamp"],
            })
        except Exception as err:
            return _resp(400, {"error": str(err)})

    return _resp(404, {"message": "Endpoint not found"})