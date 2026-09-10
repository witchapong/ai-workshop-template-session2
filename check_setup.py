r"""Run this before the first session:  .venv\Scripts\python.exe check_setup.py

It checks four things and tells you exactly what to fix if any of them fail.
Do not come to class until this prints "ALL CHECKS PASSED".
"""

import os
import sys

PLACEHOLDER = "paste-your-key-here"
# The department supplies one key. Students no longer sign up for anything,
# which removes the setup failure that cost Session 1 half the room.
ZAI_BASE = "https://api.z.ai/api/coding/paas/v4"
ZAI_MODEL = "glm-5.3-flash"
REQUIRED_PACKAGES = ["streamlit", "numpy", "matplotlib", "dotenv", "pytest"]


def check_python_version() -> tuple[bool, str]:
    """Python must be 3.14 or newer."""
    major, minor = sys.version_info[:2]
    found = f"{major}.{minor}"
    if (major, minor) >= (3, 14):
        return True, f"Python {found}"
    return False, (
        f"Python {found} is too old. This project needs 3.14 or newer. "
        r"Delete the .venv folder and rebuild it with:  py -3.14 -m venv .venv"
    )


def check_imports() -> tuple[bool, str]:
    """Every required package must be importable."""
    import importlib

    missing = []
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
    if not missing:
        return True, f"All {len(REQUIRED_PACKAGES)} packages installed"
    return False, (
        f"Missing packages: {', '.join(missing)}. "
        r"Fix it by running:  .venv\Scripts\python.exe -m pip install -r requirements.txt"
    )


def check_env(environ: dict[str, str]) -> tuple[bool, str]:
    """The departmental key must be set."""
    value = (environ.get("ZAI_API_KEY") or "").strip()
    if value and value != PLACEHOLDER:
        return True, "ZAI_API_KEY is set"
    if value == PLACEHOLDER:
        return False, (
            f"ZAI_API_KEY still contains the placeholder text. Open .env and "
            f"replace '{PLACEHOLDER}' with the key on the projector."
        )
    return False, (
        "No API key found. Copy .env.example to .env with:  copy .env.example .env"
        "  then paste the key on the projector into ZAI_API_KEY."
    )


def check_live_call() -> tuple[bool, str]:
    """Actually call the model. A key that is set but wrong fails here."""
    import json
    import urllib.error
    import urllib.request

    key = (os.environ.get("ZAI_API_KEY") or "").strip()
    if not key or key == PLACEHOLDER:
        return False, "No key to test with. Fix the check above first."
    body = json.dumps({
        "model": ZAI_MODEL,
        "messages": [{"role": "user", "content": "say OK"}],
        "max_tokens": 600,
    }).encode()
    request = urllib.request.Request(
        f"{ZAI_BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            json.load(response)
        return True, f"{ZAI_MODEL} replied"
    except urllib.error.HTTPError as error:
        if error.code == 429:
            return False, (
                "The key is busy or out of credit. If check_setup passed for "
                "the person next to you, wait ten seconds and run it again."
            )
        if error.code in (401, 403):
            return False, (
                "The key was rejected. Open .env and check you copied the whole key, "
                "then run this again."
            )
        return False, (
            f"The model refused: HTTP {error.code}. Wait ten seconds and run this "
            f"again. If it keeps happening, tell the instructor."
        )
    except Exception as error:                       # noqa: BLE001
        return False, (
            f"Could not reach {ZAI_BASE}. Campus wifi may be blocking it. Try a phone "
            f"hotspot, or tell the instructor, then run this again. ({error})"
        )


def main() -> int:
    from dotenv import load_dotenv

    load_dotenv()

    # Each check runs and prints in turn. Building the list eagerly meant the
    # network call happened before ANY line was printed, so the terminal sat
    # blank for ten or twenty seconds and read as a hang. It is the first thing
    # a student ever runs; it has to look alive.
    checks = [
        ("Python version", check_python_version),
        ("Packages", check_imports),
        ("API key present", lambda: check_env(dict(os.environ))),
        ("API key works", check_live_call),
    ]

    print()
    all_passed = True
    for label, run in checks:
        if label == "API key works":
            print("  ...  asking a provider to answer. This takes a few seconds.",
                  flush=True)
        passed, message = run()
        mark = "PASS" if passed else "FAIL"
        print(f"[{mark}] {label}: {message}", flush=True)
        all_passed = all_passed and passed

    print()
    if all_passed:
        print("ALL CHECKS PASSED")
        return 0
    print("Some checks failed. Fix the items marked FAIL above, then run this again.")
    print("Still stuck after 10 minutes? See TROUBLESHOOTING.md")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
