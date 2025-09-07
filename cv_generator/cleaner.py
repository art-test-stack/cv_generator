from .params import CVParams
import pathlib
import shutil

def clean_workspace(params: CVParams):
    print("Cleaning workspace...")
    folder = pathlib.Path(params.cv_folder)
    for item in folder.iterdir():
        if item.is_file() and item.suffix != '.pdf':
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)