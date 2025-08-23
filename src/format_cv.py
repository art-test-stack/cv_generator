from .params import CVParams


from pathlib import Path

from jinja2 import Environment

def get_latex_template(params: CVParams) -> str:
    latex_template_dir = Path(params.latex_template_dir)
    base_template = latex_template_dir / "base.tex.jinja"
    if not base_template.exists():
        raise FileNotFoundError(f"Base LaTeX template not found at {base_template}")
    
    suf_dir = {
        "modern": "moderncv.tex.jinja",
        "classic": "classiccv.tex.jinja",
        "modernus": "modernuscv.tex.jinja"
    }
    suffix_dir = suf_dir.get(params.cv_style, "moderncv.tex.jinja")

    latex_template = latex_template_dir / suffix_dir

    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_text = base_template.read_text() + latex_template.read_text()
    template = env.from_string(template_text)
    return template

def format_cv(params: CVParams) -> str:
    template = get_latex_template(params)

    # Render
    output = template.render(**params.__dict__)

    return output
