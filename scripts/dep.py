from .utils import iter_packages, ok, system


def main():
    for p in iter_packages():
        if ok(
            system(
                *("pdm", "update", "-G:all", "-u", "--no-self"),
                check=False,
                cwd=str(p),
            ),
        ):
            system("pdm", "lock", "-G:all", "--no-self", cwd=str(p))
            system("pdm", "update", "-G:all", "--no-self", "-u", cwd=str(p))

    # system("pdm", "lock", "-G:all")
    system("pdm", "update", "-G:all", "-u")
