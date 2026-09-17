#!/usr/bin/env python3
"""
ArtiFix — Script di rollback automatico.

Confronta i file critici con i backup in docs/backups/2026-09-17/.
Se un file è diverso dal backup E non ha commit recenti (< 1 ora),
lo ripristina dal backup.

Uso:
    python rollback.py [--dry-run] [--branch BRANCH]

Opzioni:
    --dry-run    Mostra cosa farebbe senza modificare nulla
    --branch     Branch da controllare (default: main)
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- CONFIGURAZIONE ---
BACKUP_DIR = Path("docs/backups/2026-09-17")
LOG_FILE = Path("docs/roadmap/Log_Errors.md")

# Mappa: file originale -> nome backup
CRITICAL_FILES = {
    "app.py": "app_v7.4.py",
    "translations.py": "translations_v7.4.py",
    "share_utils.py": "share_utils_v7.4.py",
    "requirements.txt": "requirements_v7.4.txt",
}

# Se un file ha un commit negli ultimi N minuti, NON fare rollback
RECENT_COMMIT_MINUTES = 60


def file_hash(path: Path) -> str | None:
    """Calcola SHA256 di un file. None se non esiste."""
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_recent_commit(filename: str, minutes: int = RECENT_COMMIT_MINUTES) -> bool:
    """Verifica se il file ha un commit negli ultimi `minutes` minuti."""
    try:
        since = (datetime.now() - timedelta(minutes=minutes)).isoformat()
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--oneline", "--", filename],
            capture_output=True,
            text=True,
            check=False,
        )
        return bool(result.stdout.strip())
    except Exception:
        # Se git non è disponibile, meglio essere conservativi
        return False


def log_error(filename: str, message: str) -> None:
    """Appende una riga al log errori."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"- **[{timestamp}]** `{filename}` — {message}\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def ensure_log_header() -> None:
    """Crea l'intestazione del log se non esiste."""
    if not LOG_FILE.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(
            "# ArtiFix — Log Errori\n\n"
            "Registro automatico dei rollback eseguiti dal sistema.\n\n"
            "---\n\n",
            encoding="utf-8",
        )


def rollback_file(filename: str, dry_run: bool = False) -> str:
    """
    Ritorna uno stato:
      - "OK"          -> nessuna differenza
      - "RECENT"      -> differenza ma commit recente (modifica intenzionale)
      - "ROLLBACK"    -> ripristinato dal backup
      - "MISSING"     -> file o backup mancante
    """
    backup_name = CRITICAL_FILES[filename]
    backup_path = BACKUP_DIR / backup_name
    current_path = Path(filename)

    if not current_path.exists():
        return "MISSING_CURRENT"
    if not backup_path.exists():
        return "MISSING_BACKUP"

    h_current = file_hash(current_path)
    h_backup = file_hash(backup_path)

    if h_current == h_backup:
        return "OK"

    # Differenza rilevata
    if has_recent_commit(filename):
        return "RECENT"

    # Rollback (o dry-run)
    if not dry_run:
        shutil.copy(backup_path, current_path)
    return "ROLLBACK"


def main() -> int:
    parser = argparse.ArgumentParser(description="ArtiFix rollback automatico")
    parser.add_argument("--dry-run", action="store_true", help="Non modificare nulla")
    parser.add_argument("--branch", default="main", help="Branch (info)")
    args = parser.parse_args()

    ensure_log_header()

    print(f"🔍 ArtiFix Rollback — branch: {args.branch} — dry-run: {args.dry_run}")
    print("=" * 60)

    rollbacks = 0
    for filename in CRITICAL_FILES:
        status = rollback_file(filename, dry_run=args.dry_run)

        if status == "OK":
            print(f"✅ {filename}: OK")
        elif status == "RECENT":
            print(f"🕐 {filename}: modifica recente, salto (intenzionale)")
        elif status == "ROLLBACK":
            print(f"🔧 {filename}: ROLLBACK eseguito")
            if not args.dry_run:
                log_error(filename, f"Rollback da `{CRITICAL_FILES[filename]}`")
            rollbacks += 1
        elif status.startswith("MISSING"):
            print(f"❌ {filename}: {status}")
            if not args.dry_run:
                log_error(filename, status)
        else:
            print(f"⚠️  {filename}: stato sconosciuto ({status})")

    print("=" * 60)
    print(f"Rollback eseguiti: {rollbacks}")

    # Exit code: 0 se nessun rollback, 1 se almeno un rollback (utile per Actions)
    return 1 if rollbacks > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
