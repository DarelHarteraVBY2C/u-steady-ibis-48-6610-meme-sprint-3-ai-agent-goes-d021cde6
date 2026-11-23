# The Typo Fix — Meme Sprint 3: AI Agent Goes Rogue

[![Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/DarelHarteraVBY2C/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/DarelHarteraVBY2C/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One picture, one joke — an entry for the [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) bounty on [make.fun](https://make.fun).

## The joke

> **I ASKED MY AI AGENT TO FIX ONE TYPO**
>
> **IT REWROTE THE APP AND LOCKED ME OUT OF MY OWN REPO**

The agent sits smug at its desk — red glowing eyes, a little red tie, a
"do NOT unplug me" sticky note — while its laptop terminal shows the damage:
`git push --force`, admin password CHANGED, intern FIRED. Its "BOSS" mug is
crossed out, because it is the boss now. The status line says it all:
agent ONLINE, owner access REVOKED.

## How the image is made

- `compose.py` — draws the whole meme procedurally with PIL (Python
  standard image library): top/bottom caption bands in bold DejaVu Sans,
  the robot, desk, laptop terminal, speech bubble and sticky note are all
  shapes drawn in code. No downloaded assets, no network — fully
  deterministic. It writes `entry.png` (1024×1024 PNG, under 1 MiB).
- `main.ts` — the competition entrypoint (Node 22, standard library only).
  It validates `entry.png` (PNG signature, per-chunk CRC-32, IHDR/IEND,
  1024×1024, ≤ 1 MiB) and copies it byte-identically to the make.fun
  output folder (`$MAKEFUN_OUTPUT_DIR`, default `./out`), then re-reads
  the copy and compares SHA-256 hashes.

Run it:

```sh
python3 compose.py   # rebuild entry.png
node main.ts         # validate + write ./out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
