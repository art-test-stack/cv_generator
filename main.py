from src.generate_cv import generate_latex_cv, compile_latex_cv
from src.params import CVParams
from src.cleaner import clean_folder

from pathlib import Path
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate and compile a CV in LaTeX.")

    parser.add_argument("--use-emojis", action="store_true", help="Use emojis in the CV")
    parser.add_argument("--merge-contact-header", action="store_true", help="Merge contact and header sections")
    parser.add_argument("--offer-file", type=str, default=None, help="Path to the offer file")
    parser.add_argument("--max-activities", type=int, default=5, help="Maximum number of activities to include in the CV")
    parser.add_argument("--cv-style", type=str, default="modern", help="Style of the CV (e.g., modern, classic)")
    parser.add_argument("--cv-language", type=str, default="en", help="Language of the CV (e.g., en, fr)")
    parser.add_argument("--cv-name", type=str, default="cv", help="Name of the output CV file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    job_offer_file = Path(args.offer_file) if args.offer_file else None
    if job_offer_file is None:
        job_desc = None
    elif job_offer_file.exists():
        job_desc = args.offer_file = str(job_offer_file.resolve())

    params = CVParams(
        **args.__dict__,
        github_logo="../rsc/github_logo.png",
        linkedin_logo="../rsc/linkedin_logo.png",
        user_pic="../rsc/cv.png",
        emoji_font="AppleColorEmoji.ttf",
        emoji_dir="./../rsc/",
        cv_folder="out_dir",
    )
    latex_cv = generate_latex_cv(params, job_description=job_desc)
    compile_latex_cv(params)
    clean_folder(params)
