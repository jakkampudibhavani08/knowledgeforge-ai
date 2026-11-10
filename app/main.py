from fastapi import FastAPI 

app=FastAPI(title="KnowledgeForge AI")

@app.get("/health")
def health_check():
    return{"status":"Healthy"}