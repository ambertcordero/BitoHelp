# -------------------------------------------------------
# CrypToCare — Dev Container image
# Provides Node 22 (with pnpm) AND Python 3.12 so a
# developer can work on both frontend and backend inside
# a single container.
# -------------------------------------------------------
FROM mcr.microsoft.com/devcontainers/javascript-node:22

# ---- Install Python 3.12 + pip ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# ---- Enable pnpm via corepack (ships with Node 22) ----
RUN corepack enable && corepack prepare pnpm@latest --activate

# Verify installations
RUN node --version && pnpm --version && python3 --version && pip3 --version
# =============================================================================
# CrypToCare — Dev Container Dockerfile
# =============================================================================
#
# This Dockerfile creates a full development environment for the CrypToCare
# project. When a developer opens this repo in VS Code with the Dev Containers
# extension (or GitHub Codespaces), this image is built automatically.
#
# Included tooling:
#   - Node.js 20 LTS (for Vue/Quasar frontend)
#   - pnpm (via corepack)
#   - Python 3.12 (for Django backend)
#   - pip + venv support
#   - Git, curl, and common dev utilities
#
# No manual setup is required — all dependencies are installed automatically
# via the postCreateCommand in devcontainer.json.
# =============================================================================

FROM mcr.microsoft.com/devcontainers/javascript-node:20

# ---- Install Python 3 + pip for the Django backend ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ---- Enable pnpm via corepack (ships with Node 20) ----
RUN corepack enable && corepack prepare pnpm@latest --activate

# ---- Create a symlink so "python" works (some systems only have "python3") ----
RUN if ! command -v python &> /dev/null; then ln -s $(which python3) /usr/local/bin/python; fi

# ---- Set a default working directory ----
WORKDIR /workspace

# Expose ports for frontend dev server and Django backend
EXPOSE 9000 8001
