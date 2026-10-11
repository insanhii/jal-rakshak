import json
import os
import time
import uuid

# AWS Lambda Handler for JalRakshak API
def handler(event, context):
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }

    # Handle CORS Preflight
    if http_method == 'OPTIONS':
        return {"statusCode": 200, "headers": headers, "body": json.dumps({"status": "OK"})}

    if http_method == 'GET' and '/hotspots' in path:
        # Sample response representing DynamoDB query
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "status": "success",
                "count": 5,
                "data": [
                    {
                        "incidentId": "INC-001",
                        "name": "Minto Bridge Underpass",
                        "depth": "3.8 ft",
                        "severity": "Severe",
                        "status": "Pumps Deployed",
                        "lat": 28.6366,
                        "lng": 77.2255
                    },
                    {
                        "incidentId": "INC-002",
                        "name": "Pul Prahladpur Underpass",
                        "depth": "3.2 ft",
                        "severity": "Severe",
                        "status": "Road Diverted",
                        "lat": 28.5085,
                        "lng": 77.2917
                    }
                ]
            })
        }

    elif http_method == 'POST' and '/report' in path:
        try:
            body = json.loads(event.get('body', '{}'))
            location = body.get('location', 'Unknown')
            depth = body.get('depth', '1.0 ft')
            severity = body.get('severity', 'Moderate')

            incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"

            # Simulated AWS Bedrock Risk assessment
            ai_risk_score = 85 if severity == 'Severe' else 45
            action_recommended = "Dispatch suction tankers & alert commuters" if severity == 'Severe' else "Monitor drain flow"

            return {
                "statusCode": 201,
                "headers": headers,
                "body": json.dumps({
                    "status": "created",
                    "incidentId": incident_id,
                    "location": location,
                    "severity": severity,
                    "bedrockRiskScore": ai_risk_score,
                    "actionRecommended": action_recommended,
                    "snsNotificationDispatched": True,
                    "timestamp": int(time.time())
                })
            }
        except Exception as err:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": str(err)})
            }

    return {
        "statusCode": 404,
        "headers": headers,
        "body": json.dumps({"message": "Endpoint not found"})
    }
