# Walkthrough pattern (project-agnostic)

Use the same **phase skeleton** you see in **[How-To.md](./How-To.md)** for DeepTutor—or for **any** repo you want strangers (or future you) to run without guessing.

**Using-superpowers:** One phase = one decision surface; order is fixed; optional paths are labeled **A / B / C**, not buried in prose.

---

## Phase template

| § | Purpose | Reader finishes with |
|---|---------|----------------------|
| **0** | Prerequisites | Versions checked; knows what keys/accounts are needed |
| **1** | Enter project | Correct `cd`; knows clone vs zip |
| **2** | Language/runtime env | venv/conda activated |
| **3** | Install | One chosen profile (wizard vs manual vs minimal) |
| **4** | Secrets/config | `.env` or equivalent copied from example |
| **5** | Run primary surface | One command, one URL or one CLI ping |
| **6** | Verify (optional) | Smoke test or health check |
| **7** | Alternate topology (optional) | Docker, split processes, production notes |

Add a **mental model** section (3–7 bullets): what each top-level directory does.

---

## Writing rules

1. **Link upstream README** for truth that changes every release; local doc is the **short path**.
2. **Never duplicate secrets** — point at `.env.example` only.
3. **One happy path per §3 choice** — avoid “you could also…” mid-step.
4. **Absolute paths** only in personal hub docs (`MY_SETUP`); **relative** in portable repo docs.

---

## Where this repo uses it

- Checkout-local: `DeepTutor-main/How-To.md` (relative links).
- Hub: `MY_SETUP/How-To.md` (machine paths + standalone `deeptutor-mimic`).
- Standalone app + helpers: `MY_SETUP/deeptutor-mimic/RUNBOOK.md` + `mimic-scripts/` (`set-root.sh` defaults `DEEPTUTOR_ROOT` to that folder).
