from .utils import iter_modules, system_no_fail


def main():
    system_no_fail("git", "pull")

    for p in iter_modules():
        system_no_fail("git", "pull", cwd=str(p))

    # system_no_fail("pdm install -G:all")
