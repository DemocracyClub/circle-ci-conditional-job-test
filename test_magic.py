from magic import should_run_import_scripts

cases = {
    "Changes to application only": (
        "b3798f31ebe3632b1624124bae9b3319aca23554",
        "84d487ee66578b37204a64dce4e3d6b5521eb6ea",
    ),
    "Changes to both app and import scripts": (
        "b3798f31ebe3632b1624124bae9b3319aca23554",
        "6976d5f23850956e4af425e9d27b3a651a718e4d",
    ),
    "Changes to import script only": (
        "6976d5f23850956e4af425e9d27b3a651a718e4d",
        "84d487ee66578b37204a64dce4e3d6b5521eb6ea",
    ),
}


for case, shas in cases.items():
    for job in ("First run", "Second run"):
        print(f"{case}: {job}")
        kwargs = {"post_deploy": False}
        if job == "Second run":
            kwargs["post_deploy"] = True
        out = should_run_import_scripts(*shas, **kwargs)
        print(f"\t{out}")
    print()
