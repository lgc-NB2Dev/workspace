from .utils import iter_packages, system, system_no_fail


def main():
    system_no_fail("git", "pull")

    for p in iter_packages():
        system_no_fail("git", "pull", cwd=str(p))
        if not system("git", "add", ".", cwd=str(p)):
            system_no_fail("git", "commit", "-m", "up", cwd=str(p))
            system_no_fail("git", "push", cwd=str(p))

    if not system_no_fail("git", "add", "."):
        system_no_fail("git", "commit", "-m", "up")
        system_no_fail("git", "push")
