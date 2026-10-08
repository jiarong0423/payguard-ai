#!/bin/sh
set -eu

profile_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root=$(CDPATH= cd -- "$profile_root/../.." && pwd)
command_name=${1:-help}

if [ "$#" -gt 1 ]; then
  printf '%s\n' 'GEMINI_PROFILE_ARGUMENTS_REJECTED' >&2
  exit 64
fi

case "$command_name" in
  help)
    printf '%s\n' 'Usage: integrations/gemini/run.sh {check|test|generate|help}'
    exit 0
    ;;
  check|test|generate) ;;
  *)
    printf '%s\n' 'GEMINI_PROFILE_UNKNOWN_COMMAND' >&2
    exit 64
    ;;
esac

expected_python_path="$project_root/src:$project_root/backend"
if [ "${PYTHONPATH+x}" = x ]; then
  if [ "$PYTHONPATH" != "$expected_python_path" ]; then
    printf '%s\n' 'GEMINI_PROFILE_ENVIRONMENT_REJECTED' >&2
    exit 78
  fi
  unset PYTHONPATH
fi

for rejected_name in \
  ALL_PROXY CLOUDSDK_CORE_PROJECT CURL_CA_BUNDLE GCLOUD_PROJECT GEMINI_API_KEY \
  GOOGLE_API_KEY GOOGLE_APPLICATION_CREDENTIALS GOOGLE_CLOUD_PROJECT \
  GOOGLE_GENAI_USE_ENTERPRISE GOOGLE_GENAI_USE_VERTEXAI HTTP_PROXY HTTPS_PROXY \
  NO_PROXY OPENAI_API_KEY PAYGUARD_OPENAI_OUTBOUND PYTHONHOME REQUESTS_CA_BUNDLE \
  SSL_CERT_DIR SSL_CERT_FILE all_proxy curl_ca_bundle http_proxy https_proxy \
  no_proxy requests_ca_bundle ssl_cert_dir ssl_cert_file
do
  if printenv "$rejected_name" >/dev/null 2>&1; then
    printf '%s\n' 'GEMINI_PROFILE_ENVIRONMENT_REJECTED' >&2
    exit 78
  fi
done

python_bin=${PAYGUARD_GEMINI_PYTHON_BIN:-"$profile_root/.venv/bin/python3"}
if [ ! -x "$python_bin" ]; then
  printf '%s\n' 'GEMINI_PROFILE_RUNTIME_MISSING' >&2
  exit 78
fi

export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1
"$python_bin" -I -B "$profile_root/check_runtime.py"

case "$command_name" in
  check) exit 0 ;;
  test) exec "$python_bin" -I -B -m unittest discover -s "$profile_root" -p test_worker.py -v ;;
  generate)
    if [ "${PAYGUARD_GEMINI_OUTBOUND:-}" != enabled ]; then
      printf '%s\n' 'GEMINI_PROFILE_OUTBOUND_DISABLED' >&2
      exit 78
    fi
    exec "$python_bin" -I -B "$profile_root/worker.py" generate
    ;;
esac
