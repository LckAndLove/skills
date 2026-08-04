---
name: git-commit-convention
description: Create, review, and improve Git commit messages using the Conventional Commits format. Use when preparing commits, choosing a commit type or scope, describing staged changes, documenting breaking changes, or checking commit history for consistency. For Chinese-language repositories, keep commit subjects, bodies, and migration notes in Simplified Chinese while retaining conventional types and scopes in English.
---

# Git Commit Convention

Use Conventional Commits to make history clear, searchable, and automation-friendly.

## Format

```text
<type>[optional scope][!]: <short imperative description>

[optional body]

[optional footer(s)]
```

Keep `type` and `scope` in the conventional English form, such as `feat(uart)`. For Chinese-language projects, write the subject, body, and migration notes in Simplified Chinese so users can understand the history. Keep technical names, API names, commands, and identifiers unchanged. Keep the subject concise, use an imperative/action-oriented description, and omit the final period.

## Types

- `feat`: add user-visible functionality
- `fix`: correct a defect
- `docs`: documentation only
- `style`: formatting or non-functional style changes
- `refactor`: restructure without behavior change
- `perf`: improve performance
- `test`: add or change tests
- `build`: change build system or dependencies
- `ci`: change CI/CD configuration
- `chore`: maintenance with no product behavior change
- `revert`: reverse an earlier commit

Choose the most specific type. Do not use `chore` when `docs`, `test`, `build`, or `ci` is more accurate.

## Scope and breaking changes

- Add a scope when it identifies the affected module, package, or feature: `fix(parser): 拒绝空输入`.
- Add `!` before the colon for a breaking change: `feat(api)!: remove legacy token format`.
- Explain the migration in the body or a `BREAKING CHANGE:` footer.
- Mention issue IDs in footers when the repository requires them; do not put noisy metadata in the subject.

## Workflow

1. Inspect the staged diff and verify that unrelated files are not staged.
2. Summarize the actual behavior change, not the implementation activity.
3. Select one primary type and an optional scope.
4. Prefer small, frequent commits. Commit an independent small change as soon as it is complete instead of accumulating many unrelated changes.
5. Write one commit for one cohesive change. Split unrelated changes before committing; combine changes only when they are tightly coupled and cannot be safely separated.
6. Add body details only when rationale, compatibility, testing, or migration guidance is useful.
7. If the user asks to commit, show or use the proposed message and then verify the commit result.

## Examples

```text
feat(uart): 新增非阻塞接收 API
fix: 防止缓冲区索引溢出
docs: 补充本地开发环境说明
refactor(driver): 隔离寄存器访问
test: 覆盖超时恢复场景
feat(config)!: 删除旧版 YAML 配置键

BREAKING CHANGE: 将 `device.port` 重命名为 `device.endpoint`。
```

Do not claim tests passed unless they were actually run. Do not create a commit merely because a message was requested; distinguish drafting, reviewing, and executing a commit.
