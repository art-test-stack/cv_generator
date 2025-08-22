from .schemas import CVContent
from .params import CVParams
from typing import Union, Dict
from pathlib import Path
import json


def make_activities(cv_content: CVContent, params: CVParams) -> str:
    activities_raw = cv_content.activities

    use_emojis = params.use_emojis
    emoji_section = "\\emoji{seedling} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Activities}}\n")
    latex_code.append("\\resumeSubHeadingListStart\n")

    for activity in activities_raw:
        activity_emoji = f"\\emoji{{{activity.emoji}}} " if use_emojis and activity.emoji else ""
        latex_code.append(
            f"\\resumeItem{{{activity_emoji}\\textbf{{{activity.name}}}: {activity.text}}} \\\\ \n"
        )

    latex_code.append("\\resumeSubHeadingListEnd\n")
    return "".join(latex_code)

def make_contact(cv_content: CVContent, params: CVParams) -> str:
    contact_raw = cv_content.contact

    use_emojis = params.use_emojis

    emoji_section = "\\emoji{mobile-phone-with-arrow} " if use_emojis else ""
    emoji_phone = "\\emoji{iphone} " if use_emojis else ""
    # emoji_phone = "\\emoji{iphone} " if use_emojis else ""
    emoji_email = "\\emoji{e-mail} " if use_emojis else ""
    emoji_github = f"\\includegraphics[width={params.logo_width}]{{{params.github_logo}}}\\; " if use_emojis else "github/"
    emoji_linkedin = f"\\includegraphics[width={params.logo_width}]{{{params.linkedin_logo}}}\\; in/" if use_emojis else "linkedIn/"

    latex_code = []
    latex_code.append("\\centering\n\n")

    if params.merge_contact_header:
        latex_code.append("\\vspace{7pt}\n\n")
    else:
        latex_code.append(f"\\section{{{emoji_section}Contact}}\n")

    phone = contact_raw.phone
    phone_href = phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "").replace("~", "")
    latex_code.append(f"{emoji_phone}\\href{{tel:{phone_href}}}{{{phone}}}\n\n")

    email = contact_raw.email
    latex_code.append(f"{emoji_email}\\href{{mailto:{email}}}{{ \\footnotesize {email}}} \n\n")

    github = contact_raw.github
    if github:
        latex_code.append(
            f"\\href{{https://github.com/{github}}}{{{emoji_github}{github}}}  \n\n"
        )

    linkedin = contact_raw.linkedin
    if linkedin:
        latex_code.append(
            f"\\href{{https://linkedin.com/in/{linkedin}}}{{{emoji_linkedin}{linkedin}}}\n"
        )

    return "".join(latex_code) 


def make_education(cv_content: CVContent, params: CVParams) -> str:
    education_raw = cv_content.education
    use_emojis = params.use_emojis

    emoji_section = "\\emoji{graduation-cap} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Education}}\n")
    latex_code.append("\\resumeSubHeadingListStart\n")

    educations = sorted(education_raw, key=lambda x: x.id, reverse=True)
    for edu in educations:
        if not edu.institution and not edu.location and not edu.dates and not edu.description:
            latex_code.append(f"\\item{{\\textbf{{{edu.title}}}}}\n\vspace{{5pt}}\n")
        else:
            logo = f"\\includegraphics[width={params.logo_width}]{{{edu.logo}}} " if use_emojis and edu.logo else ""
            latex_code.append(
                f"\\resumeSubheading{{\\href{{{edu.url}}}{{{logo}{edu.title}}}}}{{{edu.location}}}{{{edu.description}}}{{{edu.dates}}} \n"
            )
            if edu.highlights:
                latex_code.append("\\resumeItemListStart\n")
                for point in edu.highlights:
                    latex_code.append(f"\\resumeItem{{{point['text']}}}\n")
                latex_code.append("\\resumeItemListEnd\n")

    latex_code.append("\\resumeSubHeadingListEnd\n")

    return "".join(latex_code)

