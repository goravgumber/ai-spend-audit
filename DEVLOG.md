## Day 1 — 2025-05-06

**Hours worked:** 2
**What I did:** Read the full assignment 3 times. Set up repo.
Researched pricing for all 9 tools. Scheduled user interviews.
**What I learned:** The audit engine needs real defensible pricing
data — hardcoded, cited. The entrepreneurial files (GTM, ECONOMICS)
are 25 points — highest weight.
**Blockers:** None yet.
**Plan for tomorrow:** Initialize FastAPI + Next.js project structure.
Design database schema.

---

## Day 2 — 2025-05-07

**Hours worked:** 0
**What I did:** No work done. Was out of station with family — no laptop access.
**What I learned:** —
**Blockers:** No laptop, away from home.
**Plan for tomorrow:** Complete Day 2 tasks — FastAPI skeleton, database
setup, Next.js initialization.

---

## Day 3 — 2025-05-08

**Hours worked:** 8
**What I did:** Completed Day 2 and Day 3 tasks together. Set up FastAPI
project structure with SQLAlchemy models, Alembic migrations, and Pydantic
config. Connected to Supabase PostgreSQL. Initialized Next.js frontend with
TypeScript and Tailwind. Built pricing_catalog.py with all 9 tools and their
plans. Built audit_engine.py with 3 checks per tool — overpaying detection,
cheaper same-vendor plan, cheaper alternative tool. Wrote 7 unit tests,
all passing.
**What I learned:** Supabase direct connection on port 5432 is blocked by
IPv6 on Indian ISPs — had to switch to connection pooler on port 6543.
Passwords with special characters like @ break configparser interpolation
and psycopg2 URL parsing — fixed by resetting to alphanumeric password.
JSONB chosen for tool_entries and results columns because each tool has
different plan structures. get_cheapest_plan was returning free hobby tier
as valid downgrade for paid plan users — fixed by adding paid_only parameter.
audit_engine.py was calling old function signature in two places — used
grep to locate, sed to fix in-place. Tests went from 5/7 to 7/7.
**Blockers:** Three migration errors — wrong URL format, special character
in password, IPv6 block. All resolved. paid_only missing from two call sites,
fixed with grep + sed.
**Plan for tomorrow:** Build POST /audits API endpoint, Pydantic schemas,
connect frontend form to backend, build results page.
