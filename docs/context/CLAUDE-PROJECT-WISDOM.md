# Project Wisdom
Last Distilled: 2025-07-27 by context-keeper
Next Distillation: 2025-08-03

## 🎯 Architecture Truths
- **Agent System**: Separate agents for focused tasks prevent context pollution
- **Context Tiers**: Three-tier system (Active/Wisdom/Patterns) prevents both rot and loss
- **Delegation**: Lateral communication between agents reduces orchestration overhead

## ⚠️ Common Gotchas
- **Context Limits**: Main Claude context is finite - delegate early and often
- **Scope Creep**: Every "while I'm here" addition compounds - enforce anti-bloat discipline
- **Pattern Deviation**: New patterns need 3+ uses before abstraction

## ✅ Patterns That Work
### Agent Communication
```yaml
# Always structure delegations like this
- <delegation>
    Trigger: [specific condition]
    Target: [agent-name]
    Handoff: "[exact message format]"
  </delegation>
```

### Context Management
- Active context stays under 2000 words
- Weekly distillation prevents knowledge loss
- Explicit "NOT doing" prevents scope expansion

### Task Tracking
- Every task gets an ID (T001, T002...)
- Track estimate vs actual for drift detection
- Update status immediately, not in batches

## 📜 Code Archaeology
- **Why Sub-agents**: Previous template relied on commands that couldn't delegate, leading to context exhaustion
- **Drift Metrics**: Added after tasks regularly exceeded 3x estimates
- **Three Tiers**: Two-tier system lost important patterns during pruning