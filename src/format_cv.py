from .params import CVParams


from pathlib import Path

from jinja2 import Environment

def get_latex_template(params: CVParams) -> str:
    latex_template_dir = Path(params.latex_template_dir)
    suffix_dir = "moderncv.tex.jinja" if params.cv_style == "modern" else "classiccv.tex.jinja"

    latex_template = latex_template_dir / suffix_dir

    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_text = latex_template.read_text()
    template = env.from_string(template_text)
    return template

def format_cv(params: CVParams) -> str:
    template = get_latex_template(params)

    # Render
    output = template.render(**params.__dict__)

    return output
