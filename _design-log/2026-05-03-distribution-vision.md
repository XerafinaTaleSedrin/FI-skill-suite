# Design log — Distribution model + first beta tester

**Date**: 2026-05-03 (Sunday porch session)
**Trigger**: Marika surfaced the strategic distribution model while flagging Laura Jones as a candidate first beta tester.

---

## The two-tier distribution vision

The FI-skill-suite is licensed CC BY-NC-SA 4.0 + PolyForm Noncommercial 1.0.0. That makes the suite explicitly **free for everyone, forever, with no commercial appropriation.** But "free" only practically lands for users who can:

1. Install Claude Code locally
2. Clone a GitHub repo
3. Run a CLI tool with a local data file

That's a meaningful barrier for non-technical users. The strategic move:

### Tier 1 — Self-host (free, primary tier)

- User installs Claude Code, clones the repo, runs skills locally
- All data stays on the user's machine (privacy posture from AGENTS.md is preserved)
- Free forever; the repo is the canonical artifact
- Audience: anyone tech-savvy enough to follow a 3-step setup guide

### Tier 2 — Hosted (paid, ~$10/mo to cover API costs)

- MOC runs a hosted instance the user accesses via a website
- User uploads their data per-session OR maintains a per-user encrypted-at-rest holdings file (TBD — see open question below)
- ~$10/mo to cover the Claude API token costs of running the user's skills
- Audience: users who want the FI work without the local-install lift — non-technical users, AuDHD users for whom installation is a friction wall, users who prefer "I'll just pay $10 to get this done" over "I'll spend an evening setting it up"
- Built later; not Day 1 scope

---

## Privacy architecture — open question that needs solving before Tier 2 ships

AGENTS.md privacy posture says: *"Holdings, transactions, all financial files stay on the user's machine. Period."*

A hosted Tier 2 service inherently means user financial data passes through MOC infrastructure. That's a real tension to resolve. Options:

1. **Stateless hosted runs**: user uploads their `holdings.md` per-session, skill executes, output returned, data deleted server-side. No persistence on MOC infrastructure. Closest to AGENTS.md's intent; highest friction for the user (re-upload every session).
2. **Per-user encrypted-at-rest file**: user's data persists on MOC infrastructure but encrypted with a user-controlled key (passphrase, OAuth-derived, etc.). MOC operators cannot read it. Higher convenience, more crypto/auth infrastructure to build.
3. **BYO storage**: user's data lives in their own cloud storage (Google Drive, Dropbox, S3 bucket they control). MOC service reads with user-granted token, processes, doesn't persist. Compromise: data ownership stays with user, MOC provides compute only.

This needs a real design pass before Tier 2 launches. Probably option (3) is the cleanest for the privacy posture but most expensive to build. Option (1) is the cheapest to build and most aligned with AGENTS.md, but high friction.

Logged for a future design session.

---

## Laura Jones as candidate first beta tester

LJ (Built Resilient — VA claims + financial wellness for veterans) is Marika's MOC client. Not tech-savvy, but engaged and trusting. Two reasons she's a good first tester:

1. **She'd benefit from the actual financial work.** Real hourly wage, gap-to-FI, redirect strategy — the skills produce orienting numbers that would land for her. The exercise itself has personal value beyond the testing role.
2. **Her client base is a natural Tier 2 audience.** Veterans navigating financial transitions are exactly the demographic for whom the local-install friction is too high but who'd benefit from $10/mo hosted access. If LJ can use it herself, she becomes the natural referral path to her veteran clients later — when Tier 2 ships, she's both the case study AND the channel.

The ask for Monday's call (logged in `work/clients/laura-jones/00_client-overview.md`): would she be open to running through the suite with Marika, trading time/feedback for early access?

---

## Implications for skill design

This shifts how a few things get scoped:

- **Privacy posture in user-facing docs** needs to address both tiers. AGENTS.md currently assumes self-host; needs an addendum for "if you're using the hosted version, here's what's different about your data path."
- **The /fi:holdings-scaffold privacy walkthrough** in Step 3 should branch on tier — different gitignore/encryption/storage logic for self-host vs hosted.
- **Onboarding UX** for non-technical users (Tier 2) probably needs more hand-holding than the current SKILL.md procedures assume. Could be addressed via a wrapper that simplifies the prompt language.
- **Tier 2 API cost coverage**: $10/mo per user covers ~$8 of Claude API tokens at current rates for a reasonable monthly skill-use volume, leaving ~$2 for MOC operating margin (hosting / auth / payment processing). Tight; might need pricing-pressure-test once usage patterns are real.

---

## Action items

- [ ] LJ Monday call — ask the beta-tester question (logged in client overview)
- [ ] Privacy-architecture design pass for Tier 2 before any code (option 1 / 2 / 3 above)
- [ ] If LJ says yes: she becomes the first non-Marika user. Walk her through `/fi:holdings-scaffold` and the rest of the suite as we test.
- [ ] If LJ says no or not now: keep her in mind as future case study; identify a different Tier 2 candidate (Mary? Kate's clients? E4E classmates?)

---

*Strategic vision captured. Implementation pending — Tier 2 is a future build, Tier 1 is the current focus.*
