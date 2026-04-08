"""
Jaybird Automations — Lead Database Manager
Unified SQLite database for all prospected leads.

USAGE:
  python lead_database.py init                          # Create the database
  python lead_database.py import leads.xlsx             # Import from Excel
  python lead_database.py list --status new             # List leads by status
  python lead_database.py list --score 7                # List leads with score >= 7
  python lead_database.py update 42 --status contacted  # Update lead status
  python lead_database.py stats                         # Show pipeline stats
  python lead_database.py export                        # Export to Excel
  python lead_database.py search "law firm"             # Search by name or industry
"""

import os
import sys
import sqlite3
import argparse
from datetime import datetime

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "jaybird_leads.db")

VALID_STATUSES = ["new", "contacted", "replied", "meeting", "client", "not_interested", "do_not_contact"]


def get_db():
    """Get database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the leads database tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            industry TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            website TEXT,
            google_rating REAL,
            review_count INTEGER DEFAULT 0,
            has_chatbot INTEGER DEFAULT 0,
            website_score INTEGER DEFAULT 0,
            lead_score INTEGER DEFAULT 5,
            status TEXT DEFAULT 'new',
            source TEXT DEFAULT 'prospector',
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            last_contacted TEXT,
            next_followup TEXT
        );

        CREATE TABLE IF NOT EXISTS outreach_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            email_type TEXT NOT NULL,
            sent_at TEXT DEFAULT (datetime('now')),
            template_used TEXT,
            subject TEXT,
            opened INTEGER DEFAULT 0,
            replied INTEGER DEFAULT 0,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        );

        CREATE TABLE IF NOT EXISTS do_not_contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            reason TEXT,
            added_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
        CREATE INDEX IF NOT EXISTS idx_leads_industry ON leads(industry);
        CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(lead_score);
        CREATE INDEX IF NOT EXISTS idx_dnc_email ON do_not_contact(email);
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")


def import_from_excel(filepath):
    """Import leads from an Excel file."""
    if not HAS_PANDAS:
        print("ERROR: pandas required. Run: pip install pandas openpyxl")
        sys.exit(1)

    df = pd.read_excel(filepath)
    conn = get_db()
    cursor = conn.cursor()
    imported = 0
    skipped = 0

    for _, row in df.iterrows():
        name = str(row.get("business_name", "")).strip()
        if not name:
            continue

        # Check for duplicates by name + address
        existing = cursor.execute(
            "SELECT id FROM leads WHERE business_name = ? AND address = ?",
            (name, str(row.get("address", "")))
        ).fetchone()

        if existing:
            skipped += 1
            continue

        cursor.execute("""
            INSERT INTO leads (business_name, industry, address, phone, email, website,
                             google_rating, review_count, lead_score, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            str(row.get("industry", "")),
            str(row.get("address", "")),
            str(row.get("phone", "")),
            str(row.get("email", "")),
            str(row.get("website", "")),
            float(row.get("rating", 0) or 0),
            int(row.get("review_count", 0) or 0),
            int(row.get("lead_score", 5) or 5),
            "prospector"
        ))
        imported += 1

    conn.commit()
    conn.close()
    print(f"Imported: {imported} leads | Skipped (duplicates): {skipped}")


def list_leads(status=None, min_score=None, industry=None, limit=50):
    """List leads with optional filters."""
    conn = get_db()
    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if min_score:
        query += " AND lead_score >= ?"
        params.append(min_score)
    if industry:
        query += " AND industry LIKE ?"
        params.append(f"%{industry}%")

    query += " ORDER BY lead_score DESC, created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        print("No leads found matching criteria.")
        return

    print(f"\n{'ID':>4} {'Score':>5} {'Status':<14} {'Business Name':<30} {'Industry':<18} {'Phone':<16} {'Website'}")
    print("-" * 120)
    for r in rows:
        website = (r["website"] or "")[:30]
        print(f"{r['id']:>4} {r['lead_score']:>5} {r['status']:<14} {r['business_name'][:28]:<30} {(r['industry'] or '')[:16]:<18} {(r['phone'] or ''):<16} {website}")

    print(f"\nShowing {len(rows)} leads")


def update_lead(lead_id, status=None, notes=None):
    """Update a lead's status or notes."""
    conn = get_db()
    updates = []
    params = []

    if status:
        if status not in VALID_STATUSES:
            print(f"ERROR: Invalid status. Use one of: {', '.join(VALID_STATUSES)}")
            sys.exit(1)
        updates.append("status = ?")
        params.append(status)
        if status == "contacted":
            updates.append("last_contacted = datetime('now')")

    if notes:
        updates.append("notes = ?")
        params.append(notes)

    if not updates:
        print("Nothing to update. Use --status or --notes")
        return

    params.append(lead_id)
    query = f"UPDATE leads SET {', '.join(updates)} WHERE id = ?"
    conn.execute(query, params)
    conn.commit()
    conn.close()
    print(f"Lead #{lead_id} updated.")


