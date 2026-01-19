# Container Standards 2026

**Version:** 1.0
**Last Updated:** 2026-01-19
**Status:** Active

## 1. Introduction
This guide establishes the technical standards for containerization in 2026, superseding legacy practices. It integrates modern Docker Compose V2 syntax, BuildKit optimizations, and security-first architectures.

## 2. Security Architecture

### 2.1 Non-Root by Default
Running as root is strictly prohibited for production workloads.
- **Requirement:** Define a dedicated user in the Dockerfile or Compose file.
- **Pattern:**
  ```dockerfile
  # Dockerfile
  RUN groupadd -r appuser && useradd -r -g appuser appuser
  USER appuser
  ```
  ```yaml
  # compose.yaml
  services:
    app:
      user: "1000:1000"
      read_only: true # Enforce immutable infrastructure
  ```

### 2.2 Secrets Management
Environment variables (`ENV`) are for configuration, not secrets.
- **Standard:** Use Docker Secrets or filesystem mounts.
- **Build-time:** Use BuildKit secret mounts (`--mount=type=secret`).
  ```dockerfile
  RUN --mount=type=secret,id=npmrc,dst=/root/.npmrc npm ci
  ```
- **Runtime:**
  ```yaml
  services:
    db:
      environment:
        POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      secrets:
        - db_password
  secrets:
    db_password:
      file: ./secrets/db_password.txt
  ```

### 2.3 Network Segmentation
Flat networks are disallowed. Isolate tiers.
- **Public:** Frontend/Gateway only.
- **Private:** Backend services (no internet egress/ingress unless strictly required).
- **Data:** Database layer (accessible only by Backend).

## 3. Image Optimization (BuildKit)

### 3.1 Multi-Stage Builds
Decouple build environment from runtime artifacts.
```dockerfile
# Syntax: docker/dockerfile:1
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
USER node
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

### 3.2 Cache Mounts
Leverage BuildKit cache mounts to speed up dependency installation.
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### 3.3 Base Images
- **Preference:** `alpine` (if compatible), `distroless` (for security), or `slim` variants.
- **Vulnerability Scanning:** Images must pass CVE scans (e.g., Trivy, Grype) before deployment.

## 4. Orchestration & Operations (Compose V2)

### 4.1 Modern Syntax
- Use `compose.yaml` (preferred) or `docker-compose.yml`.
- Command: `docker compose` (NOT `docker-compose`).

### 4.2 Robust Healthchecks
Services must define healthchecks to enable auto-healing and dependency management.
```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      db:
        condition: service_healthy
```

### 4.3 Resource Constraints
Prevent "Noisy Neighbor" issues by defining hard limits.
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.25'
      memory: 256M
```

## 5. Decision Matrix: Compose vs. Kubernetes

| Feature | Docker Compose | Kubernetes (K8s) |
| :--- | :--- | :--- |
| **Scope** | Single-node, Dev environments, Simple Deployments | Multi-node, High Availability, Complex Scaling |
| **Scaling** | Manual (`docker compose up --scale`) | Auto-scaling (HPA/VPA) |
| **Networking** | Simple Bridge/Overlay | Advanced CNI, Ingress Controllers, Service Mesh |
| **Config** | Simple YAML | Helm Charts, Kustomize, Operators |
| **Use Case** | Local Dev, CI Testing, Small VPS | Enterprise Production, Microservices at scale |

## 6. Anti-Patterns to Avoid
1.  **`:latest` Tag:** Always pin versions (e.g., `node:20.10-alpine`).
2.  **`privileged: true`:** Never use unless interacting with hardware/kernel modules.
3.  **Missing `.dockerignore`:** Always exclude `.git`, `node_modules`, `secrets`.
4.  **IP Binding:** Do not bind to `0.0.0.0` if `127.0.0.1` suffices for local dev.
