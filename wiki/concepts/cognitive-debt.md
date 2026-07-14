---
id: con-d5366f164810
type: concept
title: Cognitive debt
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags: ["software-engineering", "knowledge", "ai-coding"]
relationships:
  - type: operationalized_by
    target: "[[sustaining-capacity-loop]]"
  - type: raises_question
    target: "[[what-replaces-human-review-when-software-exceeds-human-attention]]"
description: "The accumulated gap between a system's operating complexity and the context people and tools can reliably recover to understand and change it."
evidence:
  - "[[cognitive-debt-is-nothing-new-ai-just-stopped-hiding-it-evi-d47db0c3b936#Claim 1]]"
  - "[[cognitive-debt-is-nothing-new-ai-just-stopped-hiding-it-evi-d47db0c3b936#Claim 2]]"
  - "[[design-systems-are-no-longer-optional-evi-f79608079d95#Claim 2]]"
---

# Cognitive debt

## Definition

Cognitive debt is the gap between a system's accumulated decisions and the context available to people and tools who must operate, verify, or change it. AI can expose and accelerate the debt by producing more change than people can internalize, while also helping preserve and retrieve context.

## Provenance

Péter Verhás argues that cognitive debt predates AI and should be managed by feeding context into systems that can carry it forward. Mandy Michael adds the organizational failure mode: an inaccurate shared reference can be propagated across a product at machine speed.

## Aliases and related terms

- Context debt
- Comprehension debt
- Knowledge debt
- System-understanding deficit

## Distinctions and contested meanings

- Cognitive debt differs from code defects; a functioning system can still be poorly understood.
- Requiring every person to understand every generated line is not the only remedy.
- Externalized context can reduce individual burden while increasing dependence on tools and owners.
- Documentation volume is not equivalent to recoverable understanding.

## Evidence

- [[cognitive-debt-is-nothing-new-ai-just-stopped-hiding-it-evi-d47db0c3b936#Claim 1|Cognitive Debt Is Nothing New — claim 1]] locates the debt before AI.
- [[cognitive-debt-is-nothing-new-ai-just-stopped-hiding-it-evi-d47db0c3b936#Claim 2|Cognitive Debt Is Nothing New — claim 2]] proposes context-preserving tools rather than complete line-level comprehension.
- [[design-systems-are-no-longer-optional-evi-f79608079d95#Claim 2|Design Systems Are No Longer Optional — claim 2]] supplies the machine-speed propagation risk.

## Relationships

- Operationalized by the context-and-maintenance steps of the [[sustaining-capacity-loop|Sustaining capacity loop]].
- Raises [[what-replaces-human-review-when-software-exceeds-human-attention|What replaces human review when software exceeds human attention?]].
