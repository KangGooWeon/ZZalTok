from config import config


def convert_path_to_url(path: str, base_url: str, base_path: str = config.root) -> str:
    idx = path.find(base_path)
    idx = (0 if idx == -1 else idx + len(base_path))
    return (base_url if base_url.endswith('/') else base_url + '/') + path[idx:]
