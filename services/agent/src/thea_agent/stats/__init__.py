"""Life stats: collectors write raw samples, aggregators compute what the dashboard and THEA both read.

The agent's `get_stats` tool and /api/v1/stats/* share the same aggregator functions, so what she
says can never disagree with what the dashboard shows. See docs/stats-and-dashboard.md.
"""
