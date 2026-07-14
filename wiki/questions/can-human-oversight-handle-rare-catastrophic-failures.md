---
id: qst-639b5e04ed13
type: question
title: Can human oversight handle rare catastrophic failures?
status: open
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - ai-governance
  - oversight
  - reliability
relationships:
  - type: raised_by
    target: "[[agent-workflow-displaces-review-and-planning]]"
  - type: raised_by
    target: "[[the-human-in-the-loop-paradox]]"
description: "What oversight design remains effective when automated systems are usually correct, difficult to characterize, and occasionally fail severely?"
origin: another_page
---

# Can human oversight handle rare catastrophic failures?

## Why it matters

Governance often assigns a human to monitor or approve automated output. That safeguard may become ceremonial if long periods of correct behavior erode attention, if capabilities cannot be enumerated, or if the workflow removes review entirely.

## What is currently known

- One source interprets sustained vigilance over almost-always-correct systems with rare catastrophic failures as unreliable: [[undetectable-undefendable-back-doors-for-machine-learning-evi-21ae271cc148#Claim 1|the limits of sustained human vigilance]].
- The same source argues that adversarial incentives make machine-learning failures especially consequential: [[undetectable-undefendable-back-doors-for-machine-learning-evi-21ae271cc148#Claim 2|adversarial incentives and model failure]].
- Advanced AI capability is described as difficult to enumerate and therefore difficult to govern: [[how-do-you-govern-something-that-s-part-software-and-part-people-evi-da73ef066f1e#Claim 1|unknown capabilities as a governance problem]] and [[how-do-you-govern-something-that-s-part-software-and-part-people-evi-da73ef066f1e#Claim 2|the absence of an adequate theory of AI]].
- [[agent-workflow-displaces-review-and-planning|An agent workflow displaces human review and planning]] reports a workflow in which human code review is absent rather than merely weakened.
- LLM confidence is described as an unreliable guide to truth, while inconsistent errors make complex multi-step reasoning difficult to trust: [[ai-mistakes-are-very-different-from-human-mistakes-evi-6ce1d0622be3#Claim 1|confidence without calibration]] and [[ai-mistakes-are-very-different-from-human-mistakes-evi-6ce1d0622be3#Claim 2|inconsistent multi-step failure]].
- Demonstrated knowledge of business factors is therefore insufficient evidence of dependable performance in consequential use: [[ai-mistakes-are-very-different-from-human-mistakes-evi-6ce1d0622be3#Claim 3|the gap between apparent understanding and reliability]].
- Automation can increase dependence and, over time, risk eroding the human skills, judgment, and adaptability needed for recovery: [[the-hidden-cost-of-ai-trading-long-term-resilience-for-short-term-efficiency-evi-ce49c35011a3#Claim 1|efficiency coupled to dependence]], [[the-hidden-cost-of-ai-trading-long-term-resilience-for-short-term-efficiency-evi-ce49c35011a3#Claim 2|dependence eroding resilience]], and [[the-hidden-cost-of-ai-trading-long-term-resilience-for-short-term-efficiency-evi-ce49c35011a3#Claim 3|capability loss through offloading]].
- [[the-human-in-the-loop-paradox|The human-in-the-loop paradox]] adds that oversight can reduce control, responsibility, and moral agency when automation is safe only if a fallible person monitors it perfectly: [[ai-s-human-in-the-loop-isn-t-evi-734825a3f56e#Claim 1|diminished agency in oversight]] and [[ai-s-human-in-the-loop-isn-t-evi-734825a3f56e#Claim 2|the perfect-overseer contradiction]].

These sources identify the problem; they do not compare oversight mechanisms or establish failure rates.

## Missing or discriminating evidence

- Comparative performance of human-in-the-loop, human-on-the-loop, automated evaluation, and institutional audit designs.
- Failure frequency and severity under normal and adversarial conditions.
- Evidence about attention decay, escalation thresholds, and whether humans retain meaningful authority.
- Cases where hybrid review outperforms either full automation or continuous manual review.
- Calibration evidence that separates fluent confidence from task reliability.
- Designs that preserve human practice, diagnostic skill, override authority, and recovery capacity during long periods of automation.
- Evidence distinguishing dependence that creates unacceptable brittleness from ordinary reliance on reliable infrastructure.
- Evidence distinguishing meaningful authority over goals and constraints from ceremonial approval of individual outputs.

## Suggested next sources or actions

- Look for human-factors research on vigilance and automation bias.
- Collect documented AI incidents with a reconstructable oversight path.
- Separate oversight of individual outputs from governance of system deployment, incentives, and access.
- Test capability-retention mechanisms such as deliberate manual practice, fallback drills, and graduated automation.

## Resolution

_Open. The Rules pilot supports the concern but not a preferred oversight architecture._

## Relationships

- Raised by the candidate Signal [[agent-workflow-displaces-review-and-planning|An agent workflow displaces human review and planning]].
- Also raised by [[the-human-in-the-loop-paradox|the human-in-the-loop paradox]].
