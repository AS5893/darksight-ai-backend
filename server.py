import os
import magic
import mimetypes
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("CRITICAL: GOOGLE_API_KEY not found in .env file. Node initialization aborted.")

genai.configure(api_key=GEMINI_API_KEY)

try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if not available_models:
        raise RuntimeError("No compatible Gemini models found for this API key.")
    
    target_model_name = next((m for m in available_models if "1.5-pro" in m), 
                            next((m for m in available_models if "1.5-flash" in m), 
                            available_models[0]))
    
    model = genai.GenerativeModel(model_name=target_model_name)
    print(f"SYSTEM: DarkSight Node initialized with engine: {target_model_name} [cite: 6, 43]")
except Exception as e:
    print(f"FAILED TO INITIALIZE ML ENGINE: {e}")
    model = genai.GenerativeModel('gemini-1.0-pro')

app = FastAPI(title="DarkSight AI - Federated Intelligence Gateway [cite: 1, 2]")

def get_pcap_analysis_prompt(context: str) -> str:
    """
    Constructs the Semantic Threat Hashing prompt to identify 'Underlying Intent'[cite: 68, 81].
    """
    return f"""
    ROLE: You are the DarkSight AI Federated Intelligence Node. Your goal is to convert raw network telemetry into semantic threat intelligence without exposing Raw PII[cite: 43, 69].

    TASK: Analyze the provided PCAP/Network data to identify Dark Web threat correlation[cite: 2, 21].
    
    REQUIRED ANALYSIS STEPS:
    1. PROTOCOL DETECTION: Classify traffic patterns. Identify if the communication utilizes Tor, VPN, or I2P hidden services[cite: 89, 92].
    2. SEMANTIC THREAT HASHING: Identify the 'Underlying Intent' of the traffic (e.g., credential dump, exploit kit sale, or ransomware heartbeat)[cite: 68, 81].
    3. CROSS-LANGUAGE CORRELATION: Map technical indicators to known threat clusters (Russian, English, or slang)[cite: 78, 85].
    4. ENTITY EXTRACTION: Identify Crypto Wallets, Vendor Aliases, or C2 IP addresses[cite: 98, 99].

    SPECIFIC USER CONTEXT: {context if context else "General threat hunting."}

    OUTPUT SCHEMA (JSON-ready format):
    - Unified Risk Score (0-100) [cite: 103]
    - Threat Level (Low, Medium, Critical) [cite: 104, 105, 106]
    - Semantic Cluster [cite: 85]
    - Anomalies Detected [cite: 93]
    - Risk Justification
    """

@app.post("/analyze-pcap", status_code=status.HTTP_201_CREATED)
async def analyze_pcap(
    file: UploadFile = File(...),
    context: Optional[str] = Form(None)
):
    content = await file.read()
    
    await file.seek(0)

    try:
        system_prompt = get_pcap_analysis_prompt(context)
        pcap_hex = content.hex()[:30000] 
        full_query = f"{system_prompt}\n\nRAW NETWORK DATA (HEX):\n{pcap_hex}"
        
        response = model.generate_content(full_query)

        return {
            "fileName": file.filename,
            "status": "Success",
            "analysis": response.text,
            "architecture_note": "Processed via DarkSight ML Worker Layer [cite: 132]"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Intelligence Latency / Analysis failed: {str(e)} "
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)