def show_stats():
    """Show pipeline statistics."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    by_status = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM leads GROUP BY status ORDER BY cnt DESC"
    ).fetchall()
    by_industry = conn.execute(
        "SELECT industry, COUNT(*) as cnt FROM leads GROUP BY industry ORDER BY cnt DESC LIMIT 10"
    ).fetchall()
    high_score = conn.execute("SELECT COUNT(*) FROM leads WHERE lead_score >= 7").fetchone()[0]
    with_website = conn.execute("SELECT COUNT(*) FROM leads WHERE website IS NOT NULL AND website != ''").fetchone()[0]
    outreach_count = conn.execute("SELECT COUNT(*) FROM outreach_log").fetchone()[0]
    conn.close()

    print(f"\n{'='*50}")
    print(f"  JAYBIRD LEAD PIPELINE")
    print(f"{'='*50}")
    print(f"\n  Total Leads: {total}")
    print(f"  High Priority (7+): {high_score}")
    print(f"  With Website: {with_website}")
    print(f"  Emails Sent: {outreach_count}")

    print(f"\n  BY STATUS:")
    for r in by_status:
        bar = "#" * min(r["cnt"], 30)
        print(f"    {r['status']:<16} {r['cnt']:>4}  {bar}")

    print(f"\n  TOP INDUSTRIES:")
    for r in by_industry:
        bar = "#" * min(r["cnt"], 30)
        print(f"    {(r['industry'] or 'unknown')[:20]:<22} {r['cnt']:>4}  {bar}")

    print(f"\n{'='*50}\n")


def export_leads():
    """Export all leads to Excel."""
    if not HAS_PANDAS:
        print("ERROR: pandas required. Run: pip install pandas openpyxl")
        sys.exit(1)

    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY lead_score DESC", conn)
    conn.close()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"leads_export_{timestamp}.xlsx")
    df.to_excel(filepath, index=False, sheet_name="Leads")
    print(f"Exported {len(df)} leads to: {filepath}")


def search_leads(query):
    """Search leads by business name or industry."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM leads WHERE business_name LIKE ? OR industry LIKE ? ORDER BY lead_score DESC LIMIT 50",
        (f"%{query}%", f"%{query}%")
    ).fetchall()
    conn.close()

    if not rows:
        print(f"No leads matching '{query}'")
        return

    print(f"\n{'ID':>4} {'Score':>5} {'Status':<14} {'Business Name':<30} {'Industry':<18} {'Phone':<16}")
    print("-" * 100)
    for r in rows:
        print(f"{r['id']:>4} {r['lead_score']:>5} {r['status']:<14} {r['business_name'][:28]:<30} {(r['industry'] or '')[:16]:<18} {(r['phone'] or ''):<16}")


def main():
    parser = argparse.ArgumentParser(description="Jaybird Lead Database Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize the database")

    imp = subparsers.add_parser("import", help="Import leads from Excel")
    imp.add_argument("file", help="Excel file path")

    lst = subparsers.add_parser("list", help="List leads")
    lst.add_argument("--status", choices=VALID_STATUSES, help="Filter by status")
    lst.add_argument("--score", type=int, help="Minimum lead score")
    lst.add_argument("--industry", type=str, help="Filter by industry")
    lst.add_argument("--limit", type=int, default=50, help="Max results")

    upd = subparsers.add_parser("update", help="Update a lead")
    upd.add_argument("id", type=int, help="Lead ID")
    upd.add_argument("--status", choices=VALID_STATUSES, help="New status")
    upd.add_argument("--notes", type=str, help="Add notes")

    subparsers.add_parser("stats", help="Show pipeline statistics")
    subparsers.add_parser("export", help="Export leads to Excel")

    srch = subparsers.add_parser("search", help="Search leads")
    srch.add_argument("query", help="Search term")

    args = parser.parse_args()

    if args.command == "init":
        init_db()
    elif args.command == "import":
        import_from_excel(args.file)
    elif args.command == "list":
        list_leads(args.status, args.score, args.industry, args.limit)
    elif args.command == "update":
        update_lead(args.id, args.status, args.notes)
    elif args.command == "stats":
        show_stats()
    elif args.command == "export":
        export_leads()
    elif args.command == "search":
        search_leads(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
