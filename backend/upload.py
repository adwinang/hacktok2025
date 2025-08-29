import requests

# API endpoint
API_URL = "http://localhost:5000/features"

# Feature data extracted from the document
features = [
    {
        "name": "Curfew login blocker with ASL and GH for Utah minors",
        "description": "To comply with the Utah Social Media Regulation Act, we are implementing a curfew-based login restriction for users under 18. The system uses ASL to detect minor accounts and routes enforcement through GH to apply only within Utah boundaries. The feature activates during restricted night hours and logs activity using EchoTrace for auditability. This allows parental control to be enacted without user-facing alerts, operating in ShadowMode during initial rollout."
    },
    {
        "name": "PF default toggle with NR enforcement for California teens",
        "description": "As part of compliance with California's SB976, the app will disable PF by default for users under 18 located in California. This default setting is considered NR to override, unless explicit parental opt-in is provided. Geo-detection is handled via GH, and rollout is monitored with FR logs. The design ensures minimal disruption while meeting the strict personalization requirements imposed by the law."
    },
    {
        "name": "Child abuse content scanner using T5 and CDS triggers",
        "description": "In line with the US federal law requiring providers to report child sexual abuse content to NCMEC, this feature scans uploads and flags suspected materials tagged as T5. Once flagged, the CDS auto-generates reports and routes them via secure channel APIs. The logic runs in real-time, supports human validation, and logs detection metadata for internal audits. Regional thresholds are governed by LCP parameters in the backend."
    },
    {
        "name": "Content visibility lock with NSP for EU DSA",
        "description": "To meet the transparency expectations of the EU Digital Services Act, we are introducing a visibility lock for flagged user-generated content labeled under NSP. When such content is detected, a soft Softblock is applied and GH ensures enforcement is restricted to the EU region only. EchoTrace supports traceability, and Redline status can be triggered for legal review. This feature enhances accountability and complies with Article 16's removal mechanisms."
    },
    {
        "name": "Jellybean-based parental notifications for Florida regulation",
        "description": "To support Florida's Online Protections for Minors law, this feature extends the Jellybean parental control framework. Notifications are dispatched to verified parent accounts when a minor attempts to access restricted features. Using IMT, the system checks behavioral anomalies against BB models. If violations are detected, restrictions are applied in ShadowMode with full audit logging through CDS. Glow flags ensure compliance visibility during rollout phases."
    },
    {
        "name": "Unified retention control via DRT & CDS",
        "description": "Introduce a data retention feature using DRT thresholds, ensuring automatic log deletion across all regions. CDS will continuously audit retention violations, triggering EchoTrace as necessary. Spanner logic ensures all platform modules comply uniformly."
    },
    {
        "name": "NSP auto-flagging",
        "description": "This feature will automatically detect and tag content that violates NSP policy. Once flagged, Softblock is applied and a Redline alert is generated if downstream sharing is attempted."
    },
    {
        "name": "T5 tagging for sensitive reports",
        "description": "When users report content containing high-risk information, it is tagged as T5 for internal routing. CDS then enforces escalation. The system is universal and does not rely on regional toggles or GH routes."
    },
    {
        "name": "Underage protection via Snowcap trigger",
        "description": "Snowcap is activated for all underage users platform-wide, applying ASL to segment accounts. Actions taken under this logic are routed to CDS and monitored using BB to identify deviations in usage."
    },
    {
        "name": "Universal PF deactivation on guest mode",
        "description": "By default, PF will be turned off for all uses browsing in guest mode."
    },
    {
        "name": "Story resharing with content expiry",
        "description": "Enable users to reshare stories from others, with auto-expiry after 48 hours. This feature logs resharing attempts with EchoTrace and stores activity under BB."
    },
    {
        "name": "Leaderboard system for weekly creators",
        "description": "Introduce a creator leaderboard updated weekly using internal analytics. Points and rankings are stored in FR metadata and tracked using IMT."
    },
    {
        "name": "Mood-based PF enhancements",
        "description": "Adjust PF recommendations based on inferred mood signals from emoji usage. This logic is soft-tuned using BB and undergoes quiet testing in ShadowMode."
    },
    {
        "name": "New user rewards via NR profile suggestions",
        "description": "At onboarding, users will receive NR-curated profiles to follow for faster network building. A/B testing will use Spanner."
    },
    {
        "name": "Creator fund payout tracking in CDS",
        "description": "Monetization events will be tracked through CDS to detect anomalies in creator payouts. DRT rules apply for log trimming."
    },
    {
        "name": "Trial run of video replies in EU",
        "description": "Roll out video reply functionality to users in EEA only. GH will manage exposure control, and BB is used to baseline feedback."
    },
    {
        "name": "Canada-first PF variant test",
        "description": "Launch a PF variant in CA as part of early experimentation. Spanner will isolate affected cohorts and Glow flags will monitor feature health."
    },
    {
        "name": "Chat UI overhaul",
        "description": "A new chat layout will be tested in the following regions: CA, US, BR, ID. GH will ensure location targeting and ShadowMode will collect usage metrics without user impact."
    },
    {
        "name": "Regional trial of autoplay behavior",
        "description": "Enable video autoplay only for users in US. GH filters users, while Spanner logs click-through deltas."
    },
    {
        "name": "South Korea dark theme A/B experiment",
        "description": "A/B test dark theme accessibility for users in South Korea. Rollout is limited via GH and monitored with FR flags."
    },
    {
        "name": "Age-specific notification controls with ASL",
        "description": "Notifications will be tailored by age using ASL, allowing us to throttle or suppress push alerts for minors. EchoTrace will log adjustments, and CDS will verify enforcement across rollout waves."
    },
    {
        "name": "Chat content restrictions via LCP",
        "description": "Enforce message content constraints by injecting LCP rules on delivery. ShadowMode will initially deploy the logic for safe validation. No explicit mention of legal requirements, but privacy context is implied."
    },
    {
        "name": "Video upload limits for new users",
        "description": "Introduce limits on video uploads from new accounts. IMT will trigger thresholds based on BB patterns. These limitations are partly for platform safety but without direct legal mapping."
    },
    {
        "name": "Flag escalation flow for sensitive comments",
        "description": "A flow that detects high-risk comment content and routes it via CDS with Redline markers. The logic applies generally and is monitored through EchoTrace, with no mention of regional policies."
    },
    {
        "name": "User behavior scoring for policy gating",
        "description": "Behavioral scoring via Spanner will be used to gate access to certain tools. The feature tracks usage and adjusts gating based on BB divergence."
    },
    {
        "name": "Minor-safe chat expansion via Jellybean",
        "description": "We're expanding chat features, but for users flagged by Jellybean, certain functions (e.g., media sharing) will be limited. BB and ASL will monitor compliance posture."
    },
    {
        "name": "Friend suggestions with underage safeguards",
        "description": "New suggestion logic uses PF to recommend friends, but minors are excluded from adult pools using ASL and CDS logic. EchoTrace logs interactions in case future policy gates are needed."
    },
    {
        "name": "Reaction GIFs with embedded filtering",
        "description": "Enable GIFs in comments, while filtering content deemed inappropriate for minor accounts. Softblock will apply if a flagged GIF is used by ASL-flagged profiles."
    },
    {
        "name": "Longform posts with age-based moderation",
        "description": "Longform post creation is now open to all. However, moderation for underage authors is stricter via Snowcap."
    },
    {
        "name": "Custom avatar system with identity checks",
        "description": "Users can now design custom avatars. For safety, T5 triggers block adult-themed assets from use by underage profiles. Age detection uses ASL and logs flow through GH."
    }
]


def upload_features():
    """Upload all features to the API endpoint"""
    successful_uploads = 0
    failed_uploads = 0

    print(f"Starting upload of {len(features)} features to {API_URL}")
    print("-" * 50)

    for i, feature in enumerate(features, 1):
        try:
            response = requests.post(
                API_URL,
                json=feature,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code in [200, 201]:
                print(
                    f"✓ [{i:2d}/{len(features)}] Successfully uploaded: {feature['name'][:50]}...")
                successful_uploads += 1
            else:
                print(
                    f"✗ [{i:2d}/{len(features)}] Failed to upload: {feature['name'][:50]}...")
                print(f"    Status Code: {response.status_code}")
                print(f"    Response: {response.text}")
                failed_uploads += 1

        except requests.exceptions.RequestException as e:
            print(
                f"✗ [{i:2d}/{len(features)}] Connection error for: {feature['name'][:50]}...")
            print(f"    Error: {str(e)}")
            failed_uploads += 1

    print("-" * 50)
    print(f"Upload Summary:")
    print(f"  Successful: {successful_uploads}")
    print(f"  Failed: {failed_uploads}")
    print(f"  Total: {len(features)}")


if __name__ == "__main__":
    upload_features()
