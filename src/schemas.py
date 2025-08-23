from pydantic import BaseModel
from pathlib import Path
from typing import Dict, List, Optional

class Activity(BaseModel):
    name: str
    text: str
    emoji: Optional[str] = None

class Contact(BaseModel):
    phone: str
    email: str
    github: Optional[str] = None
    linkedin: Optional[str] = None

class Education(BaseModel):
    id: int
    title: str
    institution: Optional[str] = None
    location: Optional[str] = None
    dates: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    url: Optional[str] = None
    logo: Optional[str] = None

class Experience(BaseModel):
    id: int
    title: str
    company: str
    location: str
    dates: str
    highlights: Optional[List[Dict]] = None
    url: Optional[str] = None
    logo: str = ""

class Header(BaseModel):
    name: str
    text: str
    specialization: Optional[str] = None
    nationality: Optional[str] = None
    education: Optional[str] = None

class Language(BaseModel):
    id: int
    name: str
    fluency: str

class Project(BaseModel):
    id: int
    title: str
    text: str
    url: Optional[str] = None
    technologies: List[str] = None
    bullet_points: List[str] = None
    dates: Optional[str] = None
    type: Optional[str] = None

class Skill(BaseModel):
    name: str
    items: List[str]
    emoji: Optional[str] = None

class Summary(BaseModel):
    id: int
    text: str

class CVContent(BaseModel):
    activities: List[Activity]
    contact: Contact
    education: List[Education]
    experiences: List[Experience]
    header: Header
    languages: List[Language]
    projects: List[Project]
    skills: List[Skill]
    summary: Optional[Summary] = None