# Scripts Directory

This directory contains utility scripts for the project.

## shoreman.sh

Process manager for running multiple services with unified logging.

- shoreman.sh is from [mitsuhiko/minibb](https://github.com/mitsuhiko/minibb) by Armin Ronacher (mitsuhiko)
- The idea of using Makefile for development tooling, shared logfiles and Vite plugin setup inspired by mitsuhiko's workflows

Usage:
```bash
./scripts/shoreman.sh              # Run with default Procfile
./scripts/shoreman.sh Procfile.dev # Run with custom Procfile
```