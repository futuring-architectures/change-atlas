---
id: sig-4ef398f737a6
type: signal
title: MenuGen moves app building from coding to integration
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - vibe-coding
  - software-engineering
  - integration
relationships:
  - type: supports
    target: "[[software-work-is-shifting-from-code-production-to-orchestration-and-assurance]]"
description: "A technically sophisticated non-web developer built and deployed a paid application without directly writing its code, while most effort shifted into service configuration and integration."
evidence:
  - "[[vibe-coding-menugen-evi-0ce549d72b42#Claim 1]]"
  - "[[vibe-coding-menugen-evi-0ce549d72b42#Claim 2]]"
---

# MenuGen moves app building from coding to integration

## Observation

In April 2025, Andrej Karpathy reported building MenuGen end to end with AI coding tools despite little web-development experience and without directly writing the application code. The prototype appeared quickly; deployment required substantial work across APIs, authentication, hosting, configuration, rate limits, and service integration.

## Scope and timing

- Scope: One solo-built web application created by a technically sophisticated AI practitioner.
- Observation date: 2025-04-27.
- Date confidence: High for the publication and reported case; the duration of the build is not stated precisely.

## Evidence

- [[vibe-coding-menugen-evi-0ce549d72b42#Claim 1|Vibe coding MenuGen — claim 1]] reports the increased speed and feasibility of building the application.
- [[vibe-coding-menugen-evi-0ce549d72b42#Claim 2|Vibe coding MenuGen — claim 2]] identifies pre-LLM developer infrastructure as the principal source of friction.

## Limitations and alternative readings

- The case does not estimate productivity for a representative novice or professional team.
- Karpathy’s technical judgment likely helped him diagnose failures despite not writing the code directly.
- The case demonstrates task relocation, not effortlessness: work moved from code production into configuration, verification, and integration.

## Relationships

- The case [[software-work-is-shifting-from-code-production-to-orchestration-and-assurance|supports the candidate Trend from direct coding toward orchestration and assurance]].
