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
    printf '%s\n' 'Usage: tools/run.sh {test|evaluate|demo|api|local-ai-api|gemini-check|gemini-test|help}'
    exit 0
    ;;
  gemini-check|gemini-test)
    reject_arguments "$@"
    profile_command=check
    [ "$command_name" = gemini-test ] && profile_command=test
    exec /bin/sh "$project_root/integrations/gemini/run.sh" "$profile_command"
    ;;
  test|evaluate|api|local-ai-api)
    reject_arguments "$@"
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
  api)
    "$python_bin" -c 'import fastapi, httpx, uvicorn'
    exec "$python_bin" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
    ;;
  local-ai-api)
    "$python_bin" -c 'import fastapi, httpx, uvicorn'
    exec "$python_bin" -m uvicorn app.main:create_lmstudio_app --factory --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
    ;;
esac
