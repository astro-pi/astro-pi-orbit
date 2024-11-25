from pathlib import Path
import subprocess
import platform
import shutil
from typing import Optional, Union

CURRENT_DIR = Path(__file__).parent
PROJECT_DIR = CURRENT_DIR.parent
VENV_DIR = PROJECT_DIR / "venv"

PYTHON_SYNONYMS = ["python3", "python"]
PIP_SYNONYMS = ["pip3", "pip"]


class ResolvedVenv:
    venv_dir: Path
    scripts_dir: Path
    pip: Path
    python: Path
    pytest: Path

    def __init__(self, venv_dir: Path) -> None:
        self.venv_dir: Path = venv_dir
        if platform.system == "Windows":
            self.scripts_dir = VENV_DIR / "Scripts"
            get_script_name = lambda x: f"{x}.exe"  # noqa: E731

        else:
            self.scripts_dir = VENV_DIR / "bin"
            get_script_name = lambda x: x  # noqa: E731

        found_pip = None
        for pip in PIP_SYNONYMS:
            pip_path = self.scripts_dir / get_script_name(pip)
            if pip_path.exists():
                found_pip = pip_path
        if not found_pip:
            raise RuntimeError("Couldn't find pip")
        self.pip = found_pip

        found_python = None
        for python in PYTHON_SYNONYMS:
            python_path = self.scripts_dir / get_script_name(python)
            if python_path.exists():
                found_python = python_path
        if not found_python:
            raise RuntimeError("Couldn't find python")
        self.python = found_python

    def install(
        self,
        dependency: Optional[str] = None,
        requirements_txt: Optional[Union[str, Path]] = None,
    ):
        args: list[str] = [str(self.pip), "install"]
        if requirements_txt:
            args.extend(["-r", str(requirements_txt)])
        elif dependency:
            args.append(dependency)
        else:
            raise RuntimeError(
                "Please specify either a dependency "
                + "to install or a requirements.txt file"
            )
        subprocess.run(args, check=True, text=True)


def find_python() -> str:
    synonyms = [python for python in PYTHON_SYNONYMS if shutil.which]
    if len(synonyms) == 0:
        raise RuntimeError("Couldn't find Python")
    return synonyms[0]


def prepare_venv(python: str) -> ResolvedVenv:
    if not VENV_DIR.exists():
        subprocess.run([python, "-m", "venv", str(VENV_DIR)], text=True, check=True)

        venv = ResolvedVenv(VENV_DIR)
        venv.install(requirements_txt=PROJECT_DIR / "requirements-dev.txt")
    else:
        venv = ResolvedVenv(VENV_DIR)

    return venv


def run_tests(venv: ResolvedVenv):
    subprocess.run(
        [str(venv.scripts_dir / "pytest")], cwd=PROJECT_DIR, check=True, text=True
    )


def run_build(venv: ResolvedVenv):
    subprocess.run(
        [str(venv.python), "-m", "build"], cwd=PROJECT_DIR, check=True, text=True
    )


if __name__ == "__main__":
    venv: ResolvedVenv = prepare_venv(find_python())
    run_tests(venv)
    run_build(venv)
