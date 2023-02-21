import argparse
import json
import os
import re
import subprocess
import sys
import http.client


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


def should_run_import_scripts(from_sha, to_sha, action):
    changed = get_paths_changed(from_sha, to_sha)
    has_imports = any_import_scripts(changed)
    has_application = any_non_import_scripts(changed)
    if has_application and action != "post_deploy":
        sys.stdout.write("Not running import scripts, needs deploy\n")
        return False
    if (
        has_imports
        and not has_application
        and action not in ["post_deploy", "exit_early"]
    ):
        sys.stdout.write("Just running import scripts\n")
        return True
    if has_imports and has_application and action == "post_deploy":
        sys.stdout.write("Finished deploy, running import scripts\n")
        return True
    if not has_imports and action == "post_deploy":
        sys.stdout.write("A deploy happened and nothing else is left to be done\n")
        return False
    if has_imports and not has_application and action == "exit_early":
        return True


# def stop_ci_workflow():
#     CIRCLE_TOKEN = os.environ.get("CIRCLE_TOKEN")
#     CIRCLE_WORKFLOW_ID = os.environ.get("CIRCLE_WORKFLOW_ID")
#     conn = http.client.HTTPSConnection("circleci.com")
#     headers = {"Circle-Token": CIRCLE_TOKEN}
#     conn.request("POST", f"/api/v2/workflow/{CIRCLE_WORKFLOW_ID}/cancel", headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))


def stop_job():
    args = ["circleci-agent", "step", "halt"]
    subprocess.check_output(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ImportScriptRunner",
        description="""
            Checks the files changed between two GIT commits
            and decides if import scripts should be run
            """,
    )
    parser.add_argument("from_sha")
    parser.add_argument("to_sha")
    parser.add_argument(
        "--action",
        action="store",
        choices=["run_imports", "exit_early", "post_deploy"],
    )
    args = parser.parse_args()
    print(args)
    should_run = should_run_import_scripts(args.from_sha, args.to_sha, args.action)
    if should_run and args.action == "run_imports":
        print("Running import scripts")
    if should_run and args.action == "exit_early":
        stop_job()
    if should_run and args.action == "post_deploy":
        print("Running import scripts")
