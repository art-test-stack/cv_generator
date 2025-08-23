from pathlib import Path

class CVParams:
    def __init__(
            self, 
            logo_width="0.38cm", 
            github_logo="github_logo.png", 
            linkedin_logo="linkedin_logo.png",
            user_pic="user_pic.png",
            emoji_font="AppleColorEmoji.ttf",
            emoji_dir="./rsc/",
            use_emojis=True,
            data_dir="data/",
            cv_language="en",
            cv_folder="output_dir",
            cv_name="cv",
            merge_contact_header=True,
            sentence_tf_model="all-MiniLM-L6-v2",
            two_columns=False,
            max_activities=5,
            cv_style="modern",
            font_size="10pt",
            rsc_dir="rsc",
            max_projects=3,
            availability=True,
            **kwargs
        ):
        # Input parameters
        self.data_dir = Path(data_dir) / cv_language
        self.cv_language = cv_language
        self.latex_template_dir = f"data/latex"

        # Section inclusion parameters
        self.sentence_tf_model = sentence_tf_model
        self.max_activities = max_activities
        self.max_exp_highlights = 4
        self.max_edu = 4
        self.max_skills = 7
        if cv_style == "classic":
            max_projects = 2
        if cv_style == "modernus":
            max_projects = 4
        self.max_projects = max_projects
        self.selection_mode = "top_k"

        # Layout parameters
        self.availability = availability
        self.logo_width = logo_width
        self.github_logo = github_logo
        self.linkedin_logo = linkedin_logo
        self.pic = user_pic
        self.use_emojis = use_emojis
        self.merge_contact_header = merge_contact_header
        self.two_columns = two_columns
        self.cv_style = cv_style

        self.font_size = font_size or "10pt"
        self.left_col_width = "0.38"
        self.col_sep = "0.05"
        self.emoji_font = emoji_font
        self.emoji_dir = emoji_dir
        self.width_len = "1.4in"
        self.side_margin = "-0.7in"
        self.text_width = "1.4in"
        self.top_margin = "-0.5in" if cv_language == "en" else "-0.8in"
        self.text_height = "1.4in"

        # Paths for CV output
        self.cv_folder = cv_folder
        self.cv_name = cv_name


