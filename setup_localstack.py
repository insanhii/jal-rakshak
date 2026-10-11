import boto3

cfg = dict(endpoint_url="http://localhost:4566", region_name="ap-south-1",
           aws_access_key_id="test", aws_secret_access_key="test")

dynamo = boto3.client("dynamodb", **cfg)
s3 = boto3.client("s3", **cfg)
sns = boto3.client("sns", **cfg)

try:
    dynamo.create_table(
        TableName="JalRakshakIncidents",
        BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[
            {"AttributeName": "incidentId", "AttributeType": "S"},
            {"AttributeName": "severity", "AttributeType": "S"},
        ],
        KeySchema=[{"AttributeName": "incidentId", "KeyType": "HASH"}],
        GlobalSecondaryIndexes=[{
            "IndexName": "SeverityIndex",
            "KeySchema": [{"AttributeName": "severity", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"},
        }],
    )
    print("Table created")
except dynamo.exceptions.ResourceInUseException:
    print("Table already exists")

try:
    s3.create_bucket(
        Bucket="jalrakshak-evidence-000000000000",
        CreateBucketConfiguration={"LocationConstraint": "ap-south-1"},
    )
    print("Bucket created")
except Exception as e:
    print("Bucket:", e)

topic = sns.create_topic(Name="JalRakshak-SevereWaterlog-Alerts")
print("Topic:", topic["TopicArn"])

# Seed data
items = [
    ("INC-001", "Minto Bridge Underpass", "3.8 ft", "Severe", "High-Capacity Pump Dispatched", "28.6366", "77.2255"),
    ("INC-002", "Pul Prahladpur Underpass", "3.2 ft", "Severe", "Barricaded by Police", "28.5085", "77.2917"),
    ("INC-003", "Zakhira Flyover Low Section", "1.8 ft", "Moderate", "Drain Clearance Crew Active", "28.6672", "77.1593"),
    ("INC-004", "ITO Ring Road Junction", "2.1 ft", "Moderate", "Suction Tanker On Site", "28.6289", "77.2494"),
    ("INC-005", "DTU Main Gate, Bawana Road", "0.6 ft", "Caution", "Monitored Clean", "28.7499", "77.1172"),
]
for i, n, d, s, st, la, ln in items:
    dynamo.put_item(TableName="JalRakshakIncidents", Item={
        "incidentId": {"S": i}, "name": {"S": n}, "depth": {"S": d},
        "severity": {"S": s}, "status": {"S": st},
        "lat": {"N": la}, "lng": {"N": ln}})
print("Seed data added")