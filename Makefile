# Claude Code Template - Main Makefile
# This Makefile includes modular components from the make/ directory

# Include user-level first, then project-level (project overrides)
-include $(HOME)/ai_tools/make/help.mk
-include make/help.mk
-include $(HOME)/ai_tools/make/setup.mk
-include make/setup.mk
-include $(HOME)/ai_tools/make/quality.mk
-include make/quality.mk
-include $(HOME)/ai_tools/make/clean.mk
-include make/clean.mk
-include $(HOME)/ai_tools/make/context.mk
-include make/context.mk
-include $(HOME)/ai_tools/make/ai.mk
-include make/ai.mk
-include $(HOME)/ai_tools/make/project.mk
-include make/project.mk
-include $(HOME)/ai_tools/make/database.mk
-include make/database.mk
-include $(HOME)/ai_tools/make/logging.mk
-include make/logging.mk
-include $(HOME)/ai_tools/make/utils.mk
-include make/utils.mk

# Default target is defined in help.mk