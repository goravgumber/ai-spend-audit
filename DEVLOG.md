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

**Hours worked:** 4
**What I did:** Set up FastAPI project structure with SQLAlchemy models,
Alembic migrations, and Pydantic config. Connected to Supabase PostgreSQL.
Initialized Next.js frontend with TypeScript and Tailwind.
**What I learned:** Supabase direct connection on port 5432 is blocked by
IPv6 on Indian ISPs — had to switch to connection pooler on port 6543.
Passwords with special characters like @ break both configparser interpolation
and psycopg2 URL parsing. Fixed by resetting password to alphanumeric only.
JSONB chosen for tool_entries and results columns because each tool has
different plan structures — normalizing into columns would create a
schema nightmare.
**Blockers:** Three migration errors back to back — wrong URL format,
special character in password, IPv6 network block. All resolved.
**Plan for tomorrow:** Build audit engine with pricing catalog and unit tests.

---

## Day 3 — 2025-05-08

**Hours worked:** 4
**What I did:** Built pricing_catalog.py with all 9 tools and their plans.
Built audit_engine.py with 3 checks per tool — overpaying detection,
cheaper same-vendor plan, cheaper alternative tool. Wrote 7 unit tests,
all passing.
**What I learned:** get_cheapest_plan was returning free hobby tier as a
valid downgrade recommendation for users on paid plans. Fixed by adding
paid_only parameter to the function. Also learned that audit_engine.py
was calling the old function signature in two places — used grep to find
them and sed to fix in-place. Tests went from 5/7 to 7/7 after fixes.
**Blockers:** paid_only parameter missing from two call sites in
audit_engine.py. Located with grep, fixed with sed.
**Plan for tomorrow:** Build POST /audits API endpoint, Pydantic request
and response schemas, connect frontend form to backend.