def make_experiences(cv_content: CVContent, params: CVParams) -> str:
    experience_raw = cv_content.experiences
    use_emojis = params.use_emojis

    emoji_section = "\\emoji{briefcase} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Experiences}}\n")
    latex_code.append("\\resumeSubHeadingListStart\n")

    experiences = sorted(experience_raw, key=lambda x: x.id, reverse=True)
    for exp in experiences:
        logo = f"\\includegraphics[width={params.logo_width}]{{{exp.logo}}} " if use_emojis and exp.logo else ""
        latex_code.append(
            f"\\resumeSubheading{{{logo}{exp.title}}}{{{exp.location}}}{{\\href{{{exp.url}}}{{{exp.company}}}}}{{{exp.dates}}} \n"
        )
        if exp.highlights:
            latex_code.append("\\resumeItemListStart\n")
            highlights = sorted(exp.highlights, key=lambda x: x["id"], reverse=True)
            for highlight in highlights:
                latex_code.append(f"\\resumeItem{{{highlight['text']}}}\n")
            latex_code.append("\\resumeItemListEnd\n")
    latex_code.append("\\resumeSubHeadingListEnd\n")
    return "".join(latex_code)


def make_header(cv_content: CVContent, params: CVParams) -> str:
    header_raw = cv_content.header
    header = f"""\\Centering\n
\\textbf{{\\LARGE {header_raw.name}}} \\\\ \n\n
\\vspace{{7pt}} \n
{{\\large {header_raw.description}}}\n
\\RaggedLeft"""
    return header

def make_languages(cv_content: CVContent, params: CVParams) -> str:
    languages_raw = cv_content.languages

    use_emojis = params.use_emojis
    emoji_section = "\\emoji{speaking-head} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Languages}}\n")

    for language in languages_raw:
        latex_code.append(
            f"\\textbf{{{language.name}}}: {language.fluency} \\\\\n"
        )

    return "".join(latex_code)


def make_projects(cv_content: CVContent, params: CVParams) -> str:
    projects_raw = cv_content.projects

    use_emojis = params.use_emojis
    emoji_section = "\\emoji{hammer-and-wrench} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Projects}}\n")
    latex_code.append("\\resumeSubHeadingListStart\n")
    for project in projects_raw:
        # Project logo not implemented yet
        # logo = f"\\includegraphics[width={params.logo_width}]{{{project.logo}}} " if use_emojis and project.logo else ""
        logo = ""
        project_title = f"{logo}{project.title}"
        if project.url:
            project_title = f"\\href{{{project.url}}}{{{logo}{project.title}}}"

        latex_code.append(
            f"\\resumeSubheading{{{project_title}}}{{}}{{{project.dates}}}{{}} \n"
        )

        if project.text:
            latex_code.append("\\resumeItemListStart\n")
            latex_code.append(f"\\resumeItem{{{project.text}}}\n")
            latex_code.append("\\resumeItemListEnd\n")
    latex_code.append("\\resumeSubHeadingListEnd\n")
    return "".join(latex_code)


def make_skills(cv_content: CVContent, params: CVParams) -> str:
    skills_raw = cv_content.skills

    use_emojis = params.use_emojis

    emoji_section = "\\emoji{rocket} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Skills}}\n")
    latex_code.append("\\resumeSubHeadingListStart\n")

    for skill in skills_raw:
        emoji_skill = f"\\emoji{{{skill.emoji}}} " if use_emojis and skill.emoji else ""
        if not skill.items:
            continue
        skill_items = ", ".join(skill.items)
        latex_code.append(
            f"\\resumeItem{{{emoji_skill}}}\\textbf{{{skill.name}}}: {{{skill_items}.}}\n"
        )
    latex_code.append("\\resumeSubHeadingListEnd\n")

    return "".join(latex_code)


def make_summary(cv_content: CVContent, params: CVParams) -> str:
    summary_raw = cv_content.summary

    use_emojis = params.use_emojis
    emoji_section = "\\emoji{pushpin} " if use_emojis else ""

    latex_code = []
    latex_code.append(f"\\section{{{emoji_section}Summary}}\n\n")
    latex_code.append("\\justifying\n\n")
    latex_code.append(f"{{{summary_raw.text}}}\n\n")
    latex_code.append("\RaggedLeft\n")
    latex_code.append("\\vspace{5pt}\n")

    return "".join(latex_code)


def make_content(cv_content: CVContent, params: CVParams) -> Dict:

    content = {
        "header": make_header(cv_content, params),
        "contact": make_contact(cv_content, params),
        "education": make_education(cv_content, params),
        "experiences": make_experiences(cv_content, params),
        "skills": make_skills(cv_content, params),
        "projects": make_projects(cv_content, params),
        "languages": make_languages(cv_content, params),
        "activities": make_activities(cv_content, params),
        "summary": make_summary(cv_content, params),
        "pic": f"\n\\includegraphics[width=.95\\linewidth]{{{params.pic}}}"
    }
    return content