from .params import CVParams
from .schemas import CVContent, Activity, Experience, Project, Skill, Education, Summary, Language, Contact, Header
from typing import Dict, Optional
from sentence_transformers import SentenceTransformer, util
import json
import openai  # if you want API mode
import ollama  # if you want local mode


def retrieve_topk(embedder, job_desc, items, k=3):
    job_emb = embedder.encode(job_desc, convert_to_tensor=True)
    if not items[0].get("text", None):
        for item in items:
            item["text"] = str(item)
    item_embs = embedder.encode([it["text"] for it in items], convert_to_tensor=True)

    scores = util.pytorch_cos_sim(job_emb, item_embs)[0]
    ranked = sorted(zip(items, scores), key=lambda x: float(x[1]), reverse=True)
    return [it[0] for it in ranked[:k]]


def llm_select(job_desc, highlights, projects, skills, mode="ollama"):
    # Format candidate list
    candidates = {
        "highlights": highlights,
        "projects": projects,
        "skills": skills
    }

    system_prompt = """You are an assistant that selects the most relevant items
for a job application based on a job description. You must only return the IDs
of the selected items, never create new IDs, and respond in JSON format."""

    user_prompt = f"""
    Job offer:
    ---
    {job_desc}
    ---

    Candidate items (with id and text):
    {json.dumps(candidates, indent=2)}

    Task:
    - Return ONLY the IDs of the most relevant items.
    - Respond in JSON with three lists: "highlights", "projects", "skills".
    """

    if mode == "ollama":
        response = ollama.chat(model="mistral", messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return json.loads(response["message"]["content"])

    elif mode == "openai":
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)



def select_content(
        cv_content: CVContent, 
        job_description: Optional[Dict[str, str]], 
        params: CVParams
    ) -> CVContent:
    """Select content based on parameters."""
    if not job_description:
        job_description = "This is a general job description for a professional position."
    if params.selection_mode == "top_k":
        embedder = SentenceTransformer(params.sentence_tf_model) 

        top_activities = retrieve_topk(
            embedder=embedder, 
            job_desc=job_description, 
            items=cv_content["activities"], 
            k=params.max_activities
        )
        for exp in cv_content["experiences"]:
            top_highlights = retrieve_topk(
                embedder=embedder, 
                job_desc=job_description, 
                items=exp["highlights"], 
                k=params.max_exp_highlights
            )
            exp["highlights"] = top_highlights
        top_projects = retrieve_topk(
            embedder=embedder, 
            job_desc=job_description, 
            items=cv_content["projects"], 
            k=params.max_projects
        )
        top_skills = retrieve_topk(
            embedder=embedder, 
            job_desc=job_description, 
            items=cv_content["skills"], 
            k=params.max_skills
        )
        top_summary = retrieve_topk(
            embedder=embedder, 
            job_desc=job_description, 
            items=cv_content["summary"], 
            k=1
        ) if cv_content["summary"] else []
        top_education = cv_content["education"][:params.max_edu]
        top_header = retrieve_topk(
            embedder=embedder, 
            job_desc=job_description, 
            items=cv_content["header"], 
            k=1
        )[0] if cv_content["header"] else {}

    else:
        raise ValueError(f"Unknown selection mode: {params.selection_mode}")
    
    content = {
        "activities": [Activity(**act) for act in top_activities],
        "education": [Education(**edu) for edu in top_education],
        "experiences": [Experience(**exp) for exp in cv_content["experiences"]],
        "languages": [Language(**lang) for lang in cv_content["languages"]],
        "projects": [Project(**proj) for proj in top_projects],
        "skills": [Skill(**skill) for skill in top_skills],
        "summary": Summary(**top_summary[0]) if top_summary else None,
        "contact": Contact(**cv_content["contact"]),
        "header": Header(**top_header)
    }
    del cv_content
    return CVContent(**content)