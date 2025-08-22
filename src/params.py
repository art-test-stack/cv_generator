
class CVParams:
    def __init__(
            self, 
            logo_width=0.38, 
            github_logo="github_logo.png", 
            linkedin_logo="linkedin_logo.png",
            use_emojis=True,
            cv_folder="",
            cv_name="cv",
            merge_contact_header=False,
            minipages=False
        ):
        self.logo_width = logo_width
        self.github_logo = github_logo
        self.linkedin_logo = linkedin_logo
        self.use_emojis = use_emojis
        self.merge_contact_header = merge_contact_header
        self.minipages = minipages
        
        # Paths for CV output
        self.cv_folder = cv_folder
        self.cv_name = cv_name


