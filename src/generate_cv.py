from .params import CVParams
from .schemas import CVContent
from .get_content import get_content
from .select_content import select_content
from .make_sections import make_content
from .format_cv import format_cv
import mlflow, yaml, pathlib
from jinja2 import Template
import subprocess, platform, re, emoji
from pathlib import Path
from jinja2 import Environment, FileSystemLoader 


# def render_cv(profile: Profile, job_text: str, template_path: str) -> str:
#     # Simple tailoring: prioritize overlapping skills and echo keywords into bullets
#     env = Environment(loader=FileSystemLoader(searchpath=str(Path(template_path).parent)))
#     t = env.get_template(Path(template_path).name)
#     tailored = profile.model_copy(deep=True)
#     kws = set([w.lower() for w in job_text.split() if len(w)>3])
#     tailored.skills = sorted(set([s for s in profile.skills if s.lower() in kws] + profile.skills))
#     return t.render(profile=tailored)

def save_cv(md_text: str, out_dir: str = "data/interim") -> str:
    out = pathlib.Path(out_dir) / "cv.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md_text)
    mlflow.log_artifact(str(out), artifact_path="cv")
    return str(out)


def generate_latex_cv(params: CVParams, job_description=None) -> str:
    """
    Generate a LaTeX CV from the given parameters.
    :param params: Dictionary containing parameters for CV generation.
    :return: LaTeX document as a string.
    """

    raw_content = get_content(params)
    cv_content = select_content(raw_content, job_description, params)
    latex_sections = make_content(cv_content, params)
    latex_sections["main"] = format_cv(params)
    print("Platform:", platform.system())
    # if platform.system() == "Darwin":
    #     for name, content in latex_sections.items():
            # fixed_content = content.replace('\r\n', '\n').replace('\r', '\n')
            # latex_sections[name] = re.sub(r'\\emoji\{(.*?)\}', lambda m: f"\\emoji{{{emoji.emojize(f':{m.group(1)}:', language='alias')}}}", content)

    output_dir = Path(params.cv_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, content in latex_sections.items():
        output_file = output_dir / f"{name}.tex"
        print(f"Writing LaTeX section {name} to {output_file}")
        output_file.write_text(content)
    
    return latex_sections



def compile_latex_cv(params: CVParams, quite: bool = True) -> str:
    """
    Compile the LaTeX content into a PDF file.
    :param latex_content: The LaTeX content to compile.
    :param output_path: The path where the compiled PDF will be saved.
    """
    # Here you would typically call a LaTeX compiler like pdflatex
    # subprocess.run(['pdflatex', output_path])  # Uncomment to run LaTeX compilation

    output_path = f"{params.cv_folder}/main.tex"
    print(f"Compiling LaTeX CV to PDF at {output_path}")
    cmd = [
        "lualatex",
        f"-jobname={params.cv_name}",
        "-output-directory", ".",
        "main.tex"
    ]
    run_kwargs = {"check": True, "cwd": f"/Users/arthurtestard/generate_cv/{params.cv_folder}"}
    if quite:
        run_kwargs.update({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL})
    subprocess.run(cmd, **run_kwargs)

    return output_path

