# NCC Portal – Army Wing
### Role-Based Cadet Management System

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open in browser
http://127.0.0.1:5000
```

---

## Demo Login Credentials

| Role | Username | Password |
|------|----------|----------|
| ANO (Admin) | `ano_sharma` | `ano123` |
| Cadet Captain | `cc_rahul` | `cc123` |
| Leading Cadet | `lc_priya` | `lc123` |
| Cadet | `cdt_arjun` | `cdt123` |

---

## Features

### Role Hierarchy
- **ANO** – Full admin: CRUD cadets, manage users, unfreeze attendance, approve/reject change requests
- **CC** – Take & submit attendance (freezes on submit), edit cadets, post announcements, submit change requests
- **LC** – View cadets and announcements only
- **Cadet** – View own profile, attendance history, and announcements

### Modules
| Module | ANO | CC | LC | Cadet |
|--------|-----|----|----|-------|
| Dashboard | ✅ | ✅ | ✅ | ✅ |
| Cadet Register (view) | ✅ | ✅ | ✅ | Own only |
| Cadet CRUD | ✅ Full | ✅ Add/Edit | ❌ | ❌ |
| Attendance | ✅ + Unfreeze | ✅ Submit→Freeze | ❌ | ❌ |
| Attendance Report | ✅ All | ✅ All | ✅ All | Own only |
| Announcements (view) | ✅ | ✅ | ✅ | ✅ |
| Announcements (post/del) | ✅ | ✅ | ❌ | ❌ |
| User Management | ✅ | ❌ | ❌ | ❌ |
| Change Requests | ✅ Review | ✅ Submit | ❌ | ❌ |

### Attendance Change Request Workflow
1. CC submits attendance → record is frozen
2. CC clicks "Request Change" on any frozen entry → fills cadet, date, old→new status, reason
3. ANO sees badge notification in sidebar
4. ANO reviews in "Change Requests" panel → Approve or Reject
5. If approved: attendance record is updated automatically
6. If rejected: optional rejection note visible to CC

---

## Data Storage
All data is stored in `data.json` in the project root (auto-created on first run with demo data).

## Project Structure
```
ncc_portal/
├── app.py              ← Flask application (all routes & logic)
├── data.json           ← Auto-generated data store
├── requirements.txt
├── README.md
└── templates/
    ├── login.html      ← Login page
    └── index.html      ← Main SPA dashboard
```

## Tech Stack
- **Backend**: Python / Flask
- **Frontend**: Vanilla JS SPA (no framework needed)
- **Storage**: JSON file (no database required)
- **Fonts**: Bebas Neue, Rajdhani, Space Mono (Google Fonts)
