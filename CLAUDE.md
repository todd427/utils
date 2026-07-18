# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A collection of small standalone Python utilities. Currently just `currEnv.py`, which prints a summary of the current machine's hardware/software capabilities (OS, Python version, CPU, RAM, GPU/CUDA).

## Commands

```bash
python currEnv.py          # print basic environment summary
python currEnv.py --all    # include motherboard + drive details (Linux; dmidecode needs sudo)
pip install -r requirements.txt   # install dependencies (torch pulls the full CUDA stack)
```

There is no build, lint, or test setup.

## Notes

- `requirements.txt` pins a CUDA-enabled `torch` build plus its `nvidia-*-cu12` dependency chain — installs are large. The only direct third-party imports are `psutil` and `torch`.
- `currEnv.py` branches on `platform.system()` ("Linux"/"Windows") and shells out to platform-specific tools (`lscpu`, `wmic`, `dmidecode`, `lsblk`) via the `run_cmd` helper, which swallows failures and returns `None`. Any new probe should degrade gracefully the same way rather than raising.
- New utilities are added as independent top-level scripts; keep each self-contained with a `main()` and `if __name__ == "__main__"` guard, matching `currEnv.py`.
