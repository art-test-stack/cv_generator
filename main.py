from src.generate_cv import generate_latex_cv, compile_latex_cv
from src.params import CVParams


if __name__ == "__main__":
    params = CVParams(
        github_logo="rsc/github_logo.png",
        linkedin_logo="rsc/linkedin_logo.png",
        user_pic="rsc/cv.png",
        emoji_font="AppleColorEmoji.ttf",
        emoji_dir="./rsc/",
        cv_folder="out_dir",
    )
    latex_cv = generate_latex_cv(params)
    compile_latex_cv(params)
