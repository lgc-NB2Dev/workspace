from .utils import iter_packages, system, system_no_fail


def main():
    for p in iter_packages():
        if system("pdm", "update", "-G:all", "-u", "--no-self", cwd=str(p)):
            system_no_fail("pdm", "lock", "-G:all", "--no-self", cwd=str(p))
            system_no_fail("pdm", "update", "-G:all", "--no-self", "-u", cwd=str(p))

    # system_no_fail("pdm", "lock", "-G:all")
    system_no_fail("pdm", "update", "-G:all", "-u")
