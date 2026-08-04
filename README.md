# 技能仓库

用于嵌入式开发、项目结构、代码规范、开发流程和 Git 工作流的可复用 Codex 技能集合。

## 已收录技能

| 技能 | 用途 |
|---|---|
| [`embedded-c-coding-standard`](./embedded-c-coding-standard) | 基于 MISRA C、CERT C 和嵌入式工程实践，编写和审查 C 代码。 |
| [`git-commit-convention`](./git-commit-convention) | 创建和审查 Conventional Commits。提交类型和作用域使用英文，提交描述使用简体中文。 |
| [`keil-build-flash`](./keil-build-flash) | 使用 UV4.exe 编译和烧录 Keil MDK 工程，并处理路径配置和临时日志。 |
| [`keil-project-structure`](./keil-project-structure) | 规范 Keil 工程目录、文件命名、代码归属和依赖关系，并兼容旧项目与 CubeMX 工程。 |
| [`mcu-development-workflow`](./mcu-development-workflow) | 指导单片机从目标确认、计划、开发、编译、测试、审查到提交的完整流程。 |
| [`rtthread-layered-development`](./rtthread-layered-development) | 按应用层、中间件、驱动、BSP 和内核边界设计和审查 RT-Thread 代码。 |

## 仓库结构

每个技能都是一个独立目录：

```text
skill-name/
├── SKILL.md          # 技能说明和触发描述
└── agents/
    └── openai.yaml   # 界面元数据
```

如果技能需要可复用资源，可以增加 `references/`、`scripts/` 或 `assets/` 目录。

## 开发流程

1. 创建或更新一个技能目录。
2. 保持每次修改目标单一，并使用小步提交。
3. 提交前验证技能：

   ```powershell
   $env:PYTHONUTF8 = '1'
   python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skill-name
   ```

4. 检查差异后提交，需要时再推送到远程仓库。
