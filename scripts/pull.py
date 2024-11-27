from .utils import iter_modules, system


def main():
    system("git", "pull")

    for p in iter_modules():
        system("git", "pull", cwd=str(p))

    # system("pdm install -G:all")
