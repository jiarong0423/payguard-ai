# TradeGlot hosted public demo image (optional; local use needs none of this).
# The container runs with PAYGUARD_DEMO_MODE=public: every provider adapter is a refusing
# stub (or, with PAYGUARD_HOSTED_READONLY_SANDBOX=enabled, a read-only Sandbox wrapper), no PayPal write or local-model call is possible, and the image holds no keys. (r32) The one exception is the
# evidence guide's Gemini chooser, used only when the operator sets PAYGUARD_HOSTED_GUIDE_MODEL=gemini and passes a
# free-tier GEMINI_API_KEY as a service secret at run time; without both, the guide stays on keywords.

# Stage 1: build the console frontend.
FROM node:22-slim@sha256:4b150b48b4116e2a22f2c39cc27025fbf4f153e2078fd3b14d159fdb5c7279da AS frontend
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY frontend/index.html frontend/evidence.html frontend/dashboard.html frontend/scenarios.html frontend/proof.html frontend/vite.config.js ./
COPY frontend/src ./src
COPY frontend/public ./public
# Optional AG Studio licence for /dashboard.html. Render passes service env vars as build args; empty means
# trial mode (watermark). The key is a client-side licence key and ends up in the built JavaScript by design.
ARG VITE_AG_STUDIO_LICENSE=
RUN VITE_AG_STUDIO_LICENSE="$VITE_AG_STUDIO_LICENSE" npm run build

# Stage 2: the guide's Gemini worker profile (Python 3.12, its own hash-pinned lock), built where it will run.
FROM python:3.12-slim@sha256:b18b261e1b4974b4f321451ad5251ded85abb22c2b8b262da527dda1d031ab30 AS gemini
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
COPY integrations/gemini/requirements.lock /app/integrations/gemini/requirements.lock
# No pip inside the venv: the worker's runtime check accepts exactly the locked distributions.
RUN python3.12 -m venv --without-pip /app/integrations/gemini/.venv \
 && python3.12 -m pip --python /app/integrations/gemini/.venv/bin/python3 install --require-hashes --only-binary=:all: \
    --no-deps -r /app/integrations/gemini/requirements.lock

# Stage 3: Python 3.13 runtime, dependencies installed only from the hash-pinned lock.
FROM python:3.13-slim@sha256:2d44738ebf4ce5f63b9d9ea871e9c7cfdc0426f7b0c97cac915fd88ded1d86bb AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src:/app/backend \
    PAYGUARD_DEMO_MODE=public \
    PORT=10000
WORKDIR /app
COPY requirements.lock ./
RUN pip install --require-hashes --only-binary=:all: --no-deps -r requirements.lock
COPY src ./src
COPY backend ./backend
COPY data ./data
COPY policies ./policies
COPY --from=frontend /build/frontend/dist ./frontend/dist
# The 3.12 interpreter the worker venv points at (versioned names, so nothing of the 3.13 runtime is replaced).
COPY --from=gemini /usr/local/bin/python3.12 /usr/local/bin/python3.12
COPY --from=gemini /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=gemini /usr/local/lib/libpython3.12.so.1.0 /usr/local/lib/libpython3.12.so.1.0
COPY --from=gemini /app/integrations/gemini/.venv ./integrations/gemini/.venv
COPY integrations/gemini/worker.py integrations/gemini/check_runtime.py integrations/gemini/pyproject.toml integrations/gemini/requirements.lock integrations/gemini/run.sh ./integrations/gemini/
RUN ldconfig
RUN useradd --system --uid 10001 --no-create-home payguard
USER payguard
EXPOSE 10000
# No --proxy-headers: the client address stays the proxy's, and the app admits it only for the
# exact PAYGUARD_PUBLIC_HOST with the forwarding headers the hosting proxy sets.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT}\" --no-access-log --no-proxy-headers --no-server-header"]
