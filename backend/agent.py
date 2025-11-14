import os
import base64
import json
from typing import Dict, Any, Optional
import requests
from langfuse import Langfuse
try:
    from langfuse.callback import CallbackHandler  # type: ignore
except ImportError:
    CallbackHandler = None


class HandwritingExtractionAgent:
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llava")
        self.langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        self.langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        self.langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        self.request_timeout = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))
        
        self.langfuse: Optional[Langfuse] = None
        self.langfuse_handler = None
        
        if self.langfuse_public_key and self.langfuse_secret_key:
            try:
                self.langfuse = Langfuse(
                    public_key=self.langfuse_public_key,
                    secret_key=self.langfuse_secret_key,
                    host=self.langfuse_host
                )
                if CallbackHandler:
                    self.langfuse_handler = CallbackHandler(
                        public_key=self.langfuse_public_key,
                        secret_key=self.langfuse_secret_key,
                        host=self.langfuse_host
                    )
                print("✓ Langfuse initialized successfully")
            except Exception as e:
                print(f"⚠ Langfuse initialization failed: {e}")
                print("Continuing without Langfuse tracing...")
        else:
            print("⚠ Langfuse credentials not found. Continuing without tracing...")
        
        print(f"✓ Ollama configured (host={self.ollama_host}, model={self.ollama_model})")
    
    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_handwriting(self, image_path: str, filename: str) -> Dict[str, Any]:
        try:
            base64_image = self.encode_image(image_path)
            
            prompt = """You are an expert OCR system specialized in reading handwritten text.

Analyze this handwritten document carefully and extract ALL the information you can see.

CRITICAL INSTRUCTIONS:
1. DO NOT assume or hallucinate any fields
2. ONLY extract what is actually visible in the image
3. Return the data as clean, structured JSON
4. Create field names based on what you see (labels, headings, etc.)
5. If a field is blank or unreadable, mark it as null or "unreadable"
6. Preserve the logical structure and grouping of information
7. Be precise with values - don't guess or approximate

Return ONLY valid JSON with no additional text or explanation.
The JSON should have descriptive keys based on the actual content structure."""

            payload = {
                "model": self.ollama_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a precise OCR expert that returns clean JSON output."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [base64_image]
                    }
                ],
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json=payload,
                timeout=self.request_timeout
            )
            response.raise_for_status()
            response_data = response.json()
            
            if "message" not in response_data or "content" not in response_data["message"]:
                raise ValueError("Unexpected response from Ollama")
            
            extracted_text = response_data["message"]["content"]
            
            extracted_text = extracted_text.strip()
            
            if extracted_text.startswith("```json"):
                extracted_text = extracted_text[7:]
            if extracted_text.startswith("```"):
                extracted_text = extracted_text[3:]
            if extracted_text.endswith("```"):
                extracted_text = extracted_text[:-3]
            extracted_text = extracted_text.strip()
            
            try:
                structured_data = json.loads(extracted_text)
            except json.JSONDecodeError:
                structured_data = {"raw_text": extracted_text}
            
            result = {
                "success": True,
                "filename": filename,
                "extracted_data": structured_data,
                "message": "Handwriting extracted successfully"
            }
            
            if self.langfuse:
                try:
                    trace = self.langfuse.trace(name="handwriting_extraction")  # type: ignore
                    trace.update(input={"filename": filename}, output=result)
                except Exception as e:
                    print(f"⚠ Langfuse trace failed: {e}")
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "filename": filename,
                "error": str(e),
                "message": "Failed to extract handwriting"
            }
            
            if self.langfuse:
                try:
                    trace = self.langfuse.trace(name="handwriting_extraction_error")  # type: ignore
                    trace.update(input={"filename": filename}, output=error_result)
                except:
                    pass
            
            return error_result
