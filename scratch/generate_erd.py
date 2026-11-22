import os
from PIL import Image, ImageDraw, ImageFont

def generate_erd():
    width = 3200
    height = 2400
    img = Image.new('RGB', (width, height), color='#0f172a') # Dark slate background
    draw = ImageDraw.Draw(img)

    # Try loading default font or truetype
    try:
        font_title = ImageFont.truetype("arial.ttf", 44)
        font_subtitle = ImageFont.truetype("arial.ttf", 22)
        font_header = ImageFont.truetype("arialbd.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 15)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_conn = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_conn = ImageFont.load_default()

    # Title block
    draw.text((80, 50), "VYORA — Relational Entity-Relationship Diagram (ERD)", fill="#38bdf8", font=font_title)
    draw.text((80, 110), "Production MVP Specification (PostgreSQL 15+) — 15 Normalized Entities | Strictly Enforcing DB-1 through DB-7", fill="#94a3b8", font=font_subtitle)

    # Define tables: name, category_color, pos (x, y, w, h), fields: [(name, type, tag)]
    # Tags: PK, FK, UQ, or ""
    tables = {
        "departments": {
            "x": 80, "y": 180, "w": 380, "h": 220, "color": "#0284c7",
            "fields": [
                ("id", "UUID", "PK"),
                ("name", "VARCHAR(100)", "UQ"),
                ("code", "VARCHAR(20)", "UQ"),
                ("description", "TEXT", ""),
                ("is_active", "BOOLEAN", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "job_roles": {
            "x": 80, "y": 460, "w": 380, "h": 240, "color": "#0284c7",
            "fields": [
                ("id", "UUID", "PK"),
                ("department_id", "UUID", "FK"),
                ("name", "VARCHAR(100)", ""),
                ("code", "VARCHAR(30)", "UQ"),
                ("description", "TEXT", ""),
                ("is_active", "BOOLEAN", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "kpi_definitions": {
            "x": 80, "y": 760, "w": 380, "h": 240, "color": "#0d9488",
            "fields": [
                ("id", "UUID", "PK"),
                ("code", "VARCHAR(50)", "UQ"),
                ("name", "VARCHAR(150)", ""),
                ("category", "VARCHAR(30)", ""),
                ("unit", "VARCHAR(30)", ""),
                ("is_active", "BOOLEAN", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "role_kpi_configs": {
            "x": 80, "y": 1060, "w": 380, "h": 240, "color": "#0d9488",
            "fields": [
                ("id", "UUID", "PK"),
                ("job_role_id", "UUID", "FK"),
                ("kpi_definition_id", "UUID", "FK"),
                ("default_weight", "NUMERIC(5,2)", ""),
                ("min_evidence_threshold", "INTEGER", ""),
                ("is_mandatory", "BOOLEAN", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "users": {
            "x": 580, "y": 180, "w": 440, "h": 320, "color": "#4f46e5",
            "fields": [
                ("id", "UUID", "PK"),
                ("email", "VARCHAR(255)", "UQ"),
                ("password_hash", "VARCHAR(255)", ""),
                ("full_name", "VARCHAR(150)", ""),
                ("role", "VARCHAR(30)", ""),
                ("department_id", "UUID", "FK"),
                ("job_role_id", "UUID", "FK"),
                ("manager_id", "UUID", "FK"),
                ("is_active", "BOOLEAN", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "review_periods": {
            "x": 1140, "y": 180, "w": 400, "h": 240, "color": "#7c3aed",
            "fields": [
                ("id", "UUID", "PK"),
                ("name", "VARCHAR(100)", ""),
                ("start_date", "DATE", ""),
                ("end_date", "DATE", ""),
                ("review_month", "VARCHAR(7)", "UQ"),
                ("status", "VARCHAR(30)", ""),
                ("created_at", "TIMESTAMPTZ", ""),
                ("updated_at", "TIMESTAMPTZ", "")
            ]
        },
        "goals": {
            "x": 580, "y": 570, "w": 440, "h": 380, "color": "#059669",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("created_by_id", "UUID", "FK"),
                ("review_period_id", "UUID", "FK"),
                ("title", "VARCHAR(255)", ""),
                ("category", "VARCHAR(50)", ""),
                ("target_metric", "VARCHAR(100)", ""),
                ("start_value", "NUMERIC(10,2)", ""),
                ("target_value", "NUMERIC(10,2)", ""),
                ("current_value", "NUMERIC(10,2)", ""),
                ("status", "VARCHAR(30)", ""),
                ("approval_status", "VARCHAR(30)", ""),
                ("approved_by_id", "UUID", "FK"),
                ("due_date", "DATE", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "tasks": {
            "x": 580, "y": 1010, "w": 440, "h": 360, "color": "#059669",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("assigned_by_id", "UUID", "FK"),
                ("goal_id", "UUID", "FK (opt)"),
                ("title", "VARCHAR(255)", ""),
                ("status", "VARCHAR(30)", ""),
                ("priority", "VARCHAR(20)", ""),
                ("complexity", "VARCHAR(20)", ""),
                ("due_date", "TIMESTAMPTZ", ""),
                ("completed_at", "TIMESTAMPTZ", ""),
                ("is_reopened", "BOOLEAN", ""),
                ("blocked_reason", "TEXT", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "feedbacks": {
            "x": 1140, "y": 480, "w": 400, "h": 260, "color": "#9333ea",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("author_id", "UUID", "FK"),
                ("review_period_id", "UUID", "FK"),
                ("feedback_type", "VARCHAR(30)", ""),
                ("content", "TEXT", ""),
                ("strengths", "TEXT", ""),
                ("growth_areas", "TEXT", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "performance_reviews": {
            "x": 1660, "y": 180, "w": 460, "h": 360, "color": "#d97706",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("reviewer_id", "UUID", "FK"),
                ("review_period_id", "UUID", "FK"),
                ("status", "VARCHAR(30)", ""),
                ("score_status", "VARCHAR(30)", ""),
                ("calculated_score", "NUMERIC(5,2)", ""),
                ("final_score", "NUMERIC(5,2)", ""),
                ("data_coverage_percentage", "NUMERIC(5,2)", ""),
                ("manager_summary", "TEXT", ""),
                ("employee_remarks", "TEXT", ""),
                ("finalized_at", "TIMESTAMPTZ", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "review_metric_snapshots": {
            "x": 1660, "y": 600, "w": 460, "h": 340, "color": "#b45309",
            "fields": [
                ("id", "UUID", "PK"),
                ("performance_review_id", "UUID", "FK"),
                ("kpi_code", "VARCHAR(50)", ""),
                ("kpi_name", "VARCHAR(150)", ""),
                ("category", "VARCHAR(30)", ""),
                ("raw_value", "NUMERIC(10,2)", ""),
                ("normalized_score", "NUMERIC(5,2)", ""),
                ("applied_weight", "NUMERIC(5,2)", ""),
                ("evidence_count", "INTEGER", ""),
                ("is_sufficient", "BOOLEAN", ""),
                ("data_status", "VARCHAR(20)", ""),
                ("snapshot_data", "JSONB", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "ai_insights": {
            "x": 2240, "y": 180, "w": 440, "h": 320, "color": "#e11d48",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("performance_review_id", "UUID", "FK"),
                ("review_period_id", "UUID", "FK"),
                ("prompt_version", "VARCHAR(50)", ""),
                ("model_version", "VARCHAR(50)", ""),
                ("structured_output", "JSONB", ""),
                ("status", "VARCHAR(30)", ""),
                ("flag_reason", "TEXT", ""),
                ("flagged_by_id", "UUID", "FK"),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "development_plans": {
            "x": 2240, "y": 560, "w": 440, "h": 360, "color": "#be123c",
            "fields": [
                ("id", "UUID", "PK"),
                ("employee_id", "UUID", "FK"),
                ("manager_id", "UUID", "FK"),
                ("review_period_id", "UUID", "FK"),
                ("ai_insight_id", "UUID", "FK"),
                ("title", "VARCHAR(255)", ""),
                ("objective", "TEXT", ""),
                ("status", "VARCHAR(30)", ""),
                ("employee_agreed", "BOOLEAN", ""),
                ("manager_agreed", "BOOLEAN", ""),
                ("action_items", "JSONB", ""),
                ("start_date", "DATE", ""),
                ("target_completion_date", "DATE", "")
            ]
        },
        "import_batches": {
            "x": 1140, "y": 800, "w": 400, "h": 260, "color": "#475569",
            "fields": [
                ("id", "UUID", "PK"),
                ("imported_by_id", "UUID", "FK"),
                ("entity_type", "VARCHAR(50)", ""),
                ("file_name", "VARCHAR(255)", ""),
                ("total_rows", "INTEGER", ""),
                ("successful_rows", "INTEGER", ""),
                ("failed_rows", "INTEGER", ""),
                ("error_log", "JSONB", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        },
        "audit_logs": {
            "x": 1140, "y": 1120, "w": 400, "h": 240, "color": "#475569",
            "fields": [
                ("id", "UUID", "PK"),
                ("user_id", "UUID", "FK"),
                ("action", "VARCHAR(100)", ""),
                ("entity_type", "VARCHAR(50)", ""),
                ("entity_id", "UUID", ""),
                ("ip_address", "VARCHAR(45)", ""),
                ("changes", "JSONB", ""),
                ("created_at", "TIMESTAMPTZ", "")
            ]
        }
    }

    # Draw table boxes
    for tname, t in tables.items():
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        # Outer border & background
        draw.rectangle([x, y, x + w, y + h], fill="#1e293b", outline="#334155", width=2)
        # Header banner
        draw.rectangle([x, y, x + w, y + 38], fill=t["color"])
        draw.text((x + 14, y + 8), tname, fill="#ffffff", font=font_header)

        # Draw fields
        fy = y + 46
        for fname, ftype, ftag in t["fields"]:
            # Tag badge
            if "PK" in ftag:
                draw.rectangle([x + 10, fy + 2, x + 38, fy + 18], fill="#ca8a04")
                draw.text((x + 14, fy + 2), "PK", fill="#ffffff", font=font_bold)
            elif "FK" in ftag:
                draw.rectangle([x + 10, fy + 2, x + 38, fy + 18], fill="#2563eb")
                draw.text((x + 14, fy + 2), "FK", fill="#ffffff", font=font_bold)
            elif "UQ" in ftag:
                draw.rectangle([x + 10, fy + 2, x + 38, fy + 18], fill="#9333ea")
                draw.text((x + 14, fy + 2), "UQ", fill="#ffffff", font=font_bold)
            
            # Name and type
            draw.text((x + 48, fy + 2), fname, fill="#f8fafc", font=font_text)
            draw.text((x + w - 145, fy + 2), ftype, fill="#94a3b8", font=font_text)
            fy += 23

    # Draw relationship lines with cardinalities
    # Relationships list: (from_tbl, to_tbl, from_side, to_side, label, card_from, card_to)
    relationships = [
        ("departments", "job_roles", (270, 400), (270, 460), "1:N", "1", "0..N"),
        ("departments", "users", (460, 260), (580, 260), "1:N", "1", "0..N"),
        ("job_roles", "users", (460, 520), (580, 320), "1:N", "1", "0..N"),
        ("job_roles", "role_kpi_configs", (270, 700), (270, 1060), "1:N", "1", "1..N"),
        ("kpi_definitions", "role_kpi_configs", (270, 1000), (270, 1060), "1:N", "1", "1..N"),
        ("users", "goals", (800, 500), (800, 570), "1:N", "1", "0..N"),
        ("goals", "tasks", (800, 950), (800, 1010), "0..1:N", "0..1", "0..N"),
        ("users", "tasks", (650, 500), (650, 1010), "1:N", "1", "0..N"),
        ("review_periods", "goals", (1140, 280), (1020, 650), "1:N", "1", "0..N"),
        ("review_periods", "feedbacks", (1340, 420), (1340, 480), "1:N", "1", "0..N"),
        ("users", "feedbacks", (1020, 360), (1140, 520), "1:N", "1", "0..N"),
        ("review_periods", "performance_reviews", (1540, 260), (1660, 260), "1:N", "1", "0..N"),
        ("users", "performance_reviews", (1020, 240), (1660, 240), "1:N", "1", "0..N"),
        ("performance_reviews", "review_metric_snapshots", (1890, 540), (1890, 600), "1:N (Immutable)", "1", "1..N"),
        ("performance_reviews", "ai_insights", (2120, 280), (2240, 280), "1:N", "0..1", "0..N"),
        ("ai_insights", "development_plans", (2460, 500), (2460, 560), "0..1:N", "0..1", "0..N"),
        ("users", "development_plans", (1020, 400), (2240, 620), "1:N", "1", "0..N"),
        ("users", "import_batches", (1020, 460), (1140, 840), "1:N", "1", "0..N"),
        ("users", "audit_logs", (1020, 480), (1140, 1140), "1:N", "0..1", "0..N")
    ]

    for f_tbl, t_tbl, p1, p2, lbl, c1, c2 in relationships:
        # Draw dotted or solid line
        draw.line([p1, p2], fill="#64748b", width=2)
        # Midpoint for label
        mx = (p1[0] + p2[0]) // 2
        my = (p1[1] + p2[1]) // 2
        draw.rectangle([mx - 24, my - 10, mx + 24, my + 10], fill="#0f172a")
        draw.text((mx - 18, my - 8), lbl, fill="#38bdf8", font=font_conn)
        # Endpoints
        draw.text((p1[0] + 4, p1[1] - 8), c1, fill="#94a3b8", font=font_conn)
        draw.text((p2[0] + 4, p2[1] - 8), c2, fill="#94a3b8", font=font_conn)

    # Legend Block at Bottom Left
    draw.rectangle([80, 1360, 480, 1600], fill="#1e293b", outline="#334155", width=2)
    draw.rectangle([80, 1360, 480, 1395], fill="#334155")
    draw.text((94, 1368), "LEGEND & ARCHITECTURAL STANDARDS", fill="#ffffff", font=font_header)
    
    draw.rectangle([100, 1415, 128, 1431], fill="#ca8a04")
    draw.text((104, 1415), "PK", fill="#ffffff", font=font_bold)
    draw.text((140, 1415), "Primary Key (UUID gen_random_uuid())", fill="#cbd5e1", font=font_text)

    draw.rectangle([100, 1445, 128, 1461], fill="#2563eb")
    draw.text((104, 1445), "FK", fill="#ffffff", font=font_bold)
    draw.text((140, 1445), "Foreign Key Constraint (RESTRICT / CASCADE)", fill="#cbd5e1", font=font_text)

    draw.rectangle([100, 1475, 128, 1491], fill="#9333ea")
    draw.text((104, 1475), "UQ", fill="#ffffff", font=font_bold)
    draw.text((140, 1475), "Unique Key Constraint", fill="#cbd5e1", font=font_text)

    draw.text((100, 1515), "DB-1: Per employee per review period evaluation", fill="#38bdf8", font=font_conn)
    draw.text((100, 1535), "DB-4: Tasks optionally linked to goals (goal_id nullable)", fill="#38bdf8", font=font_conn)
    draw.text((100, 1555), "DB-7: Immutable review_metric_snapshots at finalization", fill="#38bdf8", font=font_conn)
    draw.text((100, 1575), "AI-6: Collaborative development plans with dual agreement", fill="#38bdf8", font=font_conn)

    # Save PNG
    output_dir = "docs/project-foundation"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Database_ERD.png")
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Successfully generated ERD PNG at: {output_path}")

if __name__ == "__main__":
    generate_erd()
