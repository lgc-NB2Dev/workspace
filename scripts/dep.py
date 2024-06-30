from .utils import iter_packages, system_no_fail


def main():
    for p in iter_packages():
        system_no_fail("pdm", "install", "-G:all", "-u", cwd=str(p))

    system_no_fail("pdm", "install", "-G:all", "-u")
