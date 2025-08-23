from .params import CVParams
from langdetect import detect
from emoji import EMOJI_DATA

def get_params(job_description: str = None) -> CVParams:
    """Get parameters for CV generation."""
    params = CVParams()
    if not job_description:
        return params
    language = detect(job_description)
    # DETERMINE JOB OFFER LANGUAGE
    if language not in ["en", "fr"]:
        language = "en"
    params.cv_language = language

    # DETERMINE IF EMOJIS SHOULD BE USED
    emoji_threshold = 5
    nb_emojis = sum(1 for char in job_description if char in set(EMOJI_DATA.keys()))
    params.use_emojis = nb_emojis > emoji_threshold
    
    # DETERMINE IF SHOULD MERGE CONTACT AND HEADER
    params.merge_contact_header = params.use_emojis

    # DETERMINE CV STYLE
    if params.use_emojis or language == "fr":
        params.cv_style = "modern"
    elif language == "en":
        params.cv_style = "classic"
    else:
        params.cv_style = "modern"
        
    return params