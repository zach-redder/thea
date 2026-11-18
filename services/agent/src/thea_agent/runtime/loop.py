"""The agent turn loop: build context -> call the model -> run tool calls -> repeat until a final answer.

Invariants: the system prompt stays byte-stable for a whole conversation (prompt caching), and
user/assistant roles strictly alternate.

Not implemented yet. See docs/architecture.md.
"""
