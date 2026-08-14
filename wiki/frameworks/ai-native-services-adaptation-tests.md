---
id: frm-599eb38f844d
type: framework
title: AI-native services adaptation tests
status: candidate
created_at: 2026-08-14
updated_at: 2026-08-14
tags: ["ai-native-services", "business-models", "product-strategy", "adaptation"]
relationships:
  - type: refines
    target: "[[capability-to-architecture-loop]]"
  - type: operationalizes
    target: "[[abundance-relocates-bottlenecks]]"
  - type: raises_question
    target: "[[how-should-products-manage-model-drift]]"
  - type: supported_by
    target: "[[decagon-automated-two-thirds-of-deployment-work-after-productizing-field-learning]]"
description: "Eleven tests for adapting an early-stage enterprise B2B AI-native services business as model capability, product assumptions, demand, field learning, and human work change."
evidence:
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 2]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 3]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 4]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 5]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 7]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 8]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 9]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 10]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 11]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 12]]"
  - "[[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 13]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 3]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 4]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 5]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 6]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 8]]"
  - "[[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 10]]"
---

# AI-native services adaptation tests

## Purpose

Use these tests when an early-stage company sells AI-native services into enterprises and model capability is changing faster than ordinary product and go-to-market assumptions. The Framework asks whether each capability gain expands the business, can be absorbed without destructive rebuilding, reaches customer adoption, and preserves a defensible role for human judgment.

## Structure

### 1. Model-improvement TAM test

Ask whether a better base model expands the set of economically viable customer problems. If it merely removes the scaffolding the business sells, the business may be renting a temporary capability gap rather than building around expanding demand.

### 2. Recurring-pivot test

For each material capability change, state what should change in service mix, product boundary, workflow, or customer selection. Treat revision as scheduled operating work while also defining evidence that prevents reflexive pivoting after noise.

### 3. UX re-engineerability test

Identify where the interface and workflow encode current model limitations: interaction grain, review burden, handoffs, prompts, diffs, exceptions, and assurance. Budget to replace those assumptions without rebuilding the entire system.

### 4. Paid-real-work test

Search for reusable product in work for which a real customer pays and delivery produces margin. Separate recurring capability from bespoke revenue, and record what compounds across engagements.

### 5. Field-learning conversion test

When neither vendor nor customer can specify a new workflow in advance, use field deployment to observe failures and discover the user journey. For every engagement, record which unknown became a reusable requirement, primitive, interface, or assurance mechanism. Set an exit criterion: if successive deployments do not require less bespoke work, determine whether the variation is irreducible, the product boundary is undecided, or a services business is being mislabeled as product discovery. Keep discovery distinct from implementation against a known specification.

### 6. Customer-adoption test

Distinguish market fit from fit inside the customer. A signed contract is not adoption; test whether workflow change, incentives, training, integration, governance, and change-management support produce repeated use and business outcomes.

### 7. Cognitive-load segment test

Determine whether the user gains output with lower cognitive load or purchases productivity by supplying more attention, verification, taste, and repair. Treat the two patterns as different product segments with different TAM, talent, reliability, and UX requirements.

### 8. Humanly-unattainable impact test

Name the workflow speed, quality, or scale that the service makes possible beyond an unaided human process. Do not confuse generated volume with business impact, and identify the people who bear the new risk or review load.

### 9. Current-quarter urgency test

Find the decision-maker for whom the outcome matters now. Then distinguish genuine urgency from sales pressure and recognize domains whose risk, regulation, or long planning horizon make speed an inappropriate value proposition.

### 10. Revenue-and-margin search test

Use revenue and then margin as near-term search feedback inside the model-improvement TAM constraint. Extract compounding assets and revise the ideal customer profile, while preserving explicit limits for safety, concentration, mission, and long-horizon investment.

### 11. Talent cap-and-moat test

Specify which human taste, judgment, domain knowledge, relationship, and execution discipline remain necessary. Test whether that dependence creates defensibility, merely limits scale, or is likely to be codified or automated away.

