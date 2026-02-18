# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
#!/usr/bin/env bash
set -euo pipefail

EXIT_OK=0
EXIT_GENERIC=1
EXIT_VALIDATION=2
EXIT_NOTFOUND=3
EXIT_FORBIDDEN=4
EXIT_DEP_MISSING=5

CORR_ID="$(python3 -c 'import uuid; print(uuid.uuid4())')"
DRY_RUN="${BACKUP_DRY_RUN:-1}"
OUT_DIR="backups"
FILE_PREFIX="db_backup"

json_log() {
  local level="$1"; shift
  local msg="$1"; shift
  local kv="${1:-}"
  if [ -n "$kv" ]; then
    printf '{"ts":"%s","level":"%s","corr_id":"%s","message":"%s",%s}\n' "$(date -u +%FT%TZ)" "$level" "$CORR_ID" "$msg" "$kv"
  else
    printf '{"ts":"%s","level":"%s","corr_id":"%s","message":"%s"}\n' "$(date -u +%FT%TZ)" "$level" "$CORR_ID" "$msg"
  fi
}

usage() {
  cat <<USAGE
Usage: scripts/backup_database.sh [--dry-run] [--apply] [--out-dir DIR] [--file-prefix NAME]
Env:
  DB_URL or DB_HOST/DB_PORT/DB_USER/DB_NAME
  BACKUP_DRY_RUN=1 (default)
USAGE
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    json_log "ERROR" "dependency missing" "\"dependency\":\"$1\""
    exit $EXIT_DEP_MISSING
  }
}

upload_hook() {
  local dump_path="$1"
  json_log "INFO" "upload hook placeholder" "\"path\":\"$dump_path\""
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --apply) DRY_RUN=0 ;;
    --out-dir) shift; OUT_DIR="${1:-}" ;;
    --file-prefix) shift; FILE_PREFIX="${1:-}" ;;
    -h|--help) usage; exit $EXIT_OK ;;
    *) json_log "ERROR" "unknown argument" "\"arg\":\"$1\""; exit $EXIT_VALIDATION ;;
  esac
  shift
done

if [ -z "$OUT_DIR" ] || [ -z "$FILE_PREFIX" ]; then
  json_log "ERROR" "invalid options"
  exit $EXIT_VALIDATION
fi

mkdir -p "$OUT_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_FILE="$OUT_DIR/${FILE_PREFIX}_${TS}.sql.gz"

if [ -n "${DB_URL:-}" ]; then
  DUMP_CMD=(pg_dump "$DB_URL")
else
  DB_HOST="${DB_HOST:-}"
  DB_PORT="${DB_PORT:-5432}"
  DB_USER="${DB_USER:-}"
  DB_NAME="${DB_NAME:-}"
  if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_NAME" ]; then
    if [ "$DRY_RUN" = "1" ]; then
      DUMP_CMD=(pg_dump "<DB_URL_OR_HOST_PARAMS>")
    else
      json_log "ERROR" "missing DB connection values"
      exit $EXIT_VALIDATION
    fi
  else
    DUMP_CMD=(pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME")
  fi
fi

if [ "$DRY_RUN" = "1" ]; then
  json_log "INFO" "dry-run backup command" "\"out\":\"$OUT_FILE\",\"cmd\":\"pg_dump ... | gzip > $OUT_FILE\""
  exit $EXIT_OK
fi

require_cmd pg_dump
set +x
"${DUMP_CMD[@]}" | gzip -c > "$OUT_FILE" || {
  json_log "ERROR" "backup failed" "\"out\":\"$OUT_FILE\""
  exit $EXIT_GENERIC
}
json_log "INFO" "backup complete" "\"out\":\"$OUT_FILE\""
upload_hook "$OUT_FILE"
exit $EXIT_OK
