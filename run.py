import uvicorn
import sys

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')  # для Windows
    uvicorn.run("src.task_manager.interfaces.api.main:app", host="0.0.0.0", port=8000, reload=True) 