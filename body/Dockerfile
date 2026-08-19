# Build context: ./body (self-contained, not part of the Python workspace).
#
# Runs `next dev` rather than a production build+start, since a production
# build would fail today -- app/page.tsx, layout.tsx, and every component
# are empty stubs (see docs/ARCHITECTURE.md). Switch to a build+start
# multi-stage once real pages exist.
FROM node:22-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
