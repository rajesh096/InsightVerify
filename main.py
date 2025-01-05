from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import mimetypes
import uvicorn
import torch
import socket

if torch.cuda.is_available():
    print("GPU Available")
else:
    print("GPU not accessible, stopping program")
    exit()

def get_local_ip():
    try:
        # Use a dummy connection to determine the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return None

local_ip = get_local_ip()
if local_ip:
    print(f"Your device's local IP address is: {local_ip}")
    print(f"Share this IP with the port (e.g., {local_ip}:12345) for local communication.")
else:
    print("Could not retrieve the local IP address.")

app = FastAPI()

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images (jpeg, png) and PDFs are allowed.")
    
    return JSONResponse(content={"filename": file.filename, "content_type": mime_type})

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)