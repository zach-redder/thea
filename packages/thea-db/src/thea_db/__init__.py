"""THEA's data layer.

Imported directly by the agent service. There's no HTTP hop, because context
assembly runs several queries per voice turn and latency matters. No other
service imports this package.
"""
