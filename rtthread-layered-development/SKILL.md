---
name: rtthread-layered-development
description: Guide the design, implementation, and review of RT-Thread code using its common layered architecture. Use for RT-Thread applications, components, middleware, device drivers, BSPs, initialization code, threads, IPC, and hardware adaptation. Define each layer's responsibilities, dependency boundaries, code placement, and forbidden content.
---

# RT-Thread Layered Development

Organize code so upper layers use lower layers, while lower layers do not depend on upper layers. Follow the project's actual directory structure and RT-Thread version when local rules are more specific.

## Common layers

| Layer | Responsibilities | May depend on | Must not contain |
|---|---|---|---|
| Application | Product behavior, state machines, task orchestration, business protocols | RT-Thread APIs, public component APIs, device abstractions | Register access, clock setup, board-specific GPIO details |
| Components/Middleware | Reusable protocols, filesystems, networking, logging, service modules | Kernel, device framework, abstract interfaces | Product workflows, board pins, board startup |
| Device drivers | `rt_device`, I/O operations, control, IRQ, DMA, device state | RT-Thread kernel, device framework, MCU HAL | Product behavior, UI logic, cross-device decisions |
| BSP/Board | Startup, clocks, pins, linker configuration, board initialization, console | MCU HAL, startup code, kernel port interfaces | Product behavior and complex protocol processing |
| Kernel | Scheduling, threads, IPC, timers, memory management | CPU port and build configuration | Product logic and device-specific behavior |

Vendor HAL code normally belongs inside the BSP or driver implementation. Do not let application code call the HAL directly; isolate hardware differences behind drivers or device interfaces.

## Dependency rules

- Keep the dependency direction: application → components/middleware → device framework/drivers → BSP/HAL → hardware.
- Prevent reverse dependencies, such as drivers including application headers, BSP code calling business functions, or components accessing board-specific GPIOs directly.
- Use interfaces, callbacks, events, or messages for cross-layer communication. Avoid hidden global state and implicit side effects.
- Put public contracts in module headers and keep implementation symbols `static`. Do not expose lower-level details to upper layers.
- Modify the kernel only for a genuine RT-Thread mechanism issue. Do not change the kernel to solve one product-specific requirement.

## Initialization and threads

- Let the BSP initialize hardware, drivers register devices, components initialize services, and the application initialize product behavior. Do not start product behavior from BSP initialization.
- Use the project's initialization export macros and stages. Keep initialization order traceable and do not use a device before it is initialized.
- Keep each thread responsible for one layer's role. Define priority, stack size, blocking points, period, shutdown behavior, and recovery behavior.
- Do not block, allocate dynamically, perform complex logging, or execute business logic in an ISR. Capture state and notify a thread instead.
- Define ownership, lifetime, timeout, and destruction rules for IPC objects. Avoid unbounded waits.

## Where should code go?

Ask what the code depends on, who it serves, and whether it can be reused outside the current product:

- Product requirements and business state → application layer.
- Reusable across products or devices → components/middleware layer.
- Hardware capability exposed through a common interface → driver layer.
- Power-on board or chip configuration → BSP layer.
- Scheduling, IPC, or memory mechanism changes → kernel layer, with separate impact assessment.

## Review checklist

1. Does the file belong to the layer matching its responsibility?
2. Are there reverse dependencies, direct cross-layer accesses, or hidden global state?
3. Does application code bypass device interfaces and access registers or HAL APIs?
4. Does a driver contain product behavior or board-specific decisions?
5. Are initialization order, thread boundaries, blocking, and timeouts explicit?
6. Are interrupt, DMA, cache, and shared-data synchronization rules correct?
7. Which code remains unchanged when the MCU or board is replaced?

Report the file/line, owning layer, violated boundary, impact, and recommended destination. Do not split code into empty wrapper modules merely to satisfy a layer diagram.
