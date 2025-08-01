# PentestAider Usage Guide

## Overview

PentestAider is an extensible penetration testing assistant that streamlines recon, scanning, exploitation, social engineering simulation, and reporting.

## Ethics Disclaimer

**Warning:** PentestAider is for use ONLY on systems and targets you are explicitly authorized to test. Unauthorized use may be illegal and unethical. Always ensure you have written permission before scanning or testing any system.

## Command-Line Flags

- `--pentest` : Enable PentestAider security tooling.
- `--scope-file` : Specify in-scope domains/IPs.
- `--unsafe-exec` : Actually execute external security tools (see below).
- `--help` : List all commands and options.

## Safe Execution & Sandboxing

By default, PentestAider runs all tool integrations in safe "stub" mode (no real external commands are executed). To enable real execution, you **must**:

1. Pass `--unsafe-exec` on the CLI, and
2. Set the environment variable:  
   `export PENTESTAIDER_UNSAFE=1`

Without both, all scan/exploit actions remain simulated.

## Example Commands

- `/recon <target>` : Run reconnaissance tools (nmap, sublist3r, etc.)
- `/scan <target>` : Perform vulnerability scanning (nikto, sqlmap, nuclei, etc.)
- `/exploit reverse <bash|python|nc> <lhost> <lport>` : Generate reverse shell payloads
- `/exploit msf <payload_type> <lhost> <lport>` : Generate msfvenom payloads
- `/osint <target>` : Run OSINT collection (whois, DNS, shodan)
- `/social email <template> <target_name> <org>` : Generate phishing email
- `/dashboard` : Show summary of latest recon/scan/exploit/social results
- `/reportgen` : Aggregate all evidence/results and save a markdown report

## Evidence Management

All reports and evidence are saved under `.aider/evidence/` with timestamps for traceability.

## See Also

- [tasks/pentest_tasklist.md](../tasks/pentest_tasklist.md) for the full roadmap.