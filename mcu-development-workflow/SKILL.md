---
name: mcu-development-workflow
description: Plan, execute, and review the complete development lifecycle for microcontroller firmware. Use for new MCU projects, legacy firmware changes, board bring-up, BSP and driver development, RTOS or middleware integration, application implementation, debugging, testing, release preparation, and maintenance planning.
---

# MCU Development Workflow

Use a user-aligned closed loop as a recommended guide, with a checkpoint before each phase when the project needs it. Adapt the tools to the MCU, compiler, IDE, RTOS, code generator, hardware, and safety requirements. For a legacy project, preserve the existing structure and build process unless a real risk justifies change. User instructions and project rules take precedence over this workflow.

## User-aligned closed-loop process

```text
Goal alignment → Change plan → User approval → Implementation
→ Build review → Board/serial test → Final review → Git commit
                                      ↑                    ↓
                                      └── fix or safe rollback
```

1. **Planning:** confirm the user's goal, expected result, scope, constraints, and acceptance criteria. Resolve ambiguity and align on the purpose before proposing implementation when clarification is needed.
2. **Change plan:** write a concrete plan listing files/modules affected, intended behavior, validation steps, risks, and rollback approach. Normally wait for user approval before making a material change, unless the user has already clearly authorized implementation.
3. **Execution:** implement the agreed scope. Prefer small, traceable changes that remain consistent with the existing project structure.
4. **Build check:** compile after implementation when possible. Aim for zero errors and zero warnings in user-owned code. Record existing library/vendor warnings as exceptions, and fix new user-code warnings when practical.
5. **Hardware check:** if a development board is connected, program it and verify the result when relevant. If the corresponding serial device is connected, use the available serial MCP tool to run the relevant connection or behavior test.
6. **Final review:** compare the actual diff and test evidence with the plan. Confirm that the change is complete, appropriately scoped, and unlikely to introduce known regressions.
7. **Commit:** when the change is ready, prefer a focused commit containing only the reviewed change. Follow the repository's commit convention.
8. **Recovery loop:** if a check fails, explain the failure, fix it, and repeat the affected validation. If the change cannot be made safe, consider a confirmed, recoverable rollback and report what was reverted.

When reporting progress, distinguish passed, failed, skipped, and unverified checks. If a board, serial port, compiler, or MCP tool is unavailable, record the limitation instead of implying that the test succeeded.

## 1. Establish context

Collect and record:

- MCU, board revision, clock source, memory map, peripherals, pin map, power, and external devices.
- Product requirements, operating modes, timing limits, error behavior, update method, and acceptance criteria.
- Toolchain, compiler version, IDE/project generator, SDK/HAL, RTOS, coding standard, static analysis, and supported configurations.
- Repository state, existing build command, programming/debug probe, test hardware, and known limitations.

Prefer to clarify the target hardware, build entry point, and success criteria before implementation. Mark unknowns as risks instead of guessing.

## 2. Define architecture

Separate responsibilities into:

```text
Application → Components/Middleware → Drivers → BSP/HAL → MCU hardware
```

Define module interfaces, ownership, data flow, task/ISR boundaries, timing budgets, memory strategy, error handling, configuration sources, and initialization order. Choose a directory structure before adding many files.

For RTOS projects, define threads, priorities, stack budgets, IPC objects, blocking rules, and interrupt-to-thread handoff. For bare-metal projects, define the super-loop and interrupt scheduling model.

## 3. Create or classify the project

- **New project:** use the project structure and naming rules from the start; configure source groups, include paths, linker settings, warnings, and reproducible build commands.
- **Legacy project:** map the current structure, build inputs, generated code, and dependencies first. Make small compatible changes; do not reorganize solely for appearance.
- **Generated project:** preserve the generator's files and configuration source. Put custom code in protected sections only when necessary and keep project-owned modules outside generated/vendor directories.

Record the initial project configuration and how to build and program it. Prefer committing it after the build, review, and relevant validation checks are complete.

## 4. Bring up the board

Prove the smallest foundation in this order:

1. Reset/startup and vector table.
2. Clock and power assumptions.
3. GPIO and a visible health signal.
4. Debug console or trace output.
5. Timer/time base and watchdog policy.
6. Required memory, storage, and communication peripherals.

At each step, record the binary, configuration, measurement, and observed result. Keep board bring-up code separate from product behavior.

## 5. Implement in layers

1. **BSP/HAL:** startup, clocks, pins, linker configuration, low-level board services.
2. **Drivers:** hardware initialization, register access, interrupts, DMA, state, timeouts, and device interfaces.
3. **Components/Middleware:** protocols, filesystems, services, codecs, logging, and reusable adapters.
4. **Application:** product state machines, commands, tasks, business rules, and user-visible behavior.

Keep dependencies downward. Define every public interface with input ranges, ownership, blocking behavior, return values, timing, and thread/ISR safety.

## 6. Validate continuously

Run the smallest useful validation after each change:

- Compile with strict warnings and check the complete build log.
- Run unit tests for pure logic and boundary conditions.
- Run driver and integration tests on real hardware or a hardware-in-the-loop setup.
- Test reset, timeout, invalid input, communication loss, low memory, watchdog recovery, and power-cycle behavior.
- Use static analysis, code review, map-file inspection, stack/heap measurements, and timing measurements where relevant.
- Record tool versions, configuration, test result, and remaining limitation.

Never treat “it compiles” as proof of hardware correctness.

## 7. Debug systematically

Reproduce the issue, reduce it to the smallest failing path, and classify it as build, startup, hardware, timing, memory, concurrency, protocol, or application behavior. Capture logs, registers, stack traces, waveforms, and exact firmware/configuration versions. Fix the root cause, add a regression test or diagnostic, and re-run affected validation.

## 8. Release and maintain

Before release, verify:

- Clean reproducible build and correct target configuration.
- Firmware image, checksum/version, linker map, memory usage, and programming procedure.
- Hardware revision, bootloader/update path, default configuration, and rollback or recovery path.
- Test evidence, known issues, release notes, and source/toolchain revision.

Keep changes small and traceable. Update architecture, interface, configuration, and recovery documentation when behavior changes.

## Review gate

For a workflow review, report the current phase, missing evidence, blocking risk, next action, owner, and suggested exit criterion. Consider resolving startup, hardware assumptions, build reproducibility, and failure recovery before advancing to application features, unless the project deliberately accepts the risk.
