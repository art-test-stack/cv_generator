from .schemas import CVContent
from .params import CVParams
import json
from pathlib import Path
from typing import Dict

def get_content(params: CVParams) -> Dict[str, Dict]:
    data_dir = params.data_dir
    content_dir = {
        "activities": Path(f"{data_dir}/activities.json"),
        "contact": Path(f"{data_dir}/contact.json"),
        "education": Path(f"{data_dir}/education.json"),
        "experiences": Path(f"{data_dir}/experiences.json"),
        "header": Path(f"{data_dir}/header.json"),
        "languages": Path(f"{data_dir}/languages.json"),
        "projects": Path(f"{data_dir}/projects.json"),
        "skills": Path(f"{data_dir}/skills.json"),
        "summary": Path(f"{data_dir}/summary.json")
    }
    content = { key: json.loads(path.read_text()) for key, path in content_dir.items() }
    
    return content