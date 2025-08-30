# Hacktok

## Getting Started

Read individual README.md files for each "micro"-service.
You may run them locally or in docker.
Suggest to run each service manually for development.
Use `docker compose up` to run all services.

## Problem

- As TikTok operates in multiple regions around the world, ensuring every product feature complies with local laws and regulations is a constant challenge. Regulations like Brazil's data localization or the EU's GDPR demand that specific features be designed with geo-specific compliance logic. Without a clear and automated way to track this, we risk:
1. Legal exposure: Compliance gaps that go undetected until it's too late.
2. Reactive firefighting: Scrambling to address compliance issues when auditors or regulators come calling.
3. Operational inefficiency: Overloading teams with manual checks and rework to ensure features are compliant in every region.

To address this, a solution that can dynamically flag features requiring geo-specific compliance logic is needed. We need the ability to quickly answer critical questions such as:
- "Does this feature need dedicated logic for region-specific compliance?"
- "How many features have we rolled out that comply with this regulation?"
  
Without this automated, traceable, and auditable system in place, scaling global product features while staying compliant becomes increasingly difficult and risky.

## Our Solution

![Architecture Diagram](./assets/architecture.png)

1. We have a knowledge base on all existing regulations.
2. This knowledge base is "smart" and will auto update itself when new regulations are published.
3. It can be a system that checks for new regulations every single day, or even down to every hour depending on computing resources.
4. When the knowledge base is updated, it will check against existing features and flag out features that need attention (assuming with the new regulation now the feature is not compliant)
5. Similarly, when we are deploying a new feature, we can mock it in the system, and with the knowledge base, it will flag out any potential regulatory conflicts.

6. As for the demo, we can have the knowledge base collect regulatory information from a nation called Hacktok.
7. In Hacktok, we can release a new regulation such as setting social media curfew.
8. We can see that based on this new regulation, can our knowledge base properly detect this new regulation, and flag out (perhaps by notifying) the feature that needs modification.

## Architecture

- **Frontend**: Next.js
- **Backend**: FastAPI
- **Database**: MongoDB
- **N8N**: Workflow automation
- **Docker**: Containerization

### System Integration

- N8N will be our automated knowledge base updater/webscraper
- Backend is for all the business logic
- Frontend for interfacing

We will implement webhooks for N8N to communicate with the BE.
FE will be connected to BE via SSE for real-time updates.

Everything will be dockerised except for MongoDB.
Docker-compose to orchestrate the deployment (volumes and networking etc).
