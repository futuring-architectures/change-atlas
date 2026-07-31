---
id: frm-b78c0277a4b1
type: framework
title: Capability-to-architecture loop
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-31
tags: ["organization-design", "ai-adoption", "capabilities"]
relationships:
  - type: operationalizes
    target: "[[capability-not-role-as-unit-of-organization-design]]"
  - type: operationalizes
    target: "[[should-ai-agents-be-designed-as-workers-or-capabilities]]"
  - type: supported_by
    target: "[[agent-experience]]"
  - type: refines
    target: "[[organizational-transformation-test]]"
  - type: supported_by
    target: "[[design-for-emergence]]"
  - type: operationalizes
    target: "[[architecture-is-the-scaling-constraint]]"
  - type: supported_by
    target: "[[ai-adoption-failure-exposed-work-system-tensions]]"
description: "A recurring six-step method for redesigning work around changing capabilities without freezing AI into inherited roles."
evidence:
  - "[[stop-managing-your-ai-workforce-start-allocating-ai-capabilities-evi-5c0ade01553f#Claim 1]]"
  - "[[stop-managing-your-ai-workforce-start-allocating-ai-capabilities-evi-5c0ade01553f#Claim 2]]"
  - "[[activity-theory-as-a-system-level-explanation-for-why-ai-adoption-is-hard-evi-dadce4b3f82c#Claim 1]]"
  - "[[activity-theory-as-a-system-level-explanation-for-why-ai-adoption-is-hard-evi-dadce4b3f82c#Claim 2]]"
  - "[[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 1]]"
  - "[[the-vibes-dont-scale-evi-e058bb26186a#Claim 2]]"
  - "[[the-future-worth-building-is-human-evi-d29670f349f2#Claim 2]]"
  - "[[the-future-worth-building-is-human-evi-d29670f349f2#Claim 4]]"
  - "[[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 3]]"
  - "[[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 5]]"
  - "[[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 6]]"
  - "[[0-50-or-200-evi-704a6910d89c#Claim 1]]"
  - "[[0-50-or-200-evi-704a6910d89c#Claim 4]]"
---

# Capability-to-architecture loop

## Purpose

Use this Framework when a new human or machine capability enters an organization. It prevents two common errors: inserting the capability into yesterday's job structure, and treating low adoption as a user deficit before examining the work system.

## Structure

### 1. Re-state purpose and constraints

Name the outcome, affected stakeholders, non-negotiable rights, and failure costs before asking what the technology can do. This prevents available capability from silently redefining organizational purpose.

### 2. Map changing capabilities

List what people, agents, deterministic software, partners, and customers can now do. Record reliability, cost, reversibility, ownership, and conditions of failure rather than treating a benchmark as a deployable capability.

### 3. Diagnose the activity system

Map goals, workflows, rules, incentives, tools, roles, and decision rights. Treat resistance, workarounds, and low adoption as possible evidence of contradiction. Do not assume the person or the technology is the sole problem.

### 4. Recompose work and boundaries

Redesign the workflow around the new capability. Decide which tasks combine, disappear, or move; where human judgment is distinctive; and which decisions require human authority. Prefer adaptable structures where users possess relevant local knowledge.

### 5. Design interfaces and assurance

Build both agent experience and human control: permissions, inspectable state, evaluation, error feedback, escalation, rollback, and accountability. Higher generation throughput increases the need for coherent constraints.

### 6. Sense, learn, and reallocate

Measure system outcomes, not only tool usage or individual speed. Watch which capabilities become bottlenecks, lose value, or become strategically sensitive. Repeat the loop as capability and context change.

## How to apply it

1. Select one consequential workflow, not an entire role or company.
2. Describe the current system and baseline outcomes.
3. Complete each step with workers and affected stakeholders, not only technology owners.
4. Run a bounded, reversible implementation with explicit stop conditions.
5. Compare local productivity with system throughput, quality, coordination load, autonomy, and distributional effects.
6. Reallocate capabilities or redesign the architecture before scaling.

## Worked example

A support agent can resolve routine tickets. A role-first approach calls it a digital support worker and measures tickets handled. The loop instead maps reliability and exception classes, redesigns the customer-support flow, preserves human authority for ambiguous or distressed customers, exposes reasons and escalation state, and measures resolution quality and customer harm. If exceptions overload humans, that is an architectural signal rather than proof that employees need more prompting training.

## Applicability and limitations

- The loop applies to organizational adoption, not model training.
- It does not presume that deploying the new capability is desirable.
- Capability maps can underrepresent tacit knowledge and political interests.
- A workflow pilot cannot reveal every network or long-term effect.
- Continuous redesign can exhaust people; cadence and stability are design constraints too.

## Evidence

- [[stop-managing-your-ai-workforce-start-allocating-ai-capabilities-evi-5c0ade01553f#Claim 1|Stop managing your AI workforce — claim 1]] identifies the role-first trap; [[stop-managing-your-ai-workforce-start-allocating-ai-capabilities-evi-5c0ade01553f#Claim 2|claim 2]] supplies the capability-allocation alternative.
- [[activity-theory-as-a-system-level-explanation-for-why-ai-adoption-is-hard-evi-dadce4b3f82c#Claim 1|Activity Theory as a system-level explanation — claim 1]] treats adoption failure as a system signal; [[activity-theory-as-a-system-level-explanation-for-why-ai-adoption-is-hard-evi-dadce4b3f82c#Claim 2|claim 2]] calls for redesign.
- [[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 1|Introducing AX — claim 1]] locates agent compatibility in the interface.
- [[the-vibes-dont-scale-evi-e058bb26186a#Claim 2|The Vibes Don’t Scale — claim 2]] makes coherence constraints more important as production accelerates.
- [[the-future-worth-building-is-human-evi-d29670f349f2#Claim 2|The Future Worth Building Is Human — claim 2]] adds continuous customization with practitioners; [[the-future-worth-building-is-human-evi-d29670f349f2#Claim 4|claim 4]] requires evaluation of joint organizational outcomes rather than machine-alone capability.
- [[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 3|The Operating Model Is the Real AI Harness — claim 3]] defines the operating system to be redesigned; [[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 5|claim 5]] makes organization design primary rather than downstream; and [[the-operating-model-is-the-real-ai-harness-evi-47b5a20b1162#Claim 6|claim 6]] joins harness and organizational architecture.
- [[0-50-or-200-evi-704a6910d89c#Claim 1|0%, 50%, or 200% — claim 1]] separates the capability premise from the organizational response; [[0-50-or-200-evi-704a6910d89c#Claim 4|claim 4]] supplies growth-oriented reinvestment as one purpose-and-allocation choice.

## Relationships

- Operationalizes [[capability-not-role-as-unit-of-organization-design|Capability, not role, as the unit of organization design]].
- Incorporates [[agent-experience|Agent experience]] into human-governed deployment.
- Complements the [[organizational-transformation-test|Organizational transformation test]], which evaluates whether the resulting change is structural.
- Informed by [[design-for-emergence|Design for emergence]] and applies [[architecture-is-the-scaling-constraint|Architecture is the scaling constraint]] to organization design.
