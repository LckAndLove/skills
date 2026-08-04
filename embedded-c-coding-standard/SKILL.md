---
name: embedded-c-coding-standard
description: Apply concise, industry-standard embedded C guidance when writing or reviewing firmware, drivers, HALs, ISRs, RTOS code, bootloaders, and .c/.h files. Inherit MISRA C as the primary baseline, use CERT C for security, and use Barr Group Embedded C conventions for practical style. Do not claim formal compliance without project evidence.
---

# Embedded C Coding Standard

Use the project's adopted edition and checker configuration as the authority. This skill summarizes intent; it does not reproduce external standards.

## Baseline

- MISRA C: safety, determinism, type discipline, bounded control flow, and analyzability.
- CERT C: input validation, memory safety, integer safety, concurrency, and security.
- Barr Group Embedded C: naming, formatting, module organization, and firmware readability.
- Project rules and hardware/ABI constraints override the defaults; record deviations.

## Core rules

- Use fixed-width types, `size_t` for sizes, `bool` for logic, and named constants instead of magic numbers.
- Check ranges, lengths, pointers, return values, allocation results, and conversion overflow.
- Prefer static, bounded memory; define ownership, lifetime, capacity, and cleanup.
- Keep public interfaces explicit and private symbols `static`; use `const` for read-only data.
- Keep loops bounded and avoid recursion, hidden blocking, large stack objects, and unbounded logging.
- Use `volatile` only for hardware/async objects; use atomics or critical sections for synchronization.
- Keep ISRs short, bounded, non-blocking, and limited to capture/defer work; do not use blocking APIs, dynamic allocation, or complex logging in an ISR.
- Access registers with correct width, masks, ordering, reserved-bit handling, and documented side effects.
- Define timeout, fault, recovery, and safe-state behavior for every hardware or communication failure.
- Avoid undefined behavior, unsafe string operations, multiple-evaluation macros, implicit narrowing, and undocumented compiler extensions.

## Naming

Use the repository's existing convention. If none exists:

| Item | Form | Example |
|---|---|---|
| File | `lower_snake_case` | `can_driver.c` |
| Function | `module_verb_object` | `uart_rx_read` |
| Variable | descriptive `lower_snake_case` | `retry_count` |
| Boolean | predicate | `is_ready`, `has_error` |
| Constant/macro | `UPPER_SNAKE_CASE` | `UART_RX_BUFFER_SIZE` |
| Enum | module-prefixed members | `UART_STATE_IDLE` |
| Type | project suffix/prefix | `uart_state_t` |
| ISR/register | vendor or hardware name | `USART1_IRQHandler` |
| Unit | suffix | `timeout_ms`, `voltage_mv` |

## Review output

Report only actionable findings. Use:

```text
[P1] file.c:42 — rule/source
Evidence: ...
Impact: ...
Fix: ...
```

Prioritize undefined behavior, memory errors, race conditions, unsafe hardware behavior, unbounded timing, and unchecked failures. Finish with assumptions, deviations, and required validation.

For details and examples, read [references/rules.md](references/rules.md).
