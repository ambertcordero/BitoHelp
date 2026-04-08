FROM node:22-alpine

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY . .
RUN pnpm install --no-frozen-lockfile

EXPOSE 9000

CMD ["pnpm", "dev"]
