import re
import subprocess


cases = {
    "Changes to appliation only": (
        "b3798f31ebe3632b1624124bae9b3319aca23554",
        "84d487ee66578b37204a64dce4e3d6b5521eb6ea"
    ),
    "Changes to both app and import scripts": (
        "b3798f31ebe3632b1624124bae9b3319aca23554",
        "6976d5f23850956e4af425e9d27b3a651a718e4d"
    ),
    "Changes to import script only": (
        "6976d5f23850956e4af425e9d27b3a651a718e4d",
        "84d487ee66578b37204a64dce4e3d6b5521eb6ea"
    )
}


def get_paths_changed(from_sha, to_sha):
    args = ["git", "diff", "--name-only", from_sha, to_sha]
    output = subprocess.check_output(args)
    return output.decode().splitlines()

def is_import_script(path):
    if re.search("import_[^\.]+\.py", path):
        return True
    return False

def any_import_scripts(changed):
    return any(is_import_script(path) for path in changed)

def any_non_import_scripts(changed):
    return any(not is_import_script(path) for path in changed)

def should_run_import_scripts(from_sha, to_sha, post_deploy=False):
    changed = get_paths_changed(*shas)
    has_imports = any_import_scripts(changed)
    has_appliation = any_non_import_scripts(changed)
    if has_appliation and not post_deploy:
        return "Not running import scripts, needs deploy"
    if has_imports and not has_appliation and not post_deploy:
        return "Just running import scripts"
    if has_imports and has_appliation and post_deploy:
        return "Finished deploy, running import scripts"
    if not has_imports and post_deploy:
        return "A deploy happened and nothing else is left to be done"

for case, shas in cases.items():
    for job in ("First run", "Second run"):
        print(f"{case}: {job}")
        kwargs = {"post_deploy": False}
        if job == "Second run":
            kwargs["post_deploy"] = True
        out = should_run_import_scripts(*shas, **kwargs)
        print(f"\t{out}")
    print()

