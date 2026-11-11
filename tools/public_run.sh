#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
command_name=${1:-help}
if [ "$#" -gt 0 ]; then
  shift
fi

reject_arguments() {
  if [ "$#" -ne 0 ]; then
    printf '%s\n' 'PAYGUARD_PUBLIC_ARGUMENTS_REJECTED' >&2
    exit 64
  fi
}

require_python() {
  python_bin=${PAYGUARD_PYTHON_BIN:-"$project_root/.venv/bin/python3"}
  if [ ! -x "$python_bin" ]; then
    printf '%s\n' 'PAYGUARD_RUNTIME_MISSING: create .venv or set PAYGUARD_PYTHON_BIN explicitly' >&2
    exit 78
  fi
  if ! "$python_bin" -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 13) else 78)'; then
    printf '%s\n' 'PAYGUARD_PYTHON_313_REQUIRED' >&2
    exit 78
  fi
}

case "$command_name" in
  help)
    reject_arguments "$@"
    printf '%s\n' 'Usage: tools/run.sh {start|console|test|evaluate|demo|api|gemini-check|gemini-test|help}'
    exit 0
    ;;
  gemini-check|gemini-test)
    reject_arguments "$@"
    profile_command=check
    [ "$command_name" = gemini-test ] && profile_command=test
    exec /bin/sh "$project_root/integrations/gemini/run.sh" "$profile_command"
    ;;
  test|evaluate|api|console)
    reject_arguments "$@"
    ;;
  start)
    # One command from a fresh clone: create the Python 3.13 runtime and build the console only when missing.
    reject_arguments "$@"
    cd "$project_root"
    # .venv/.payguard-lock records the lock it was installed from: a failed or older install is redone.
    lock_digest=$(cksum < requirements.lock)
    if [ -z "${PAYGUARD_PYTHON_BIN:-}" ] && { [ ! -x "$project_root/.venv/bin/python3" ] || [ "$(cat .venv/.payguard-lock 2>/dev/null)" != "$lock_digest" ]; }; then
      if command -v uv >/dev/null 2>&1; then
        printf '%s\n' 'TradeGlot: installing .venv (Python 3.13) from requirements.lock'
        [ -x .venv/bin/python3 ] || uv venv --python 3.13 .venv
        uv pip install --python .venv/bin/python3 --require-hashes -r requirements.lock
        printf '%s\n' "$lock_digest" > .venv/.payguard-lock
      elif [ -x .venv/bin/python3 ]; then
        # A .venv made by hand (README steps) without uv on PATH: use it as it is; the console checks its imports.
        printf '%s\n' 'TradeGlot: uv not found; using the existing .venv as it is' >&2
      else
        printf '%s\n' 'PAYGUARD_UV_MISSING: install uv (https://docs.astral.sh/uv/) or create .venv yourself' >&2
        exit 78
      fi
    fi
    # Rebuild the console when it is missing or older than any frontend source (for example after a git pull).
    if [ ! -f "$project_root/frontend/dist/index.html" ] || [ -n "$(find frontend/src frontend/public frontend/index.html frontend/evidence.html frontend/dashboard.html frontend/scenarios.html frontend/proof.html frontend/package.json frontend/package-lock.json frontend/vite.config.js -newer frontend/dist/index.html 2>/dev/null | head -n 1)" ]; then
      if ! command -v npm >/dev/null 2>&1; then
        printf '%s\n' 'PAYGUARD_NPM_MISSING: install Node.js 20.19+ or 22.12+ with npm' >&2
        exit 78
      fi
      printf '%s\n' 'TradeGlot: building the console (frontend/dist)'
      (cd frontend && npm ci --ignore-scripts --no-audit --no-fund && npm run build)
    fi
    # One command for every use (owner 2026-11-03): ask once whether the guide may call Gemini, unless the caller
    # already chose. Gemini calls cost the owner's own credit, so the default is no; a non-interactive run never asks.
    if [ -z "${PAYGUARD_GUIDE_MODEL:-}" ] && [ -t 0 ]; then
      printf '%s' 'TradeGlot: use Gemini for the guide? It calls the paid API when you type in a guide. [y/N] '
      read -r use_gemini || use_gemini=''
      case "$use_gemini" in
        y|Y|yes|YES) export PAYGUARD_GUIDE_MODEL=gemini; printf '%s\n' 'TradeGlot: guide uses Rules + Gemini' ;;
        *) printf '%s\n' 'TradeGlot: guide uses rules only (no model calls)' ;;
      esac
    fi
    # A console already running on the port would make this start fail with a bind error; say so plainly.
    if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
      printf '%s\n' 'PAYGUARD_PORT_BUSY: something is already running on http://127.0.0.1:8000. Stop it (Ctrl+C in its terminal) and run this again.' >&2
      exit 75
    fi
    printf '%s\n' 'TradeGlot: open http://127.0.0.1:8000 (Ctrl+C to stop)'
    command_name=console
    ;;
  demo) ;;
  *)
    printf '%s\n' 'PAYGUARD_PUBLIC_UNKNOWN_COMMAND' >&2
    exit 64
    ;;
esac

require_python
cd "$project_root"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$project_root/src:$project_root/backend"

case "$command_name" in
  test) exec "$python_bin" -m unittest discover -s tests -v ;;
  evaluate) exec "$python_bin" -m payguard.advisory_eval ;;
  demo) exec "$python_bin" -m payguard.cli "$@" ;;
  console)
    # One process, one address: the API serves the built frontend on http://127.0.0.1:8000.
    if [ ! -f "$project_root/frontend/dist/index.html" ]; then
      printf '%s\n' 'PAYGUARD_CONSOLE_BUILD_MISSING: run "cd frontend && npm ci --ignore-scripts --no-audit --no-fund && npm run build" first' >&2
      exit 65
    fi
    "$python_bin" -c 'import fastapi, httpx, uvicorn'
    exec "$python_bin" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
    ;;
  api)
    "$python_bin" -c 'import fastapi, httpx, uvicorn'
    exec "$python_bin" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
    ;;
esac
