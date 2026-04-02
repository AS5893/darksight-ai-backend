# darksight-ai-backend

# DarkSight AI: Federated Intelligence Gateway 🛡️🌐

**DarkSight AI** is a privacy-preserving, localized network intelligence node designed to convert raw network telemetry (PCAPs) into actionable semantic threat intelligence. By utilizing a **Domain-adapted Transformer**, DarkSight identifies the "Underlying Intent" of malicious traffic without compromising user privacy.

---

## 🚀 Technical Breakthroughs

- **Federated Semantic Threat Hashing**: Moves beyond traditional signature-based detection (like Snort) to identify high-level intent (e.g., "Ransomware Heartbeat" or "Credential Dump").
- **Zero Raw Data Sharing**: Processes network hex-dumps locally within the node. Only the extracted intelligence is shared, ensuring **Zero PII Leakage**.
- **Extreme Fault Tolerance**: Features a self-healing ML initialization engine that dynamically discovers and selects the best available generative model (Gemini 1.5/2.5/3) to prevent system downtime.
- **Unified Risk Scoring**: Generates a composite **0-100 Risk Score** and classifies threats into (Low, Medium, Critical) levels for immediate investigator response.

---

## 🏗️ Architecture & Flow

1. **Ingestion Layer**: Raw PCAP data is received via a high-concurrency FastAPI gateway.
2. **ML Worker Layer**: Binary data is converted to a privacy-preserving Hex format.
3. **Intelligence Engine**: The Hex data is analyzed by a localized LLM for protocol detection (Tor, VPN, I2P) and entity extraction (Crypto Wallets, C2 IPs).
4. **Output Gateway**: A structured JSON response is returned, providing a **Unified Risk Score** and **Semantic Cluster** (e.g., "Financial Malware / English Market").

---

How to Use
To analyze a suspicious network capture, send a POST request to the /analyze-pcap endpoint.

Using PowerShell:

PowerShell
$url = "http://localhost:8001/analyze-pcap"
$filePath = "C:\path\to\your\Noobs Keylogger.pcap"

Invoke-RestMethod -Uri $url -Method Post -Form @{
    file = Get-Item $filePath
    context = "Checking for ransomware patterns"
}

Expected Response:

JSON
{
  "fileName": "Noobs Keylogger.pcap",
  "status": "Success",
  "analysis": "...[Extracted Threat Intelligence]...",
  "architecture_note": "Processed via DarkSight ML Worker Layer"
}
