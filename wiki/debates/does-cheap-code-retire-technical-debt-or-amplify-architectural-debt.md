---
id: deb-e2dda82f3569
type: debate
title: Does cheap code retire technical debt or amplify architectural debt?
status: open
created_at: 2026-07-14
updated_at: 2026-07-14
tags: ["software-engineering", "technical-debt", "ai-coding"]
relationships:
  - type: supported_by
    target: "[[agentic-development-folded-requirements-into-iteration]]"
  - type: supported_by
    target: "[[architecture-is-the-scaling-constraint]]"
  - type: qualifies
    target: "[[software-work-is-shifting-from-code-production-to-orchestration-and-assurance]]"
  - type: raises_question
    target: "[[what-replaces-human-review-when-software-exceeds-human-attention]]"
description: "Cheap generation and remediation could make code disposable, or increase change volume until coherence, verification, and architecture become the dominant debt."
evidence:
  - "[[entering-technical-debt-s-zirp-era-evi-08371ea1fa15#Claim 1]]"
  - "[[entering-technical-debt-s-zirp-era-evi-08371ea1fa15#Claim 2]]"
  - "[[the-software-development-lifecycle-is-dead-evi-de2981d8e0b9#Claim 1]]"
  - "[[the-vibes-dont-scale-evi-e058bb26186a#Claim 1]]"
  - "[[the-vibes-dont-scale-evi-e058bb26186a#Claim 2]]"
---

# Does cheap code retire technical debt or amplify architectural debt?

## Central question

When AI makes code generation and modification cheap, does debt lose force because teams can repair or replace implementations quickly, or does abundant change create more incoherence than organizations can evaluate and integrate?

## Position A

Cheap remediation changes the economics of quality. Teams can generate many mutations, test them rapidly, replace poor implementations, and treat more software as disposable. Requirements can emerge through iteration because the cost of trying another version is low.

## Position B

Code is only one layer of debt. Higher change volume increases dependencies, inconsistent assumptions, security exposure, migration cost, and verification load. Architecture, domain boundaries, conventions, and decisions about what to build become more—not less—important.

## Additional positions

- Both can be true at different layers: implementation debt falls while architectural and institutional debt rises.
- Cheap replacement may work for isolated, well-tested components but fail for long-lived systems with hidden coupling.
- The decisive variable may be evaluation quality: generation helps only where selection signals represent the outcomes that matter.

## Sources of disagreement

- Whether “cost of change” includes review, integration, deployment, migration, coordination, and failure.
- Whether generated variants can be evaluated automatically.
- Whether the system is disposable or institutionally embedded.
- Whether architecture is treated as up-front specification or an evolving constraint system.

## Evidence

- [[entering-technical-debt-s-zirp-era-evi-08371ea1fa15#Claim 1|Entering Technical Debt's ZIRP Era — claim 1]] forecasts variant-and-selection development; [[entering-technical-debt-s-zirp-era-evi-08371ea1fa15#Claim 2|claim 2]] interprets lower remediation costs as a change in quality production.
- [[the-software-development-lifecycle-is-dead-evi-de2981d8e0b9#Claim 1|The Software Development Lifecycle Is Dead — claim 1]] describes requirements moving into iteration.
- [[the-vibes-dont-scale-evi-e058bb26186a#Claim 1|The Vibes Don’t Scale — claim 1]] relocates the bottleneck to what should be built and how it coheres; [[the-vibes-dont-scale-evi-e058bb26186a#Claim 2|claim 2]] argues architecture matters more at high throughput.

## Current assessment

The evidence supports bottleneck relocation more strongly than debt elimination. Cheap code and cheap change are not equivalent: systems still incur evaluation, integration, coordination, migration, and consequence costs. The optimistic position is most plausible for bounded components with strong tests and reversible deployment.

## Open questions

- Which classes of software actually exhibit near-zero total change cost?
- Does AI reduce old debt faster than it creates new dependencies?
- What evidence can validate architecture at generated-code throughput?

## Relationships

- Informed by [[agentic-development-folded-requirements-into-iteration|Agentic development folded requirements into iteration]].
- Framed by [[architecture-is-the-scaling-constraint|Architecture is the scaling constraint]].
- Raises [[what-replaces-human-review-when-software-exceeds-human-attention|What replaces human review when software exceeds human attention?]].
