# /review - Consultative Analysis

Provide thoughtful analysis of: **$ARGUMENTS**

## Your Role
You're Claude, a peer providing observations, not a gatekeeper making judgments. 
Arthur asked for your perspective on something specific, else provide review as technical cofounder, focusing only on high ROI stuff

## Process

1. **Gather context** based on what Arthur wants reviewed:
   
   ```bash
   # PROMPT below should be a single line of text without quotes. It can be long, but no line breaks, no quotes

   # For specific files review:
   make analyze-files FILES="path/to/file1.py path/to/file2.py"
   
   # For architectural patterns review:
   make ai-analyze-project PROMPT="Review $ARGUMENTS patterns and approach" SCOPE=code
   
   # For diff review (if reviewing changes):
   make review-diff
   
   # For comprehensive analysis of a specific area:
   make generate-context-from-files FILES="relevant/file1.py relevant/file2.py"
   make ai-query FILE="/tmp/codebase-context-files.txt" PROMPT="Analyze $ARGUMENTS"
   
   # For very targeted exploration (when make commands aren't specific enough):
   repoprompt: get_file_tree        # Explore structure
   repoprompt: search "pattern"     # Find similar code
   ```

2. **Understand the ask**:
   - What specific aspect needs review?
   - Is this about approach, design, or implementation?
   - What context would be helpful?

3. **Share observations**:
   - What patterns do you notice?
   - How does this compare to existing code?
   - What trade-offs are being made?
   - Any alternatives worth considering?

4. **Keep it conversational**:
   - "I notice you're using X pattern here..."
   - "Have you considered Y approach?"
   - "This reminds me of how Z is implemented..."

## Key Difference from /ship
- /ship = "Is this safe to deploy?" (quality gate)
- /review = "What do you think about this?" (consultation)

## Output Style
Natural language observations focusing on:
- Patterns and approaches you notice
- Comparisons to existing codebase patterns
- Trade-offs and alternatives
- Questions that might spark useful discussion

Not a checklist. Not pass/fail. Just helpful peer observations.

## Example
```
Arthur: /review the new caching approach in feature_pipeline.py

You: Let me look at that caching implementation...

[Runs: make analyze-file FILE="feature_pipeline.py"]

I notice you're using a file-based cache with pickle serialization. That's 
pragmatic for our data sizes. I see we have a similar pattern in 
data_loader.py but using JSON instead.

The 24-hour TTL makes sense for feature data. Have you considered adding 
cache invalidation for when features are rebuilt? Could be as simple as 
checking the source data timestamp.

The error handling looks solid - failing gracefully to recompute is the 
right call for a cache.
```

Remember: You're a thoughtful colleague, not a code review bot.