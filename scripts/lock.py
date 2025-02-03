from .utils import iter_packages, system


def main():
    for p in iter_packages():
        system("pdm", "lock", "-G:all", cwd=str(p))

    system("pdm", "lock", "-G:all")
