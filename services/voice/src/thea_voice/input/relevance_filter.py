"""Addressee detection: was that directed at THEA, or is it worth noticing? Respond, note, or discard.

Cascade, cheapest signal first: speaker ID, wake word, recent-conversation window, acoustic cues,
contextual cues (alone? on a call? TV on?), then a tiny semantic classifier. Emits `addressed` 0..1.
Design and thresholds: docs/ambient-and-home.md.

Not implemented yet.
"""
