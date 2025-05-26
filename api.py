from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, AnyHttpUrl
from typing import Optional, Dict, Any
import uvicorn
import os

# Import existing FangScan functions
from core.ssl_info import get_ssl_info
from core.tech_detect import detect_cms, detect_js_frameworks, builtwith_tech
from core.cdn_check import check_cdn
from core.dns_enum import get_dns_records
from core.headers import get_headers, check_security_headers

app = FastAPI(
    title="FangScan API",
    description="REST API for FangScan Web Reconnaissance Tool",
    version="2.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: AnyHttpUrl
    scan_ssl: bool = False
    scan_cms: bool = False
    scan_headers: bool = False
    scan_cdn: bool = False
    scan_dns: bool = False
    scan_all: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://example.com",
                    "scan_all": True
                }
            ]
        }
    }

@app.post("/scan")
async def scan(request: ScanRequest):
    try:
        url = str(request.url)
        hostname = url.split("//")[-1].split("/")[0]
        result = {"url": url}

        if request.scan_all or request.scan_ssl:
            result["ssl_info"] = get_ssl_info(hostname)

        if request.scan_all or request.scan_cms:
            techs = builtwith_tech(url)
            result["technologies"] = techs
            result["cms"] = detect_cms(url, techs)
            result["javascript_frameworks"] = detect_js_frameworks(url)

        if request.scan_all or request.scan_cdn:
            headers = get_headers(url)
            result["server_info"] = {
                "server": headers.get("Server", "Unknown"),
                "x_powered_by": headers.get("X-Powered-By", "Unknown"),
                "http3_support": "alt-svc" in headers,
                "cdn": check_cdn(headers, hostname).get("detected", "Unknown")
            }

        if request.scan_all or request.scan_dns:
            result["dns"] = get_dns_records(hostname)

        if request.scan_all or request.scan_headers:
            headers = get_headers(url)
            result["headers"] = check_security_headers(headers)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable for Codespace compatibility
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port) 