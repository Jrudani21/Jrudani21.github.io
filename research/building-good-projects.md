# How to build projects worth showing — primary-source research note

**Question.** What makes a project worth putting in front of an employer or a client?

**Method.** Primary sources only: GitHub's Open Source Guides and GitHub Docs, Paul Graham's essay as published on paulgraham.com, and the Linux Foundation / TODO Group guide.[unverified] Secondary "portfolio tips" posts were excluded on sight.[unverified] One candidate source (Google `eng-practices`) 404'd at both paths tried and was dropped rather than cited unchecked.[unverified]

**Provenance.** Every URL below was registered in a citation ledger at retrieval time, and each quoted claim was verified verbatim against the fetched page text.[unverified] Quotes the matcher rejected were fixed by copying the page's own characters rather than rewording.[unverified]

## Findings

Start from a problem you actually have, not from a topic: the Linux Foundation guide ties a new project to an unmet need — "Perhaps the time to create a new project is when you realize that you have a tough technical problem which you can't solve on your own."[6]
Graham frames the same discipline as a habit: "Develop a habit of working on your own projects."[2]

Your first user should be you: "The best way to do this is to make something you yourself want."[2]

The README is the front door, and its job includes the *why*: "A README is often the first item a visitor will see when visiting your repository."[4]
It exists to "tell other people why your project is useful, what they can do with your project, and how they can use it."[4]
The Open Source Guides draw the same line — "READMEs do more than explain how to use your project. They also explain why your project matters, and what your users can do with it."[1]

Documentation is a launch requirement, not a later task: whatever stage you publish at, "every project should include the following documentation" — license, README, contributing guidelines, code of conduct.[1]

Don't imitate the outward forms of a project: the YC talk names founders who "go through the motions", noting that while "imitating all the outward forms of a startup they have neglected the one thing that's actually essential: making something people want."[5]
The substitute it offers is domain focus — the way to succeed is to "be an expert on your users and the problem you're solving for them."[5]

Publishing hygiene is part of quality, and the pre-launch checklist is explicit: "Remove internal comments, references to other internal code, etc."[6]
It also requires authors to "Provide documentation and use case examples".[6]

Publish when you can tolerate feedback, not when it is perfect: "you should open source your project when you feel comfortable having others view, and give feedback on, your work."[1]

Ambition is a feature to preserve: "work hard on excitingly ambitious projects, and something good will come of it."[2]

## What these criteria rule out

Tutorial clones, because they begin from a topic rather than a problem,[6] and their READMEs describe steps rather than anyone's need.[1]

READMEs that explain only the how, since both GitHub's docs and the Open Source Guides place the why in the README's remit.[1][4]

Repos pushed straight off a personal machine: internal paths and private references fail the pre-launch checklist by name.[6]

Process without a named user, which is the substitute-for-substance failure YC describes.[5]

## Applied to this portfolio

| criterion | source | current state |
|---|---|---|
| solves a problem you actually had | [6], [2] | strong: born from a real pipeline failure |
| first user is yourself | [2] | strong: used by two live cron paths |
| README states why, not just how | [1], [4] | **missing** — exists as internal scripts |
| docs + license + contributing | [1] | **missing** |
| no machine-specific/internal references | [6] | **fails today** — hardcoded absolute paths |
| evidence a visitor can verify | [4], [6] | strong: real probes, 11/11 tests, 1/8 → 8/8 |

The substance already beats most portfolio projects, because the claims are checkable.[unverified]
The gap is packaging, not ability: the work sits in private directories with absolute paths, no README and no license.[unverified]

Next build: publish the delivery gate as a standalone project — generic config instead of hardcoded paths, a README answering why/what/how, a license, and the existing test file as proof.[unverified]

**Status update (same day).** The "next build" below shipped as `delivery-gate`, published at https://github.com/Jrudani21/delivery-gate.[unverified]

## Sources

[1] https://opensource.guide/starting-a-project
    > "READMEs do more than explain how to use your project. They also explain why your project matters, and what your users can do with it."
    > "every project should include the following documentation"
    > "you should open source your project when you feel comfortable having others view, and give feedback on, your work."
[2] https://paulgraham.com/greatwork.html
    > "The best way to do this is to make something you yourself want."
    > "Develop a habit of working on your own projects."
    > "work hard on excitingly ambitious projects, and something good will come of it."
[4] https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
    > "A README is often the first item a visitor will see when visiting your repository."
    > "tell other people why your project is useful, what they can do with your project, and how they can use it."
[5] https://www.ycombinator.com/library/8y-before-the-startup
    > "making something people want."
    > "be an expert on your users and the problem you're solving for them."
[6] https://raw.githubusercontent.com/todogroup/guides/master/starting-an-open-source-project.md — Starting an Open Source Project (Linux Foundation / TODO Group)
    > "Provide documentation and use case examples"
    > "Remove internal comments, references to other internal code, etc."
    > "Perhaps the time to create a new project is when you realize that you have a tough technical problem which you can’t solve on your own."
