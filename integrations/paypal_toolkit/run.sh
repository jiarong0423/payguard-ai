#!/bin/sh
set -eu
export OPENAI_AGENTS_DISABLE_TRACING=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
unset PYTHONPATH PYTHONHOME
profile_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command_name=${1:-help}
if [ "$#" -gt 1 ]; then printf '%s\n' 'PROFILE_ARGUMENTS_REJECTED' >&2; exit 64; fi
case "$command_name" in
  help) printf '%s\n' 'Usage: integrations/paypal_toolkit/run.sh {check|test|help}'; exit 0 ;;
  check|test) ;;
  *) printf '%s\n' 'PROFILE_UNKNOWN_COMMAND' >&2; exit 64 ;;
esac
python_bin=${PAYGUARD_PAYPAL_TOOLKIT_PYTHON_BIN:-"$profile_root/.venv/bin/python3"}
if [ ! -x "$python_bin" ]; then printf '%s\n' 'PROFILE_RUNTIME_MISSING' >&2; exit 78; fi
"$python_bin" -I -B "$profile_root/check_runtime.py"
if [ "$command_name" = check ]; then exit 0; fi
if [ "$command_name" = test ]; then
  exec "$python_bin" -I -B -m unittest discover -s "$profile_root" -p test_runtime.py -v
fi
