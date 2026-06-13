#!/usr/bin/env bash
# Diagnostic & fix "Too many open files" - VPS Ubuntu / Coolify
# Usage: sudo bash fd-diagnostic.sh [--fix] [--fix-permanent]

set -euo pipefail

# ─── Couleurs ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

OK()    { echo -e "${GREEN}[OK]${RESET}    $*"; }
WARN()  { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
ERROR() { echo -e "${RED}[ERROR]${RESET} $*"; }
INFO()  { echo -e "${CYAN}[INFO]${RESET}  $*"; }
TITLE() { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════════${RESET}"; \
          echo -e "${BOLD}${CYAN}  $*${RESET}"; \
          echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}"; }

FIX=false
FIX_PERMANENT=false
for arg in "$@"; do
  [[ "$arg" == "--fix" ]] && FIX=true
  [[ "$arg" == "--fix-permanent" ]] && FIX_PERMANENT=true && FIX=true
done

require_sudo() {
  if [[ $EUID -ne 0 ]]; then
    ERROR "Ce script doit être lancé avec sudo : sudo bash $0 $*"
    exit 1
  fi
}
require_sudo "$@"

# ─── 1. DIAGNOSTIC FDs ───────────────────────────────────────────────────────
TITLE "1. DIAGNOSTIC — File Descriptors système"

# /proc/sys/fs/file-nr : utilisés / libres / max
FILE_NR=$(cat /proc/sys/fs/file-nr)
FD_USED=$(echo "$FILE_NR" | awk '{print $1}')
FD_FREE=$(echo "$FILE_NR" | awk '{print $2}')
FD_MAX=$(echo  "$FILE_NR" | awk '{print $3}')
FD_PCT=$(awk "BEGIN{printf \"%.1f\", ($FD_USED/$FD_MAX)*100}")

INFO "/proc/sys/fs/file-nr  →  utilisés: $FD_USED  /  libres: $FD_FREE  /  max: $FD_MAX"
if   (( FD_USED * 100 / FD_MAX >= 90 )); then ERROR "FDs globaux à ${FD_PCT}% (CRITIQUE)"
elif (( FD_USED * 100 / FD_MAX >= 70 )); then WARN  "FDs globaux à ${FD_PCT}% (élevé)"
else OK "FDs globaux à ${FD_PCT}%"
fi

# ulimit du shell courant
ULIMIT_SOFT=$(ulimit -Sn)
ULIMIT_HARD=$(ulimit -Hn)
INFO "ulimit shell courant  →  soft: $ULIMIT_SOFT  /  hard: $ULIMIT_HARD"
if   [[ "$ULIMIT_SOFT" == "unlimited" ]]; then OK  "ulimit soft = unlimited"
elif (( ULIMIT_SOFT < 65536 ));           then WARN "ulimit soft faible ($ULIMIT_SOFT < 65536 recommandé)"
else OK "ulimit soft = $ULIMIT_SOFT"
fi

# ─── 2. TOP 10 PROCESSUS par FDs ouverts ─────────────────────────────────────
TITLE "2. TOP 10 — Processus avec le plus de FDs ouverts"

INFO "Comptage via /proc/*/fd (peut prendre quelques secondes)..."
echo ""
printf "%-8s %-25s %-8s %s\n" "PID" "COMMANDE" "FDs" "UTILISATEUR"
printf "%-8s %-25s %-8s %s\n" "---" "--------" "---" "-----------"

declare -A TOP_PROCS
while IFS= read -r -d '' fddir; do
  pid=$(echo "$fddir" | grep -oP '(?<=/proc/)\d+')
  [[ -z "$pid" ]] && continue
  count=$(ls -1 "$fddir" 2>/dev/null | wc -l) || continue
  cmd=$(cat /proc/"$pid"/comm 2>/dev/null || echo "?")
  user=$(stat -c '%U' /proc/"$pid" 2>/dev/null || echo "?")
  TOP_PROCS["$pid"]="$count|$cmd|$user"
done < <(find /proc -maxdepth 2 -name fd -type d -print0 2>/dev/null)

# Tri et top 10
IFS=$'\n' sorted=($(
  for pid in "${!TOP_PROCS[@]}"; do
    echo "${TOP_PROCS[$pid]}|$pid"
  done | sort -t'|' -k1 -rn | head -10
))

for line in "${sorted[@]}"; do
  count=$(echo "$line" | cut -d'|' -f1)
  cmd=$(  echo "$line" | cut -d'|' -f2)
  user=$( echo "$line" | cut -d'|' -f3)
  pid=$(  echo "$line" | cut -d'|' -f4)
  marker=""
  (( count > 10000 )) && marker="${RED}  ← CRITIQUE${RESET}"
  (( count > 1000  )) && (( count <= 10000 )) && marker="${YELLOW}  ← élevé${RESET}"
  printf "%-8s %-25s %-8s %-12s" "$pid" "$cmd" "$count" "$user"
  echo -e "$marker"
done
echo ""

# ─── 3. SYSCTL EN LIVE ───────────────────────────────────────────────────────
TITLE "3. SYSCTL — Valeurs actuelles"

check_sysctl() {
  local key=$1 recommended=$2 label=$3
  local val
  val=$(sysctl -n "$key" 2>/dev/null || echo "N/A")
  printf "  %-45s = %-12s" "$key" "$val"
  if [[ "$val" == "N/A" ]]; then
    echo -e "  ${YELLOW}[WARN] clé non disponible${RESET}"
  elif (( val >= recommended )); then
    echo -e "  ${GREEN}[OK]${RESET}  (recommandé ≥ $recommended)"
  else
    echo -e "  ${YELLOW}[WARN]${RESET} $label (recommandé ≥ $recommended)"
    $FIX && { sysctl -w "${key}=${recommended}" > /dev/null; WARN "→ Appliqué en live: $key=$recommended"; }
  fi
}

check_sysctl "fs.file-max"                    2097152  "limite globale trop basse"
check_sysctl "fs.inotify.max_user_instances"  8192     "inotify instances insuffisantes"
check_sysctl "fs.inotify.max_user_watches"    1048576  "inotify watches insuffisants"
check_sysctl "net.core.somaxconn"             65535    "backlog connexions trop bas"
check_sysctl "vm.max_map_count"               262144   "requis par Elasticsearch/Supabase"

# ─── 4. LIMITES SYSTEMD / PAM ────────────────────────────────────────────────
TITLE "4. LIMITES — systemd & PAM"

SYSTEM_CONF="/etc/systemd/system.conf"
USER_CONF="/etc/systemd/user.conf"
LIMITS_CONF="/etc/security/limits.conf"
LIMITS_D="/etc/security/limits.d/99-fd.conf"

check_conf_value() {
  local file=$1 key=$2 recommended=$3
  local val
  val=$(grep -E "^[^#]*${key}" "$file" 2>/dev/null | tail -1 | grep -oP '\d+' | tail -1 || echo "0")
  printf "  %-45s = %-12s" "$file → $key" "$val"
  if [[ "$val" == "0" ]] || [[ -z "$val" ]]; then
    echo -e "  ${YELLOW}[WARN]${RESET} non défini (recommandé $recommended)"
  elif (( val >= recommended )); then
    echo -e "  ${GREEN}[OK]${RESET}"
  else
    echo -e "  ${YELLOW}[WARN]${RESET} faible (recommandé ≥ $recommended)"
  fi
}

check_conf_value "$SYSTEM_CONF" "DefaultLimitNOFILE" 1048576
check_conf_value "$USER_CONF"   "DefaultLimitNOFILE" 1048576

if [[ -f "$LIMITS_CONF" ]]; then
  NOFILE_ENTRIES=$(grep -E 'nofile' "$LIMITS_CONF" 2>/dev/null || true)
  if [[ -n "$NOFILE_ENTRIES" ]]; then
    OK "Entrées nofile dans limits.conf trouvées"
    echo "$NOFILE_ENTRIES" | sed 's/^/    /'
  else
    WARN "Aucune entrée nofile dans $LIMITS_CONF"
  fi
fi

if [[ -f "$LIMITS_D" ]]; then
  OK "Fichier $LIMITS_D existe"
else
  WARN "$LIMITS_D absent (recommandé)"
fi

# ─── 5. DOCKER — DÉTECTION FUITES FDs ────────────────────────────────────────
TITLE "5. DOCKER — Détection fuites FDs par container"

if ! command -v docker &>/dev/null; then
  WARN "Docker non trouvé dans PATH"
else
  CONTAINERS=$(docker ps --format '{{.Names}}|{{.ID}}|{{.Image}}' 2>/dev/null || echo "")
  if [[ -z "$CONTAINERS" ]]; then
    INFO "Aucun container Docker en cours d'exécution"
  else
    printf "\n%-30s %-14s %-8s %s\n" "NOM" "ID" "FDs" "IMAGE"
    printf "%-30s %-14s %-8s %s\n" "---" "--" "---" "-----"

    while IFS='|' read -r name cid image; do
      # PID du processus racine du container
      cpid=$(docker inspect --format '{{.State.Pid}}' "$cid" 2>/dev/null || echo "0")
      if [[ "$cpid" == "0" ]] || [[ -z "$cpid" ]]; then
        fd_count="N/A"
      else
        # Compter récursivement les FDs du namespace
        fd_count=$(find /proc/"$cpid"/fd -maxdepth 1 2>/dev/null | wc -l || echo "N/A")
      fi

      marker=""
      if [[ "$fd_count" != "N/A" ]]; then
        (( fd_count > 5000 )) && marker="${RED}  ← FUITE probable${RESET}"
        (( fd_count > 1000 )) && (( fd_count <= 5000 )) && marker="${YELLOW}  ← surveiller${RESET}"
      fi

      printf "%-30s %-14s %-8s %-35s" "$name" "${cid:0:12}" "$fd_count" "$image"
      echo -e "$marker"
    done <<< "$CONTAINERS"
  fi
fi

# ─── 6. N8N — BINARY DATA LEAK ───────────────────────────────────────────────
TITLE "6. N8N — Détection binary data / fichiers temporaires"

N8N_CONTAINERS=$(docker ps --format '{{.Names}}|{{.ID}}' 2>/dev/null | grep -i 'n8n\|n7n' || true)
if [[ -z "$N8N_CONTAINERS" ]]; then
  INFO "Aucun container n8n/n7n détecté"
else
  while IFS='|' read -r name cid; do
    INFO "Container n8n détecté: $name ($cid)"

    # Taille du répertoire /home/node/.n8n dans le container
    TMP_SIZE=$(docker exec "$cid" sh -c 'du -sh /home/node/.n8n/binaryData 2>/dev/null || echo "N/A"' 2>/dev/null || echo "N/A")
    TEMP_FILES=$(docker exec "$cid" sh -c 'find /tmp /home/node/.n8n/binaryData -type f 2>/dev/null | wc -l' 2>/dev/null || echo "N/A")

    if [[ "$TMP_SIZE" != "N/A" ]]; then
      SIZE_MB=$(echo "$TMP_SIZE" | grep -oP '[\d.]+(?=[MG])' || echo "0")
      echo "  binaryData size : $TMP_SIZE"
      echo "  Fichiers temp   : $TEMP_FILES"
      if [[ "$TMP_SIZE" == *"G"* ]] || (( ${SIZE_MB%.*} > 500 )); then
        ERROR "binary data volumineux dans $name — risque de fuite FDs/inodes"
        INFO  "Conseil: activer EXECUTIONS_DATA_PRUNE=true dans les env vars n8n"
      else
        OK "binary data OK ($TMP_SIZE)"
      fi
    fi

    # Logs d'erreur récents EMFILE
    EMFILE=$(docker logs --since 48h "$cid" 2>&1 | grep -i 'EMFILE\|too many open\|ENFILE' | tail -5 || true)
    if [[ -n "$EMFILE" ]]; then
      ERROR "Erreurs EMFILE récentes dans $name :"
      echo "$EMFILE" | sed 's/^/    /'
    else
      OK "Aucune erreur EMFILE dans les logs récents de $name"
    fi
  done <<< "$N8N_CONTAINERS"
fi

# FFmpeg / ffmpeg container
FFMPEG_CONTAINERS=$(docker ps --format '{{.Names}}|{{.ID}}' 2>/dev/null | grep -i 'ffmpeg' || true)
if [[ -n "$FFMPEG_CONTAINERS" ]]; then
  while IFS='|' read -r name cid; do
    INFO "Container FFmpeg détecté: $name"
    ZOMBIE=$(docker exec "$cid" sh -c 'ps aux | grep -c ffmpeg' 2>/dev/null || echo "0")
    (( ZOMBIE > 5 )) && WARN "Processus ffmpeg multiples dans $name ($ZOMBIE)" || OK "FFmpeg processus OK ($ZOMBIE)"
  done <<< "$FFMPEG_CONTAINERS"
fi

# ─── 7. CORRECTIONS PERMANENTES ──────────────────────────────────────────────
if $FIX_PERMANENT; then
  TITLE "7. APPLICATION — Corrections permanentes"

  # /etc/sysctl.conf
  SYSCTL_FILE="/etc/sysctl.conf"
  declare -A SYSCTL_WANTED=(
    ["fs.file-max"]="2097152"
    ["fs.inotify.max_user_instances"]="8192"
    ["fs.inotify.max_user_watches"]="1048576"
    ["net.core.somaxconn"]="65535"
    ["vm.max_map_count"]="262144"
  )
  for key in "${!SYSCTL_WANTED[@]}"; do
    val="${SYSCTL_WANTED[$key]}"
    if grep -qE "^[^#]*${key}" "$SYSCTL_FILE" 2>/dev/null; then
      sed -i "s|^[^#]*${key}.*|${key} = ${val}|" "$SYSCTL_FILE"
      OK "Mis à jour dans $SYSCTL_FILE: $key = $val"
    else
      echo "${key} = ${val}" >> "$SYSCTL_FILE"
      OK "Ajouté dans $SYSCTL_FILE: $key = $val"
    fi
    sysctl -w "${key}=${val}" > /dev/null
  done
  sysctl -p > /dev/null 2>&1 && OK "sysctl -p appliqué"

  # /etc/security/limits.d/99-fd.conf
  cat > "$LIMITS_D" << 'EOF'
# Augmente la limite de FDs pour tous les utilisateurs (n8n, docker, ffmpeg)
*    soft nofile 1048576
*    hard nofile 1048576
root soft nofile 1048576
root hard nofile 1048576
EOF
  OK "Écrit: $LIMITS_D"

  # /etc/systemd/system.conf
  for key in DefaultLimitNOFILE DefaultLimitNPROC; do
    val="1048576"
    if grep -qE "^[^#]*${key}" "$SYSTEM_CONF" 2>/dev/null; then
      sed -i "s|^[^#]*${key}.*|${key}=${val}|" "$SYSTEM_CONF"
    else
      # Ajoute sous [Manager] si présent, sinon en fin de fichier
      if grep -q '^\[Manager\]' "$SYSTEM_CONF" 2>/dev/null; then
        sed -i "/^\[Manager\]/a ${key}=${val}" "$SYSTEM_CONF"
      else
        echo "${key}=${val}" >> "$SYSTEM_CONF"
      fi
    fi
    OK "Mis à jour $SYSTEM_CONF: $key=$val"
  done

  # /etc/systemd/user.conf
  for key in DefaultLimitNOFILE DefaultLimitNPROC; do
    val="1048576"
    if grep -qE "^[^#]*${key}" "$USER_CONF" 2>/dev/null; then
      sed -i "s|^[^#]*${key}.*|${key}=${val}|" "$USER_CONF"
    else
      if grep -q '^\[Manager\]' "$USER_CONF" 2>/dev/null; then
        sed -i "/^\[Manager\]/a ${key}=${val}" "$USER_CONF"
      else
        echo "${key}=${val}" >> "$USER_CONF"
      fi
    fi
    OK "Mis à jour $USER_CONF: $key=$val"
  done

  # Override systemd pour les services Docker (applique aux containers)
  DOCKER_OVERRIDE_DIR="/etc/systemd/system/docker.service.d"
  DOCKER_OVERRIDE="${DOCKER_OVERRIDE_DIR}/limits.conf"
  mkdir -p "$DOCKER_OVERRIDE_DIR"
  cat > "$DOCKER_OVERRIDE" << 'EOF'
[Service]
LimitNOFILE=1048576
LimitNPROC=1048576
EOF
  OK "Écrit: $DOCKER_OVERRIDE"
  systemctl daemon-reload && OK "systemctl daemon-reload OK"

  # Conseil redémarrage
  echo ""
  WARN "Certains services doivent être redémarrés pour prendre les nouvelles limites :"
  echo "    sudo systemctl restart docker"
  echo "    # Puis redémarrer les containers n8n via Coolify ou :"
  echo "    # docker restart \$(docker ps -q)"
  echo ""
  WARN "Un reboot complet est la méthode la plus sûre pour appliquer toutes les limites."

else
  TITLE "7. CORRECTIONS PERMANENTES"
  INFO "Mode lecture seule. Pour appliquer les corrections :"
  echo "    sudo bash $0 --fix             # live sysctl seulement"
  echo "    sudo bash $0 --fix-permanent   # live + persistant (sysctl.conf, systemd, limits.d)"
fi

# ─── RÉSUMÉ FINAL ─────────────────────────────────────────────────────────────
TITLE "RÉSUMÉ"
echo -e "  Système       : $(uname -r)"
echo -e "  Date          : $(date)"
echo -e "  FDs utilisés  : ${FD_USED} / ${FD_MAX} (${FD_PCT}%)"
echo -e "  Kernel        : $(uname -r)"
echo ""
INFO "Logs Coolify  : docker logs coolify 2>&1 | grep -i 'EMFILE\\|too many'"
INFO "Logs n8n      : docker logs n8n 2>&1 | grep -i 'EMFILE\\|too many' | tail -20"
echo ""
