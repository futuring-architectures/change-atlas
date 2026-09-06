---
id: frm-55ebccacd231
type: framework
title: Automation posture matrix
status: candidate
created_at: 2026-07-14
updated_at: 2026-09-06
tags:
  - automation
  - augmentation
  - human-agency
relationships:
  - type: operationalizes
    target: "[[the-human-in-the-loop-paradox]]"
  - type: raises_question
    target: "[[which-ai-interfaces-preserve-human-agency]]"
  - type: qualified_by
    target: "[[who-captures-the-gains-from-automation]]"
  - type: qualified_by
    target: "[[ai-automation-remains-constrained-by-deployment-economics]]"
  - type: qualified_by
    target: "[[ai-workslop-shifts-cognitive-labor-to-recipients]]"
description: "A two-axis matrix for choosing between automation, verified delegation, interactive copilot support, and expert augmentation according to task predictability and consequence."
evidence:
  - "[[enough-ai-copilots-we-need-ai-huds-evi-3c09cc413bb5#Claim 2]]"
  - "[[ai-s-human-in-the-loop-isn-t-evi-734825a3f56e#Claim 2]]"
  - "[[building-agency-into-the-relationships-between-humans-and-ai-evi-43b087f1ebc2#Claim 2]]"
  - "[[revenge-of-the-chickenized-reverse-centaurs-evi-34fd83edde9a#Claim 2]]"
  - "[[ai-wont-steal-as-many-jobs-as-expected-evi-1db89aca324b#Claim 1]]"
  - "[[ai-generated-workslop-is-destroying-productivity-evi-58ee7347e6af#Claim 2]]"
  - "[[a-vision-for-product-teams-evi-cbb1d8ab9fed#Claim 2]]"
  - "[[applied-ai-doesnt-work-evi-f6f3996faaab#Claim 8]]"
---

# Automation posture matrix

## Purpose

Use this Framework before choosing a default “copilot” or autonomous-agent interface. It asks whether the work is predictable and whether mistakes are consequential. The answer determines whether the system should act, propose, expose information, or remain subordinate to human judgment. The Organization collection adds two gates after quadrant selection: whether deployment is economically viable and whether apparent savings survive across the whole workflow.

## Structure

The horizontal axis is **task predictability**: from stable inputs, rules, and success criteria to ambiguous, changing, context-dependent work. The vertical axis is **consequence and reversibility**: from low-cost, easily detected and reversible errors to high-impact, delayed, or difficult-to-reverse failures.

Before selecting a quadrant, choose the least complex implementation substrate that fits the step. Stable rules belong in deterministic software. Bounded judgments may fit an agent when representative outcome-labeled examples, measurement, and recovery exist. Human-gated work should present the decision-maker with relevant evidence and real authority, not merely place a person after opaque generation.

### Predictable + low consequence: automate

Let the system act with lightweight monitoring. Optimize for speed and low interaction cost. Keep undo and exception reporting available.

### Predictable + high consequence: verified delegation

Automate only inside explicit constraints. Use independent checks, logs, staged execution, fallback, sampling, and escalation. Do not depend on a continuously vigilant person as the sole safety mechanism.

### Ambiguous + low consequence: interactive copilot

Let the system generate options and drafts while the person supplies context, taste, and direction. Make uncertainty and revision cheap.

### Ambiguous + high consequence: expert augmentation

Prefer interfaces that extend perception, comparison, memory, and simulation without silently taking control. Preserve the expert’s ability to inspect assumptions, shape objectives, and stop or redirect action.

## How to apply it

1. Define the actual unit of work rather than labeling an entire occupation automatable.
2. Score predictability using input stability, success criteria, exception frequency, and model drift.
3. Score consequence using blast radius, detectability, delay, reversibility, and affected parties.
4. Select the posture for the current quadrant.
5. Test economic viability using integration, maintenance, exception, and retained-flexibility costs—not task capability alone.
6. Measure total workflow effort, including verification, context reconstruction, rework, and burden shifted to recipients.
7. Specify who can change goals, constraints, and escalation rules.
8. Reassess when model behavior, workflow, cost, or consequence changes.

## Worked example

Summarizing an internal meeting for the participants may fit interactive copilot support: ambiguity exists, but correction is easy. Automatically denying a benefit claim may appear predictable while carrying high consequence and hidden exceptions; it requires verified delegation at minimum and may remain human-led if affected people lack recourse.

## Applicability and limitations

- Predictability and consequence are continua, not objective binary categories.
- Organizational incentives can understate consequence or classify ambiguity away.
- High model confidence is not evidence that a task belongs in a predictable quadrant.
- The matrix selects an interaction posture; it does not supply domain-specific safety controls.
- Technical feasibility is not evidence that automation is economical at the workflow or firm level.
- A locally faster producer can make the total system slower by externalizing interpretation and repair.

## Evidence

- [[enough-ai-copilots-we-need-ai-huds-evi-3c09cc413bb5#Claim 2|Enough AI copilots! We need AI HUDs — claim 2]] distinguishes routine delegation from expert augmentation.
- [[ai-s-human-in-the-loop-isn-t-evi-734825a3f56e#Claim 2|AI's “human in the loop” isn't — claim 2]] rejects perfect-human oversight as a safety design.
- [[building-agency-into-the-relationships-between-humans-and-ai-evi-43b087f1ebc2#Claim 2|Building agency into human–AI relationships — claim 2]] makes user influence a design objective.
- [[revenge-of-the-chickenized-reverse-centaurs-evi-34fd83edde9a#Claim 2|Revenge of the Chickenized Reverse Centaurs — claim 2]] supplies the failure mode in which AI directs and the human becomes subordinate.
- [[ai-wont-steal-as-many-jobs-as-expected-evi-1db89aca324b#Claim 1|AI won’t steal as many jobs as expected — claim 1]] adds the economic-feasibility gate.
- [[ai-generated-workslop-is-destroying-productivity-evi-58ee7347e6af#Claim 2|AI-Generated “Workslop” — claim 2]] shows cognitive labor moving downstream rather than disappearing.
- [[a-vision-for-product-teams-evi-cbb1d8ab9fed#Claim 2|A Vision For Product Teams — claim 2]] distinguishes process-heavy work from contextual judgment while leaving their boundary open to reassessment.
- [[applied-ai-doesnt-work-evi-f6f3996faaab#Claim 8|Applied AI Doesn't Work — claim 8]] adds a deterministic-software, agentic-judgment, and human-gated substrate test based on examples, consequence, evaluability, and verification burden.

## Relationships

- The matrix operationalizes [[the-human-in-the-loop-paradox|the human-in-the-loop paradox]].
- Applying it raises [[which-ai-interfaces-preserve-human-agency|the question of which interface forms preserve meaningful agency]].
- [[who-captures-the-gains-from-automation|The automation-gains Debate]] qualifies the matrix: a sound interaction posture does not determine ownership, compensation, bargaining power, or distribution.
- [[ai-automation-remains-constrained-by-deployment-economics|Deployment economics]] qualifies technical posture selection.
- [[ai-workslop-shifts-cognitive-labor-to-recipients|The workslop burden shift]] qualifies local productivity claims with workflow-level consequences.
