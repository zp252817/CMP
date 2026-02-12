# Git Auto Update (GitHub Pages)

## One-time setup

1. Initialize git repo (if needed):

```bash
cd /Users/zhangpanmac/Desktop/CMP
git init
git branch -M main
git remote add origin <your-github-repo-url>
```

2. In GitHub repo settings:
- Open `Settings -> Pages`
- Set `Build and deployment` to `GitHub Actions`

3. Make sure workflow file exists:
- `/Users/zhangpanmac/Desktop/CMP/.github/workflows/deploy-knowledge-map.yml`

## Daily update flow

After you add/update docs:

```bash
cd /Users/zhangpanmac/Desktop/CMP
./scripts/km-site publish "chore(km): update knowledge map"
```

This command will:
1. Regenerate static site to `/Users/zhangpanmac/Desktop/CMP/site`
2. Commit changed files
3. Push to your current branch

If current branch is `main` (or `master`), GitHub Pages auto-deploys the same link.

## Useful commands

```bash
./scripts/km-site build
./scripts/km-site commit "chore(km): update knowledge map"
./scripts/km-site push
```
