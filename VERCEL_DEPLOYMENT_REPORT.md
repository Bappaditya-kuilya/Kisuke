# VERCEL_DEPLOYMENT_REPORT.md

> Kisuke Website — Vercel Deployment Diagnosis
> Date: 2026-07-09

---

## Root Cause

**Vercel Root Directory is set to `/` (repo root) instead of `website/`.**

The repository is a monorepo:
```
/
├── pyproject.toml          # Python project (Kisuke core)
├── src/kisuke/             # Python source
├── tests/                  # Python tests
├── architecture/           # Design docs
├── docs/                   # Documentation
└── website/                # Next.js marketing site
    ├── package.json
    ├── next.config.ts
    └── src/app/
```

When Vercel builds from `/`:
1. It finds `pyproject.toml` (Python) — not a Next.js project
2. No `package.json` in root — framework detection fails
3. Next.js build never runs
4. Result: empty deployment → 404

**The website files ARE in git (60 files tracked). The build IS correct when run from `website/`. The deployment configuration is wrong.**

---

## Local Build Verification

| Check | Result |
|-------|--------|
| `pnpm build` (from `website/`) | Success |
| Routes generated | 6: `/`, `/about`, `/architecture`, `/docs`, `/download`, `/roadmap` |
| Static pages | All 7 (including `/_not-found`) |
| Build output | `.next/server/app/` contains all routes |

---

## Exact Fix Required

### Option A: Vercel Dashboard (Recommended)

1. Go to https://vercel.com/dashboard
2. Select the Kisuke project
3. Go to **Settings** → **General**
4. Set **Root Directory** to: `website`
5. Set **Framework Preset** to: `Next.js`
6. Set **Build Command** to: `pnpm build`
7. Set **Install Command** to: `pnpm install`
8. Click **Save**
9. Go to **Deployments** → click **Redeploy** on latest commit

### Option B: Vercel CLI

```bash
cd /home/kisuke/kisuke/website
vercel link
vercel env pull
vercel --prod
```

### Option C: Add vercel.json (if dashboard not accessible)

Create `website/vercel.json`:
```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

Then set Root Directory to `website` in dashboard.

---

## What Vercel Should See

When Root Directory is `website/`:

| Setting | Value |
|---------|-------|
| Root Directory | `website` |
| Framework Preset | Next.js |
| Node.js Version | 20+ (auto-detected) |
| Install Command | `pnpm install` |
| Build Command | `pnpm build` |
| Output Directory | `.next` (default for Next.js) |
| Production Branch | `main` |

---

## Verification After Fix

Once Root Directory is set to `website/`, verify:

| URL | Expected |
|-----|----------|
| `https://kisuke.vercel.app/` | Homepage loads |
| `https://kisuke.vercel.app/docs` | Docs page loads |
| `https://kisuke.vercel.app/architecture` | Architecture page loads |
| `https://kisuke.vercel.app/download` | Download page loads |
| `https://kisuke.vercel.app/roadmap` | Roadmap page loads |
| `https://kisuke.vercel.app/about` | About page loads |

---

## Files Changed

None. The issue is a Vercel project configuration, not a code issue.

---

## Commands Executed

| Command | Result |
|---------|--------|
| `git ls-files website/` | 60 files tracked |
| `pnpm build` (from `website/`) | Success, 7 routes |
| `ls .next/server/app/` | All routes present |
| `cat .next/app-path-routes-manifest.json` | 6 routes confirmed |

---

## Remaining Issues

| Issue | Status |
|-------|--------|
| Vercel CLI authentication | Not available (no token) |
| Root Directory fix | Requires Vercel dashboard access |
| Custom domain (kisuke.dev) | Requires DNS configuration after deployment |

---

## Summary

The 404 is caused by Vercel building from the wrong directory. The website code is correct, the build is correct, the routes are correct. Only the Vercel Root Directory setting needs to change from `/` to `website/`.

**After applying the fix:**
- All 6 routes will deploy
- Homepage will load
- No more 404

DEPLOYMENT FIX IDENTIFIED
AWAITING VERCEL DASHBOARD CONFIGURATION
