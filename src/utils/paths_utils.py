import os

def get_project_root():
    current_file = os.path.abspath(__file__)
    utils_dir = os.path.dirname(current_file)      # src/utils/
    src_dir = os.path.dirname(utils_dir)           # src/
    project_root = os.path.dirname(src_dir)        # project root
    return project_root


def get_config_path(filename=".env"):
    return os.path.join(get_project_root(), "config", filename)


def get_prompts_path(filename):
    return os.path.join(get_project_root(), "prompts", filename)


def get_outputs_path(filename):
    return os.path.join(get_project_root(), "outputs", filename)


def get_data_path(filename):
    return os.path.join(get_project_root(), "data", filename)

def get_sounds_path(filename):
    return os.path.join(get_project_root(), "sounds", filename)

def get_photos_path(filename):
    return os.path.join(get_project_root(), "photos", filename)