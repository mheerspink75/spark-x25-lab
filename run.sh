#!/usr/bin/env bash

set -euo pipefail

OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
OLLAMA_CONTEXT_LENGTH="${OLLAMA_CONTEXT_LENGTH:-65536}"

OLLAMA_MODEL="${OLLAMA_MODEL:-SparkLLM/Spark-X2.5-4B:latest}"
OPENCODE_MODEL="${OPENCODE_MODEL:-ollama/${OLLAMA_MODEL}}"

OLLAMA_LOG="${OLLAMA_LOG:-./ollama.log}"

echo "== Local OpenCode launcher =="
echo "Ollama host:    ${OLLAMA_HOST}"
echo "Ollama model:   ${OLLAMA_MODEL}"
echo "OpenCode model: ${OPENCODE_MODEL}"
echo "Context:        ${OLLAMA_CONTEXT_LENGTH} tokens"

for command in ollama opencode curl; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        echo "Error: '${command}' is not installed or not in PATH." >&2
        exit 1
    fi
done

server_started=false
ollama_pid=""

cleanup() {
    if [[ "${server_started}" == "true" ]] &&
       [[ -n "${ollama_pid}" ]] &&
       kill -0 "${ollama_pid}" >/dev/null 2>&1; then

        echo
        echo "== Stopping Ollama server =="
        kill "${ollama_pid}"
    fi
}

trap cleanup EXIT INT TERM

# Start Ollama before running any commands that connect to it.
if curl -fsS "http://${OLLAMA_HOST}/api/tags" >/dev/null 2>&1; then
    echo "== Using existing Ollama server =="
    echo "Warning: the existing server controls its own context setting."
else
    echo "== Starting Ollama server =="

    OLLAMA_HOST="${OLLAMA_HOST}" \
    OLLAMA_CONTEXT_LENGTH="${OLLAMA_CONTEXT_LENGTH}" \
        ollama serve >"${OLLAMA_LOG}" 2>&1 &

    ollama_pid=$!
    server_started=true

    echo "Waiting for Ollama..."

    ready=false

    for _ in $(seq 1 30); do
        if curl -fsS "http://${OLLAMA_HOST}/api/tags" >/dev/null 2>&1; then
            ready=true
            break
        fi

        if ! kill -0 "${ollama_pid}" >/dev/null 2>&1; then
            echo "Error: Ollama exited unexpectedly." >&2
            echo "Review ${OLLAMA_LOG}:" >&2
            tail -n 30 "${OLLAMA_LOG}" >&2
            exit 1
        fi

        sleep 1
    done

    if [[ "${ready}" != "true" ]]; then
        echo "Error: Ollama did not become ready." >&2
        echo "Review ${OLLAMA_LOG}:" >&2
        tail -n 30 "${OLLAMA_LOG}" >&2
        exit 1
    fi

    echo "== Ollama server is ready =="
fi

# Ensure the model exists.
if ! ollama list |
    awk 'NR > 1 {print $1}' |
    grep -Fxq "${OLLAMA_MODEL}"; then

    echo "== Pulling missing model =="
    ollama pull "${OLLAMA_MODEL}"
else
    echo "== Model is installed =="
fi

echo "== Testing model =="

response="$(
    curl -fsS "http://${OLLAMA_HOST}/api/generate" \
        -H "Content-Type: application/json" \
        -d "$(printf \
            '{"model":"%s","prompt":"Reply with OK.","stream":false,"options":{"num_ctx":%s}}' \
            "${OLLAMA_MODEL}" \
            "${OLLAMA_CONTEXT_LENGTH}")"
)"

if ! grep -q '"response"' <<<"${response}"; then
    echo "Error: the model test did not return a response." >&2
    echo "${response}" >&2
    exit 1
fi

echo "== Model test succeeded =="
echo "== Starting OpenCode =="

exec opencode --model "${OPENCODE_MODEL}" "$@"