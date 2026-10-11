# JalRakshak: Hyperlocal Flood & Waterlogging Sentinel
### Bharat Builds Tour (Track 02: Heat and Water)
**Team:** TURIYA (Ansh Devkate, Om Kodilkar)

---

## 1. Problem Statement
Every monsoon season across Indian metros, unpredictable flash waterlogging paralyzes transit:
- Commuters unknowingly drive into submerged underpasses (e.g. Minto Bridge, Pul Prahladpur), leading to stalled engines and dangerous drownings.
- Municipal pump units get delayed reports without depth and priority classification.
- Existing map navigators (like Google Maps) alert for general traffic, but cannot tell if water depth is 0.5 ft (passable) or 3.5 ft (deadly).

---

## 2. Our Solution: JalRakshak
**JalRakshak** is a community-driven and sensor-backed flood early warning system that delivers:
1. **Live Waterlog Sentinel Map:** Shows exact water depth and danger zones with animated pulse indicators.
2. **AI Safe Navigation Assistant:** Calculates alternative routes specifically bypassing flooded underpasses and water traps.
3. **AWS Bedrock Flood Copilot:** Natural language assistant answering questions regarding safe roads, emergency rescue contacts, and civic actions.
4. **Instant Crowdsource & CV verification:** Citizens submit real-time reports with photo geotags.

---

## 3. AWS Architecture & Tools Used
JalRakshak fulfills the Bharat Builds Tour criteria by leveraging AWS serverless and AI services:

- **AWS Lambda & API Gateway:** Serverless ingestion microservice handling incoming incident reports without infrastructure overhead.
- **Amazon DynamoDB:** Sub-millisecond queries for geotagged flood markers (`JalRakshakIncidents` table).
- **Amazon S3:** High-durability cloud storage for user-submitted street flood images.
- **Amazon Rekognition / Bedrock (AI):** Multi-modal image analysis to gauge water depth against tire rims + automated LLM flood advisory.
- **Amazon SNS / SQS:** Pub/Sub alert pipeline that triggers automated SOS dispatches to municipal ward authorities.
- **AWS SAM (Serverless Application Model):** Infrastructure as Code (`template.yaml`) for 1-click cloud deployment.

---

## 4. How to Run Locally
1. Simply open `index.html` in any web browser.
2. Or serve it via Python:
   ```bash
   python -m http.server 8000
   ```
3. Visit `http://localhost:8000`.

---

## 5. Demo Video 3-Minute Script (Ready for Recording)
- **0:00 - 0:30 (Hook & Problem):** "Every monsoon, hundreds of commuters get trapped in flooded underpasses, and municipal teams react too late."
- **0:30 - 1:30 (Live Demo):** Walk through the interactive map, show live severity badges, submit a simulated flood report, and run the Safe Route Finder.
- **1:30 - 2:30 (AWS Tech Stack):** Explain the SAM template, Lambda handler, S3 photo upload pipeline, DynamoDB indexing, and Bedrock AI Copilot.
- **2:30 - 3:00 (Impact & Wrap Up):** "JalRakshak saves lives, protects vehicles, and gives cities real-time flood resilience. Thank you!"
