# -------------------------------------------------------
# CrypToCare Frontend — Quasar dev server
# Uses Node 22 + pnpm to run the Vite dev server on :9000
# Build & run:  docker compose up --build
# -------------------------------------------------------
FROM node:22-alpine

WORKDIR /app

# Enable corepack and activate pnpm (ships with Node 22)
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy dependency manifests first for better Docker layer caching
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# quasar prepare (postinstall) needs these config files to exist
COPY quasar.config.js postcss.config.js jsconfig.json index.html ./

# Install dependencies (--no-frozen-lockfile because lock may drift)
RUN pnpm install --no-frozen-lockfile

# Copy the rest of the source code
COPY . .

EXPOSE 9000

# Start the Quasar dev server (DOCKER=1 env makes it bind to 0.0.0.0)
CMD ["pnpm", "dev"]
