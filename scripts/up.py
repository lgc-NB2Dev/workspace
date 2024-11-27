from .utils import iter_modules, system


def main():
    for p in iter_modules():
        system("git", "add", ".", cwd=str(p))
        if not system("git", "commit", "-m", "up", check=False, cwd=str(p)):
            system("git", "pull", cwd=str(p))
            system("git", "push", cwd=str(p))

    system("git", "add", ".")
    if not system("git", "commit", "-m", "up"):
        system("git", "pull")
        system("git", "push")
