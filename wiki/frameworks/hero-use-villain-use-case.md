---
id: frm-147b274c0bfc
type: framework
title: Hero-use / villain-use case analysis
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - abuse
  - accountability
  - product-design
relationships: []
description: "A dual-use review that pairs a product's intended beneficial use with foreseeable abuse of the same core capabilities and a mitigation obligation."
evidence:
  - "[[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 1]]"
  - "[[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 2]]"
  - "[[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 3]]"
---

# Hero-use / villain-use case analysis

## Purpose

Use this framework to prevent product teams from evaluating a capability only through its intended, well-meaning user. It pairs the hero use case with foreseeable malicious use and turns residual abuse risk into an explicit mitigation problem.

## Structure

### Hero use case

Describe the paradigmatic beneficial use: who acts, what capability they use, and what value the product creates.

### Villain use case

Hold the core capability constant and change the actor's intent, target, or context. Ask how the same affordance enables abuse rather than inventing an unrelated threat.

### Residual-risk obligation

Assume abuse cannot be eliminated. Decide which harms the product facilitates, which mitigations are proportionate, and what evidence will show whether those mitigations work.

## How to apply it

1. Name the product's core capability rather than only its feature label.
2. Write the intended actor, action, target, and benefit as a hero-use case.
3. Vary intent, scale, target vulnerability, and coordination to generate villain-use cases using the same capability.
4. Rank foreseeable harms by severity, reach, reversibility, and likelihood.
5. Assign mitigations across product design, access, monitoring, user recourse, and incident response.
6. Record residual risks and the decision authority that accepts them.
7. Revisit both use cases as deployment scale and user behavior change.

Steps 1–7 are an Atlas operationalization. The source establishes the hero/villain distinction and mitigation duty but does not provide this exact procedure.

## Worked example

A natural-language generation system may help a hero user translate public-health guidance at low cost. The same scalable generation capability may help a villain user produce tailored deceptive messages. The framework asks which safeguards reduce abuse without assuming that beneficial use removes the product maker's responsibility.

This example is illustrative and is not an observed case in the current Governance Evidence.

## Applicability and limitations

- The framework is most useful for dual-use products whose core affordances transfer readily between beneficial and harmful intent.
- “Villain” can oversimplify harms caused by ordinary incentives, careless use, institutional practice, or emergent effects without malicious intent.
- Foreseeability expands with hindsight; teams need explicit evidence and review intervals to avoid unlimited responsibility.
- Mitigation can create its own access, privacy, speech, or concentration costs.

## Evidence

- [[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 1|Holding Big Tech Accountable — claim 1]] establishes the abuse assumption.
- [[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 2|Holding Big Tech Accountable — claim 2]] supplies the hero/villain pairing.
- [[what-it-really-means-to-hold-big-tech-accountable-evi-7b7e963d4cf1#Claim 3|Holding Big Tech Accountable — claim 3]] supplies the mitigation obligation.

## Relationships

- No typed relationship is asserted yet. Later synthesis should test whether this Framework operationalizes a broader responsible-design Concept supported beyond one source.
