---
id: frm-2bdc515fc791
type: framework
title: AI claim ladder
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - ai-evaluation
  - evidence
  - competence
relationships:
  - type: operationalizes
    target: "[[capability-is-not-competence]]"
description: "A five-level test for preventing observed output from silently escalating into claims about capability, competence, understanding, or accountable agency."
evidence:
  - "[[the-fundamental-extrapolation-error-evi-b53afd4c787e#Claim 2]]"
  - "[[just-calm-down-about-gpt-4-already-evi-6299ed6efcc4#Claim 2]]"
  - "[[unpredictable-black-boxes-are-terrible-interfaces-evi-23a45a14f69a#Claim 1]]"
  - "[[what-are-ai-world-models-and-why-do-they-matter-evi-13d6eebc6516#Claim 1]]"
---

# AI claim ladder

## Purpose

Use the ladder when a benchmark, demo, or fluent output is being used to justify a broader statement about what an AI system can do. Each step requires new evidence. The Framework prevents a true claim at a lower level from becoming an unsupported claim at a higher one.

## Structure

### 1. Output performance

What artifact did the system produce under the observed prompt, model version, tools, and evaluation conditions? Record the result without inferring a general capability.

### 2. Bounded task capability

Can the system reproduce the performance across a defined task distribution? Specify inputs, acceptable outputs, error rates, cost, latency, and conditions of failure.

### 3. Transfer and reliability

Does the capability survive changed phrasing, new examples, adversarial inputs, longer horizons, and model updates? Identify calibration, monitoring, and recovery rather than relying on fluent confidence.

### 4. Workflow competence

Can the system perform the interdependent practice in context: gather missing information, resolve ambiguity, use tools, recognize limits, recover from error, and coordinate with people? This is where exam success must be tested against the real work.

### 5. Understanding and accountable agency

What additional claim is actually being made—an internal world model, reasoning, intent, moral agency, or responsibility? State the operational criterion and do not infer legal or moral accountability merely because the interface uses first-person language.

## How to apply it

1. Write the strongest sentence currently being claimed about the system.
2. Place it on the highest rung it requires.
3. List the direct Evidence available at each lower rung.
4. Identify the first rung where the evidence becomes analogy, expectation, or extrapolation.
5. Design a test for that missing transition.
6. Attribute responsibility to the people and institutions deploying the system unless a defensible governance rule says otherwise.

## Worked example

Passing a bar examination is output performance. Repeated passage across unseen variants establishes a bounded capability. Robust performance under adversarial questions and model updates addresses reliability. Completing legal work with client context, procedural obligations, exceptions, and recovery would test workflow competence. None of these results alone determines whether the model understands law or can bear professional responsibility.

## Applicability and limitations

- The levels are evidential thresholds, not a universal theory of intelligence.
- A system can be useful at a lower rung and unsafe at a higher-stakes workflow.
- External tools, memory, and organizational process may raise system-level competence without changing the base model.
- Some domains require different metrics, and “understanding” remains philosophically contested.

## Evidence

- [[the-fundamental-extrapolation-error-evi-b53afd4c787e#Claim 2|The Fundamental Extrapolation Error — claim 2]] motivates the distinction between exam fragments and professional work.
- [[just-calm-down-about-gpt-4-already-evi-6299ed6efcc4#Claim 2|Just Calm Down About GPT-4 Already — claim 2]] warns against promoting performance into competence.
- [[unpredictable-black-boxes-are-terrible-interfaces-evi-23a45a14f69a#Claim 1|Unpredictable Black Boxes are Terrible Interfaces — claim 1]] adds the need for a predictive user model.
- [[what-are-ai-world-models-and-why-do-they-matter-evi-13d6eebc6516#Claim 1|What are AI “world models”? — claim 1]] supplies one proposed set of higher-level capability requirements.

## Relationships

- The Framework operationalizes [[capability-is-not-competence|the distinction between capability and competence]].