## How to apply it

1. Select one service line, model dependency, and customer segment.
2. Record the current model capability, workflow, UX assumptions, hours, cost, price, margin, adoption, and human review load.
3. Run all eleven tests after a material model release or at a fixed strategic cadence.
4. Mark each result as expansion, obsolescence, migration, unresolved, or outside scope.
5. Choose one bounded pivot and one element to preserve for continuity.
6. Re-measure customer outcomes, margin, cognitive load, and reusable capability before scaling the change.

## Worked example

The source reports a Salesforce Apex unit-test harness whose team spent four months improving diffs because poor diffs transferred review burden to users. GPT-4o then reduced that technical problem. The model-improvement and UX tests would ask whether the release expands the service into newly viable testing work, which interaction assumptions should disappear, what prior work remains reusable, and whether review attention moves to a different bottleneck rather than vanishing.

For a new accounting agent, the field-learning conversion test would not ask customers to specify an unprecedented journey abstractly. It would place product-capable staff near the work, distinguish regulatory and customer-specific variation from product gaps, encode repeated learning, and test whether each deployment reduces the next one's bespoke burden.

## Applicability and limitations

- The Framework is derived from one founder's practitioner account and self-reported business results.
- Its stated scope is early-stage enterprise B2B AI-native services; it should not be presumed to transfer to consumer products, SMBs, mature firms, public services, or frontier labs.
- Revenue and margin are useful survival signals but incomplete measures of durable value, safety, customer concentration, labor quality, or public impact.
- Frequent pivots can destroy accumulated knowledge, trust, team capacity, and strategic coherence.
- Cognitive load can be productive learning, expert control, avoidable repair, or risk transfer; the Framework does not treat all attention as equivalent.
- Human dependence is not automatically a moat, and model improvement can remove both burdens and differentiators.
- Field presence can expose tacit work while also privileging the customers able to host intensive deployments; learning must be checked for representativeness, consent, and transfer rather than assumed to become product automatically.

## Evidence

- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 2|When the Models Get Better — claim 2]] supplies the capability-gap test; [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 3|claim 3]] proposes model-driven market expansion.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 4|Claim 4]] makes pivoting recurring work, while [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 5|claim 5]] locates rebuild risk in UX and workflow assumptions.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 7|Claim 7]] ties product discovery to paid, profitable delivery; [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 8|claim 8]] separates market fit from customer adoption.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 9|Claim 9]] supplies cognitive-load segmentation; [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 10|claim 10]] keeps durable-output judgment and discipline with the human.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 11|Claim 11]] supplies the impact-and-urgency tests, and [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 12|claim 12]] supplies revenue-and-margin search.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 13|Claim 13]] frames human talent as both capacity limit and proposed moat.
- [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 3|To FDE, or not to FDE? — claim 3]] supplies unknown-workflow discovery; [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 4|claim 4]] supplies the forward-deployment exit; [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 5|claim 5]] identifies non-compounding bespoke work; and [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 6|claim 6]] distinguishes discovery from implementation.
- [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 8|Claim 8]] supplies Decagon's reported reduction in customer-specific engineering and deployment automation; [[to-fde-or-not-to-fde-evi-efcf1dd5486b#Claim 10|claim 10]] provides the reusable-product test.

## Relationships

- Refines the [[capability-to-architecture-loop|Capability-to-architecture loop]] by adding market expansion, UX migration, customer adoption, business fitness, and talent tests for a narrowly scoped service category.
- Operationalizes [[abundance-relocates-bottlenecks|Abundance relocates bottlenecks]] by tracing cheaper model capability into wider viable demand, changing UX, customer adoption, cognitive load, and human judgment.
- Raises [[how-should-products-manage-model-drift|the question of how products should manage model drift]] because re-engineerability and recurring pivots do not supply versioning, regression, rollback, or switching controls.
- Supported by [[decagon-automated-two-thirds-of-deployment-work-after-productizing-field-learning|Decagon automated two-thirds of deployment work after productizing field learning]].
