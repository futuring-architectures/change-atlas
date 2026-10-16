---
id: qst-9c5469f8a83a
type: question
title: What replaces human review when software exceeds human attention?
status: open
created_at: 2026-07-14
updated_at: 2026-10-16
tags:
  - software-assurance
  - code-review
  - ai-agents
relationships:
  - type: raised_by
    target: "[[does-cheap-code-retire-technical-debt-or-amplify-architectural-debt]]"
  - type: raised_by
    target: "[[software-work-is-shifting-from-code-production-to-orchestration-and-assurance]]"
  - type: raised_by
    target: "[[ai-native-organizational-trust-stack]]"
  - type: raised_by
    target: "[[cognitive-debt]]"
description: "What evidence, controls, and accountability can establish trust when generated production code grows faster than humans can inspect it?"
origin: another_page
---

# What replaces human review when software exceeds human attention?

## Why it matters

The candidate software-work Trend moves people from writing and reading implementation toward specifying intent and evaluating systems. If code volume outgrows human attention, familiar line-by-line review can no longer be the universal trust mechanism. Removing it without a replacement turns faster production into faster accumulation of opaque risk.

## What is currently known

- [[software-work-is-shifting-from-code-production-to-orchestration-and-assurance|The candidate Trend]] documents bounded movement toward loops, integration, and generated code.
- One 2026 source predicts that unread production code will become normal and proposes “code reading coverage” as a tracked safety signal: [[write-only-code-evi-a392d13f6115#Claim 1|Write-Only Code — claim 1]] and [[write-only-code-evi-a392d13f6115#Claim 2|claim 2]].
- An existing Signal reports an agent workflow that replaces review with test iteration: [[agent-workflow-displaces-review-and-planning|An agent workflow displaces human review and planning]].
- MenuGen shows that integration failures and outdated service knowledge can remain outside the code-writing bottleneck: [[vibe-coding-menugen-evi-0ce549d72b42#Claim 2|Vibe coding MenuGen — claim 2]].
- The [[ai-native-organizational-trust-stack|AI-native organizational trust stack]] proposes data, evaluation, governance, learning, and human-judgment layers, but does not establish which assurance techniques are sufficient for generated software.
- [[ai-workslop-shifts-cognitive-labor-to-recipients|The workslop Signal]] shows that nominal review removal can reappear as unplanned downstream verification and repair.
- [[earning-judgment-evi-207760005515#Claim 4|Earning Judgment — claim 4]] proposes an evidence-bearing outer loop: humans decide what deserves attention, inspect diffs, tests, logs, and rationale, approve or block, and carry the consequence.
- [[earning-judgment-evi-207760005515#Claim 5|Earning Judgment — claim 5]] adds wrong logs, explicit eval rubrics, separate specification and verification, and autonomy calibrated to reversibility and consequence.
- Stewart Gloster poses a related capacity problem at the governance layer: decisions about access, automation, and authority may outgrow centralized case-by-case review. She proposes inherited operating controls, with identity, scoped permissions, runtime constraints, observability, and revocation enforcing decisions where action occurs: [[ai-is-making-systems-thinking-more-valuable-evi-d698feaae662#Claim 9|the review-capacity forecast]], [[ai-is-making-systems-thinking-more-valuable-evi-d698feaae662#Claim 7|reusable controls]], and [[ai-is-making-systems-thinking-more-valuable-evi-d698feaae662#Claim 13|enforceable authority]]. This concerns operational authority, not proof that generated code can safely bypass comprehension or independent evaluation.
- [[ai-is-making-systems-thinking-more-valuable-evi-d698feaae662#Claim 19|AI Is Making Systems Thinking More Valuable — claim 19]] separates outcome ownership, authority grants, data ownership, monitoring, stopping power, and responsibility for correction before an incident.

## Missing or discriminating evidence

- Comparative defect, security, recovery, and maintenance outcomes for reviewed and unread generated code.
- Assurance primitives that test behavior, invariants, provenance, dependencies, and blast radius independently of the generator.
- Evidence about which systems remain too consequential or novel to ship without human comprehension.
- Accountability mechanisms when no person can explain the implementation line by line.
- Evidence that inherited controls enforce intended limits across workflows, including revocation, exception paths, and common failures in shared infrastructure.

## Suggested next sources or actions

- Collect production incident reports from agent-generated systems.
- Compare property testing, formal methods, sandboxing, staged rollout, observability, and independent-agent review.
- Track both code-reading coverage and outcome measures so lower review does not become a self-validating efficiency target.
- Compare case-by-case approval with tested reusable constraints and risk-based escalation, while measuring bypasses, intervention effectiveness, and downstream work.

## Resolution

_Open. The corpus now supplies a concrete outer-loop pattern and several calibration practices, but it does not establish that these controls scale, remain independent, or provide sufficient assurance for consequential generated systems._

## Relationships

- Also raised by [[cognitive-debt|Cognitive debt]], which separates code correctness from recoverable system understanding.

- Raised by [[software-work-is-shifting-from-code-production-to-orchestration-and-assurance|the candidate shift toward orchestration and assurance]] and the [[ai-native-organizational-trust-stack|AI-native organizational trust stack]].
