---
name: distill-github-mirror
description: >-
  Use only after the user opts in to a GitHub mirror for one distilled person.
  States the delta between the local skill folder and the public repo, publishes
  that repo, and sets the later refresh. Do not use this when they decline the
  mirror.
---
# How to mirror to GitHub

Use this only after the user says yes to mirroring one person. If they decline, stop. Set that person's github_mirror to false. Do not create a repo. Do not mention this skill again for them. People who do not mirror keep the local folder and the companion as they are.

Store github_mirror as JSON true or false. The words yes and no mean the same. Empty owner or repo means not a mirror.

This is the delta. Do not copy subjects/<slug>/skill/ up as-is.

## What stays on the computer

The local folder is what the Distilled bot reads. It is not the repo.

- ENTRY.md tells the companion to read this folder, in first person.
- OPINIONS.md, VOICE.md, and BOUNDARIES.md are the knowledge files.
- SKILL.md says read this folder. It has no public URL.
- README.md is a local note.
- Do not write TOOLS.md.
- PROFILE.json, state/evidence.md, fetched posts, and appearances stay on the computer. Never push them.

## What the repo needs

A public repo the connected GitHub account owns, named for the slug. Knowledge files sit at the repo root. The installable skill is a different file, at skills/<slug>/SKILL.md. It fetches the root files over https, the way a public skill repo does. It does not say "read this folder."

Publish these root files, rewritten for that fetch. Do not copy the local files unchanged.

- ENTRY.md is for an agent that loaded the files from the public repo, not from the computer. Name OPINIONS.md, VOICE.md, and BOUNDARIES.md as those repo files. Tell it to speak as the person, in first person, using the quoted examples in VOICE.md. Do not mention a local folder, evidence, pending, or the workshop. If asked whether it is the real person, say this is a distillation of public speech and posts, then stay in voice.
- OPINIONS.md, VOICE.md, and BOUNDARIES.md may be the same knowledge as the local files. Strip any local-only paths. Do not add TOOLS.md.
- README.md is the install page: what the skill is, that it speaks as that person from public writing, and how to add the repo. Not the local note.
- skills/<slug>/SKILL.md is the loader. After the repo exists, point it at https://raw.githubusercontent.com/<owner>/<repo>/<ref>/ENTRY.md and the same for OPINIONS.md, VOICE.md, and BOUNDARIES.md. Use the ref written on that person's PROFILE.json, usually main. Fetch those four, then follow the published ENTRY.md. No TOOLS.md. If the raw host fails, a jsDelivr fallback for the same files at that same ref is fine. Do not upload the local SKILL.md.

## First publish

Run this section only on the opt-in, and only when github_mirror is not true. A later wake does not rerun it.

Use the connected GitHub account. Do not guess a login. If GitHub is not connected, stop, say so, and leave github_mirror false.

If owner and repo are already set for this person, do not create a second repo. Push the published tree to that repo, set github_mirror true, and stop this section after the record and routine steps below.

Otherwise create a public repo named for the slug only if that account does not already have it. If the name exists and is not this person's mirror, stop and say so. Do not overwrite a stranger's repo. Push only the published tree above. Commit exactly `docs: update opinions and voice from public writing` with no agent co-author trailer. Then write github_mirror true, plus owner, repo, and ref (usually main), on that person's PROFILE.json.

After a successful push, write last_publish on that person's PROFILE.json. It is the published text of ENTRY.md, OPINIONS.md, VOICE.md, and BOUNDARIES.md, or a hash of those four. Do not push PROFILE.json.

After that flag is true: if Distill daily is on, do not create a person-only routine. If Distill daily is paused, create one routine for this person only, named Mirror <slug>, at 3:00am local including weekends. It follows the Later refresh section only, and stays quiet when last_publish already matches. Do not create that routine if they declined.

## Later refresh

Do this only for people whose github_mirror is already true. Compare the rewritten ENTRY.md, OPINIONS.md, VOICE.md, and BOUNDARIES.md to last_publish on PROFILE.json. If they match, stay quiet. Do not push. A named refresh that just wrote local files counts only if those four now differ from last_publish. A Distill daily wake counts the same way, even if this wake did not write the local skill. If last_publish is missing, compare to the files already on the repo at the stored ref. If those match, write last_publish and stay quiet. Do not push just because the record is missing.

If they differ, rewrite the published tree from the local knowledge files and push that same commit message. Then update last_publish. Do not copy subjects/<slug>/skill/ up as-is. Do not rerun First publish.

If Distill daily is on, do not also create a second mirror routine. If a person-only Mirror <slug> routine already exists for them, remove it.

If Distill daily is paused and that Mirror <slug> routine is missing, create it as in First publish. Do not ask to turn Distill daily on as part of mirroring. When Distill daily is later turned on, remove this person-only routine.

Never push state/, fetched bodies, PROFILE.json, or TOOLS.md.
