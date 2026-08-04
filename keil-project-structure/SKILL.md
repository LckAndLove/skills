---
name: keil-project-structure
description: Design and review a consistent Keil MDK project directory structure and file naming scheme. Use when creating or reorganizing Keil projects, deciding where application, BSP, driver, middleware, configuration, startup, linker, test, and generated files belong, or reviewing whether a source file is placed and named correctly.
---

# Keil Project Structure

Use a predictable layout so a developer can locate code by responsibility, replace a board or MCU with limited changes, and keep generated/vendor files separate from product code. Follow an existing project's established convention when it is documented and consistent.

## Project age decision

Classify the project before proposing changes:

- **New project:** use the recommended structure, naming rules, dependency direction, and generated-file separation from the start.
- **Existing project:** preserve the established physical layout and Keil groups. Do not move or rename files only for aesthetics. Make incremental changes, keep new code consistent with the existing project, and introduce a new boundary only when it reduces a real maintenance or safety risk.
- **Mixed project:** keep legacy modules stable and apply the recommended structure only to newly added modules. Document the boundary between legacy and new code.

For an existing project, first map the current directories and Keil groups, identify build/include dependencies, and estimate migration risk. Prefer wrappers, adapters, and new modules over large-scale file moves. A review should distinguish “recommended for new code” from “necessary to fix now.”

## STM32CubeMX-generated projects

Detect a CubeMX project by its `.ioc` file and generated directories such as `Core/`, `Drivers/`, `Middlewares/`, or a generated Keil project. Preserve the generator's layout because regeneration can overwrite generated files:

```text
project/
├── project.ioc                 # CubeMX source configuration
├── Core/
│   ├── Inc/                    # Generated application headers and user sections
│   └── Src/                    # Generated startup, HAL init, and interrupt files
├── Drivers/
│   ├── CMSIS/
│   └── STM32xxxx_HAL_Driver/
├── Middlewares/                # Generated or vendor middleware
├── Application/                # Project-owned application modules
├── Components/                 # Project-owned reusable services
├── BSP/                        # Board-specific code outside CubeMX-generated code
└── MDK-ARM/                    # Keil project, listings, and objects when generated here
```

- Keep CubeMX-generated files and names unchanged unless the generator configuration requires a change.
- Put custom logic in `Application/`, `Components/`, `BSP/`, or project-owned driver wrappers. Use `USER CODE BEGIN/END` sections only for small initialization hooks or code that must remain in a generated file.
- Do not put product modules inside `Drivers/STM32xxxx_HAL_Driver/`, CMSIS, or other vendor directories.
- Treat the `.ioc` file as the source of truth for clocks, pins, peripherals, middleware, and generated project settings. Document manual Keil changes that are not represented in the `.ioc` file.
- After regeneration, verify that custom code, include paths, source groups, linker settings, and startup behavior remain intact.

## Recommended layout

```text
project/
├── project.uvprojx              # Keil project file
├── project.uvoptx               # User options; usually not hand-edited
├── Application/                 # Product behavior and application entry
│   ├── Inc/
│   └── Src/
├── BSP/                         # Board-specific startup and hardware setup
│   ├── Inc/
│   ├── Src/
│   ├── Startup/                # startup_*.s and vector table
│   └── Linker/                 # scatter/linker files
├── Drivers/                     # MCU peripherals and external device drivers
│   ├── Inc/
│   └── Src/
├── Components/                  # Reusable middleware and protocol modules
│   ├── Inc/
│   └── Src/
├── RT-Thread/                   # Optional RT-Thread framework source
├── Config/                     # Build, pin, feature, and version configuration
├── ThirdParty/                 # Vendor libraries and external dependencies
├── Tests/                      # Unit, integration, and hardware tests
├── Docs/                       # Project-specific technical documentation
└── Output/                      # Optional build artifacts; normally excluded from Git
```

Use `MDK-ARM/` for the `.uvprojx`, listings, objects, and other Keil-specific files when the project follows that convention. Otherwise keep the `.uvprojx` at the repository root. Determine the actual location from the project file and keep physical directories, Keil groups, include paths, and source paths aligned.

## File placement

