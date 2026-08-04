# Embedded C Quick Reference

Use the adopted project versions of MISRA C, CERT C, and Barr Group Embedded C for exact wording and compliance decisions.

## High-risk checks

- Undefined behavior: invalid shifts, signed overflow, uninitialized reads, lifetime violations, bad format strings, and evaluation-order assumptions.
- Memory: bounds, capacity, integer multiplication overflow, ownership, DMA alignment/cache state, and cleanup after partial initialization.
- Concurrency: ISR/task/shared-data races, atomicity of multi-byte values, lock ordering, callback lifetime, and `volatile` misuse.
- Hardware: register width, masks, reserved bits, read/write side effects, reset state, sequencing, timeout, and safe recovery.
- Real time: bounded loops, no recursion, no unexpected blocking, bounded stack/logging, and wrap-safe tick arithmetic.

## Minimal code preferences

```c
static bool adc_read_mv(uint16_t raw, uint16_t *out_mv)
{
    if ((out_mv == NULL) || (raw > ADC_MAX_COUNTS)) {
        return false;
    }

    *out_mv = (uint16_t)(((uint32_t)raw * ADC_REF_MV) / ADC_MAX_COUNTS);
    return true;
}
```

- Prefer `static const`, enums, and inline functions over magic numbers and unsafe macros.
- Use explicit lengths for binary data; avoid unbounded `strcpy`, `strcat`, and `sprintf`.
- Document non-obvious units, invariants, hardware constraints, and approved deviations.

## Deviation record

```text
Rule/source: ...
Location: ...
Reason: ...
Risk control: ...
Verification: ...
Owner/review date: ...
```
