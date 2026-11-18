# Build context: packages/thea-db
#
# One-shot job for the `migrate` compose service: applies migrations/*.sql in
# order with psql. thea-db is a library the agent imports, not a long-running
# service, so this is the only image it needs.
FROM postgres:16-alpine
COPY migrations /migrations
CMD ["sh", "-c", "for f in /migrations/*.sql; do echo \"applying $f\"; psql \"$DATABASE_URL\" -v ON_ERROR_STOP=1 -f \"$f\" || exit 1; done"]
