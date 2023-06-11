import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
test_resources = current_path / "resources"


def mock_get_html(url: str) -> str:
    filename = f"{url.replace('/', '-')}.html"
    html = get_test_resource_text(filename)
    return html


def get_test_resource(filename: str) -> Path:
    return test_resources / filename


def get_test_resource_text(filename: str) -> str:
    return get_test_resource(filename).read_text()
