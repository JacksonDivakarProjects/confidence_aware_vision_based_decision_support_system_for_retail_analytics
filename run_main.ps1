Set-Location $PSScriptRoot

# Activate venv (PowerShell)
.\.venv\Scripts\Activate.ps1

# Age & Gender (new window)
Start-Process powershell `
  -ArgumentList "-NoExit", "-Command", "cd 'Python Folder\age_and_gender_classification'; python main.py"

# FastAPI (new window)
Start-Process powershell `
  -ArgumentList "-NoExit", "-Command", "cd 'Python Folder\fastapi_backend'; python -m uvicorn app:app --reload --port 9000"

# React (new window)
Start-Process powershell `
  -ArgumentList "-NoExit", "-Command", "cd 'React Folder\frontend'; npm start"
