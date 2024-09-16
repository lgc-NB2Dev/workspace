from .utils import iter_modules, system, system_no_fail


def main():
    for p in iter_modules():
        system_no_fail("git", "add", ".", cwd=str(p))
        if not system("git", "commit", "-m", "up", cwd=str(p)):
            system_no_fail("git", "pull", cwd=str(p))
            system_no_fail("git", "push", cwd=str(p))

    system_no_fail("git", "add", ".")
    if not system_no_fail("git", "commit", "-m", "up"):
        system_no_fail("git", "pull")
        system_no_fail("git", "push")
