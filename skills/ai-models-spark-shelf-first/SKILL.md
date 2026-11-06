---
name: AI Models Spark shelf first
description: >-
  Use when AI Models or Engineer recommends open-weight downloads for the DGX
  Spark - prefer NVFP4 or EXL3 on Spark (not Mac GGUF); re-list Passport shelf
  and beat local models before suggesting anything new.
---
# AI Models Spark shelf first

Before recommending a download or Passport gap, prove the existing shelf is weaker for a **single DGX Spark** job.

## Order

1. **Re-list** `/Volumes/My Passport/models` on the Mac (live inventory). Do not trust a stale snapshot. Mac is staging disk only.
2. **Filter for single-Spark fit** - one user, GB10 / sm_12.1, 128 GB unified. Serve and benchmark on the **DGX Spark**, never as a Mac-llama default when a Spark path exists.
3. **Quant preference for Spark:** prefer **NVFP4** or **EXL3** (recipe-backed). Prefer EXL3 over GGUF when both exist for the same model on one Spark. Do not lead with GGUF/llama.cpp on Mac for Spark jobs.
4. **Rank candidates against what is already on the Passport**, especially strong shelf NVFP4 / EXL3 builds. Name Hub id, quant, disk size, and why it beats a named shelf model.
5. Only then propose a download. State size and wait for an explicit yes on that exact model.

## Do not

- Pitch Passport "gaps" that do not beat what he already has for single-Spark serve
- Recommend Mac-only GGUF as the Spark path when NVFP4 or EXL3 exists
- Invent tok/s or claim an NVFP4/EXL3 repo that is not on Hub
- Start a multi-GB download without size + yes

## Output shape

Shelf check → single-Spark filter → NVFP4/EXL3 preference → vs-shelf rank (winner or "no clean upgrade") → optional download ask.
