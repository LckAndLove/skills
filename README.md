# Skills

Reusable Codex skills for embedded development, coding standards, and Git workflows.

## Included skills

| Skill | Purpose |
|---|---|
| [`embedded-c-coding-standard`](./embedded-c-coding-standard) | Review and write embedded C using MISRA C, CERT C, and practical firmware conventions. |
| [`git-commit-convention`](./git-commit-convention) | Create and review Conventional Commits. Use English types/scopes and Simplified Chinese commit descriptions for Chinese-language repositories. |
| [`keil-build-flash`](./keil-build-flash) | Build and flash Keil MDK projects with UV4.exe, including path configuration and temporary logs. |
| [`rtthread-layered-development`](./rtthread-layered-development) | Design and review RT-Thread code according to application, middleware, driver, BSP, and kernel boundaries. |

## Repository structure

Each skill is a self-contained directory:

```text
skill-name/
├── SKILL.md          # Skill instructions and trigger description
└── agents/
    └── openai.yaml   # UI metadata
```

Additional `references/`, `scripts/`, or `assets/` directories may be added when a skill needs reusable resources.

## Development workflow

1. Create or update one skill directory.
2. Keep each change focused and use small commits.
3. Validate the skill before committing:

   ```powershell
   $env:PYTHONUTF8 = '1'
   python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skill-name
   ```

4. Review the diff, commit, and push when ready.
