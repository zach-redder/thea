"""Redis-backed short-term session state (active conversation, turn buffer, presence).

Separate from thea.memories: this holds minutes-to-hours of context and is
safe to lose. Long-term recall goes through repositories/memory_repo.py.

Not implemented yet. Planned interface: get(session_id), append_turn(session_id, turn),
set_presence(room), with a TTL on every key.
"""
