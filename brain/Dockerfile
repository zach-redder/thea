# Build context: ./brain
#
# brain is not a long-running service (heart connects to Postgres directly
# via SQLAlchemy -- see brain/README.md). This image only exists to apply
# brain/migrations/*.sql against Postgres as docker-compose's one-shot
# `migrate` service; it's a thin psql wrapper, not a Python runtime.
FROM postgres:16-alpine
COPY migrations /migrations
CMD ["sh", "-c", "for f in /migrations/*.sql; do echo \"applying $f\"; psql \"$DATABASE_URL\" -v ON_ERROR_STOP=1 -f \"$f\" || exit 1; done"]
