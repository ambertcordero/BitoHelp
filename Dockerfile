# -------------------------------------------------------
# CrypToCare Frontend — Quasar dev server
# Uses Node 22 + pnpm to run the Vite dev server on :9000
# Build & run:  docker compose up --build
# -------------------------------------------------------
FROM node:22-alpine AS builder

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

# Build stage for production
FROM builder AS production

# Allow VITE_API_URL to be passed as build argument
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

# Copy env file from deployment folder and export vars for build
COPY deployment/.env_prod /tmp/.env
RUN export $(cat /tmp/.env | grep -v '^#' | xargs) && pnpm build

# Production runtime - serve static files with Nginx
FROM nginx:alpine AS prod-runtime
COPY --from=production /app/dist/spa /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Development runtime
FROM builder AS dev-runtime
EXPOSE 9000

# Start the Quasar dev server (DOCKER=1 env makes it bind to 0.0.0.0)
CMD ["pnpm", "dev"]
