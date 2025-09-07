from .params import CVParams
from .generate_cv import generate_latex_cv, compile_latex_cv
from .cleaner import clean_workspace
from .get_params import get_params
from .schemas import JobFormatting
from typing import Optional, Dict
from pathlib import Path


class CVPipeline:
    def __init__(
            self, 
            offer_file: Optional[str] = None, 
            params: Optional[Dict] = {}, 
            offer_dict: Optional[Dict] = None
        ):
        if not params:
            params = {}
        if offer_file:
            self.job_offer_file = Path(offer_file) if offer_file else None
            self.job_description = self.job_offer_file.read_text() if self.job_offer_file and self.job_offer_file.exists() else None
        elif offer_dict:
            self.job_offer_file = JobFormatting(**offer_dict)
            self.job_description = offer_dict['description']
            self.job_offer_file.stem = offer_dict.get('id', 'generated_cv')
        else: 
            self.job_offer_file = None
            self.job_description = None

        directory = Path(".cv_generator")
        if not directory.exists():
            directory.mkdir()
            
        # if self.job_offer_file is None:
        #     job_desc = None
        # elif self.job_offer_file.exists():
        #     job_desc = str(self.job_offer_file.resolve())
        params = params | get_params(self.job_description) # job_desc
        params["cv_name"] = self.job_offer_file.stem if self.job_offer_file else "generated_cv"
        emoji_dir = str((Path(__file__).parent.parent / "rsc").resolve()) + "/"
        emoji_dir = "./../rsc/" 

        current_path=Path.cwd() / ".cv_generator"
        if not current_path.exists():
            current_path.mkdir(parents=True, exist_ok=True)
        
        self.params = CVParams(
            github_logo=str((Path(__file__).parent / "../rsc/github_logo.png").resolve()),
            linkedin_logo=str((Path(__file__).parent / "../rsc/linkedin_logo.png").resolve()),
            user_pic=str((Path(__file__).parent / "../rsc/cv.png").resolve()),
            emoji_font="AppleColorEmoji.ttf",
            # emoji_font=str((Path(__file__).parent / "../rsc/AppleColorEmoji.ttf").resolve()),
            emoji_dir=emoji_dir[1:] if emoji_dir.startswith("/") else emoji_dir,
            data_dir=str((Path(__file__).parent / "../data").resolve()),
            latex_template_dir=str((Path(__file__).parent / "../data/latex").resolve()),
            # github_logo="./../rsc/github_logo.png",
            # linkedin_logo="./../rsc/linkedin_logo.png",
            # user_pic="./../rsc/cv.png",
            # emoji_font="AppleColorEmoji.ttf",
            # emoji_dir="./../rsc/",
            # cv_folder=str((Path(__file__).parent / "../out_dir").resolve()),
            cv_folder=str(current_path.resolve() / params["cv_name"]),
            **params
        )

    def make_cv(self):
        print("Generating CV...")
        print(self.params.cv_folder)
        latex_cv = generate_latex_cv(self.params, job_description=self.job_description)
        compile_latex_cv(self.params, quite=True)
        clean_workspace(self.params)


    def get_pdf_bytes(self) -> Optional[str]:
        output_pdf = Path(self.params.cv_folder) / f"{self.params.cv_name}.pdf"
        if output_pdf.exists():
            return output_pdf.read_bytes()
        return None

    def get_pdf_path(self) -> Optional[str]:
        output_pdf = Path(self.params.cv_folder) / f"{self.params.cv_name}.pdf"
        if output_pdf.exists():
            return str(output_pdf)
        return None

    def get_all_cv_generated(self) -> bool:
        output_pdf = Path(self.params.cv_folder)
        return [str(pdf) for pdf in output_pdf.glob("*.pdf")]