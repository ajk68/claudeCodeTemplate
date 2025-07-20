/ship - Finalize and Deploy
You are shipping: $ARGUMENTS

Why This Command Exists
This is your final quality gate before code reaches users. Ship broken code and users suffer. But ship nothing and the business dies. Find the balance.

Your Mission
Get working code deployed safely. How you do that depends on what you're shipping.

Core Process (Adapt as Needed)
1. Understand What You're Shipping
Look at the changes. Are they:

Part of a planned feature? Check the implementation plan for this session (or check for docs/implementation_plan_*.md)
Ad-hoc fixes that grew?
Experimental work that actually worked?
A mix of all the above?
Context matters. A critical hotfix ships differently than a new feature.

2. Run Your Quality Checks
bash
# Review the diff
make review-diff

# Run tests
make test

# Check code quality
make lint

# Optional: Format if needed
make format
3. Make a Judgment Call
If issues found, consider:

How critical? Will it actually break something?
How complex to fix? 5 minutes or 5 hours?
What's the business impact of not shipping?
Your options aren't just "fix or abort":

Quick fix with /implement if obvious
Step back with /architect if it's gotten messy
Ship with known issues if they're acceptable
Revert parts and ship the rest
Ask Arthur: "Found X issue. It would take Y to fix. Ship anyway?"
If it's gotten too complex:

"This has grown beyond the original scope. I see:
- [What was intended]
- [What we actually have]
- [The gaps/issues]

Should we:
1. Step back and create a proper plan?
2. Ship what works, document the rest?
3. Spend time cleaning this up first?

What's the business priority here?"
4. Prepare the Commit
Ask before committing in these cases:

Changes grew beyond original scope
Multiple unrelated changes mixed together
Known issues that might need discussion
Experimental code that "works but..."
Otherwise, match the commit to what actually happened:

Planned feature: Reference the original intent
Hotfix: Explain what broke and why this fixes it
Exploration that worked: Be honest about what it does
5. Ship It
Once you and Arthur agree on the path forward:

bash
# Stage the changes
git add -A  # or selective staging if shipping partially

# Create the commit with a clear message
git commit -m "type: what changed from user perspective

- Why this change matters
- Any important implementation notes
- Known limitations if relevant"

# Show what we're about to push
git log --oneline -n 1
git push origin HEAD
Commit message based on context:

Planned feature → Reference the implementation plan
Bug fix → "fix: what was broken and impact"
Refactor → "refactor: what improved and why"
Mixed changes → Consider multiple commits
Final check: "Committed and pushed: [commit message]. Deployed successfully."

Guiding Principles
Be pragmatic: Perfect code that never ships helps nobody.

Be honest: If the code got messy, say so. If there are known issues, document them.

Be contextual: A payment processing fix needs different rigor than a color change.

Be communicative: When in doubt, explain the situation and options to Arthur.

Anti-Patterns to Avoid
❌ Shipping obviously broken code
❌ Endless polishing that delays value
❌ Hiding problems until they explode
❌ Following process when it doesn't fit

Remember
You're not a robot following a checklist. You're a thinking engineer making deployment decisions. The process is here to help, not constrain.

Sometimes the right call is to ship messy code and file a refactor ticket. Sometimes it's to stop and rethink. Use your judgment and keep Arthur in the loop.

The goal: Ship value to users without breaking things. How you get there is up to you.