| Code responsibility | Directory | Examples |
|---|---|---|
| Product state machines, commands, task orchestration | `Application/` | `app_main.c`, `device_task.c` |
| Board clocks, pins, console, board init | `BSP/` | `board_init.c`, `board_clock.c` |
| Startup, vector table, linker/scatter files | `BSP/Startup/`, `BSP/Linker/` | `startup_stm32.s`, `stm32.sct` |
| MCU peripheral abstraction | `Drivers/` | `uart_driver.c`, `spi_driver.c` |
| External sensor/flash/display driver | `Drivers/` | `imu_driver.c`, `nor_flash.c` |
| Protocol, codec, reusable service | `Components/` | `modbus.c`, `crc16.c` |
| Feature, pin, clock, version configuration | `Config/` | `board_config.h`, `feature_config.h` |
| Vendor SDK or library source | `ThirdParty/` | `Vendor_HAL/`, `CMSIS/` |
| Tests and test fixtures | `Tests/` | `test_uart.c`, `test_protocol.c` |

Do not put product behavior in `BSP` or `Drivers`, direct register access in `Application`, vendor files in `Application`, or generated build output beside source files.

## Naming rules

- Use lowercase `snake_case` for project-owned directories and source files: `motor_control.c`, `board_clock.c`.
- Preserve established industry and vendor names such as `BSP`, `CMSIS`, `RT-Thread`, `Inc`, and `Src` when they are already used consistently.
- Keep implementation/header pairs aligned: `uart_driver.c` and `uart_driver.h`.
- Use a module prefix for public symbols and filenames: `uart_`, `motor_`, `board_`.
- Use suffixes consistently:
  - `_app`: application module
  - `_task`: thread/task entry or task module
  - `_bsp`: board support implementation
  - `_drv` or `_driver`: hardware driver
  - `_hal`: hardware abstraction wrapper
  - `_cfg`: configuration source/header
  - `_isr` or `_irq`: interrupt handling module
  - `_test`: test module
- Use `*_config.h` for compile-time configuration and `*_types.h` for shared type definitions.
- Use vendor names only for vendor-owned files. Do not rename third-party files merely to match project style; isolate them under `ThirdParty/`.
- Avoid generic names such as `common.c`, `utils.c`, or `misc.c` unless the module has a clearly bounded responsibility.

## RT-Thread projects

For RT-Thread projects, use the following additional mapping:

| RT-Thread content | Recommended location | Rule |
|---|---|---|
| RT-Thread kernel and official drivers | `RT-Thread/` | Treat as framework code; do not place product logic here. |
| Board port and RT-Thread board startup | `BSP/` | Own clocks, pins, startup, heap, console, and board initialization. |
| Project-specific RT-Thread device drivers | `Drivers/` | Adapt hardware to the RT-Thread device interface. |
| Reusable RT-Thread services and protocol adapters | `Components/` | Keep independent of a specific product where possible. |
| Threads, applications, shell commands, and product state machines | `Application/` | Use public RT-Thread and project interfaces; do not access registers directly. |
| Kconfig, pin, clock, feature, and board configuration | `Config/` | Keep build and hardware choices centralized. |

Keep RT-Thread source, vendor SDKs, and project-owned code distinguishable. Do not modify framework or vendor files for a product-only requirement; add an adapter or project module instead.

## Generated and third-party files

- Treat `MDK-ARM/Listings/`, `MDK-ARM/Objects/`, map files, `.axf`, `.hex`, `.bin`, and temporary logs as generated output. Keep them out of source directories and normally exclude them from Git.
- Keep CMSIS, MCU standard peripheral libraries, USB libraries, and other vendor packages under `ThirdParty/` or the repository's established `Libraries/` directory.
- Keep third-party source unchanged when possible. Put project-specific configuration and wrappers outside the third-party directory.

## Dependency direction

Keep dependencies moving downward:

```text
Application → Components → Drivers → BSP/HAL → MCU hardware
```

- `Application` may use public component and driver interfaces, but must not include MCU vendor headers directly.
- `Components` must not depend on a specific board or product feature.
- `Drivers` may use BSP/HAL services but must not call application functions.
- `BSP` owns board-specific startup, clocks, pins, memory layout, and low-level console setup.
- `ThirdParty` code should be wrapped by project-owned adapters instead of being included throughout the application.

## Review workflow

1. Identify the code's responsibility and hardware dependence.
2. Place it in the narrowest directory that owns that responsibility.
3. Choose a module-prefixed filename and matching header/source pair.
4. Check include and link dependencies against the downward dependency rule.
5. Keep Keil groups, include paths, source paths, and repository directories consistent.
6. Separate generated files and build artifacts from reviewed source code.

For reviews, report the file, current location, recommended location, naming issue, dependency violation, and migration impact. Do not move files solely for aesthetics when the current structure is documented and coherent.
