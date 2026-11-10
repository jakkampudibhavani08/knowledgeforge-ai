from fastapi import FastAPI, HTTPException, File, UploadFile
from pathlib import Path 
import uuid 
import os 

app=FastAPI(title="KnowledgeForge AI")

upload_dir = Path("uploads")
upload_dir.mkdir(parents=True, exist_ok=True)



@app.get("/health")
def health_check():
    return{"status":"Healthy"}


@app.post("/documents/upload", status_code=201)
async def upload_doc(file:UploadFile=File(...)):
    max_file_size=10*1024*1024 
    file_extensions={".pdf",".txt"}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please mention Filename"
        )
   
    extensions=Path(file.filename).suffix.lower()

    if extensions not in file_extensions:
        raise HTTPException(
            status_code=415,
            detail="File type not supported. Only Pdf and txt allowed."
        )

    content=await file.read(max_file_size+1)
    if len(content)==0:
        raise HTTPException(
            status_code=400,
            detail="Empty files are not allowed"
        )
    if len(content)>max_file_size:
            raise HTTPException(
                status_code=413,
                detail="Maximum File size is 5GB"
            )

    file_id=str(uuid.uuid4())
    new_filename=f"{file_id}{extensions}"
    file_path=upload_dir/new_filename
    file_path.write_bytes(content)

    return{
        "message": "File Successfully uploaded",
        "file_id":file_id,
        "original_filename":file.filename,
        "new_filename": new_filename,
        "size":len(content),
        "file_path":str(file_path),
        "format type": extensions
    }


        

