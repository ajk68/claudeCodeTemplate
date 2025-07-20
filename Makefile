# Claude Code Template - Main Makefile
# This Makefile includes modular components from the make/ directory

# Include all modular makefiles
include make/help.mk
include make/setup.mk
include make/quality.mk
include make/clean.mk
include make/context.mk
include make/ai.mk
include make/project.mk
include make/database.mk
include make/logging.mk
include make/utils.mk

# Default target is defined in help.mk