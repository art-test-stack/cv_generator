from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional

class Activity(BaseModel):
    name: str
    description: str
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
    highlights: Optional[List[str]] = None

class Header(BaseModel):
    name: str
    description: str

class Language(BaseModel):
    id: int
    name: str
    fluency: str

class Project(BaseModel):
    id: int
    title: str
    description: str
    url: Optional[str] = None
    technologies: List[str] = None
    bullet_points: List[str] = None
    dates: Optional[str] = None

class Skill(BaseModel):
    name: str
    items: List[str]
    emoji: Optional[str] = None

class Summary(BaseModel):
    id: int
    content: str

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