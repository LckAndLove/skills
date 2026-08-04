"""Validate the basic structure and metadata of every skill in this repository."""

from pathlib import Path
import re
import sys

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    name = skill_dir.name
    if not NAME_PATTERN.fullmatch(name):
        fail(f"invalid skill directory name: {name}", errors)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(f"missing SKILL.md: {skill_dir}", errors)
        return

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"missing frontmatter: {skill_md}", errors)
        return

    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"invalid frontmatter terminator: {skill_md}", errors)
        return

    try:
        frontmatter = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as exc:
        fail(f"invalid YAML in {skill_md}: {exc}", errors)
        return

    if frontmatter.get("name") != name:
        fail(f"frontmatter name does not match directory: {skill_md}", errors)
    if not isinstance(frontmatter.get("description"), str) or not frontmatter["description"].strip():
        fail(f"missing description: {skill_md}", errors)

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        return
    try:
        interface = (yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}).get("interface", {})
    except yaml.YAMLError as exc:
        fail(f"invalid YAML in {openai_yaml}: {exc}", errors)
        return
    for key in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            fail(f"missing interface.{key}: {openai_yaml}", errors)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skills = sorted(
        path for path in root.iterdir()
        if path.is_dir() and not path.name.startswith((".", "_")) and path.name not in {"scripts", "examples"}
    )
    if not skills:
        fail("no skill directories found", errors)
    for skill_dir in skills:
        validate_skill(skill_dir, errors)

    if errors:
        print("Skill validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Validated {len(skills)} skill(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
