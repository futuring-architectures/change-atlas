---
id: qst-f353545ebbb8
type: question
title: How should products manage model drift?
status: open
created_at: 2026-07-14
updated_at: 2026-10-16
tags:
  - model-drift
  - ai-operations
  - product-lifecycle
relationships:
  - type: raised_by
    target: "[[activity-alignment-gap]]"
  - type: raised_by
    target: "[[ai-native-services-adaptation-tests]]"
description: "How should AI products be designed, budgeted, and governed when provider models, behavior, price, and performance can change beneath a stable product interface?"
origin: ingestion
---

# How should products manage model drift?

## Why it matters

Traditional project governance often treats software as a durable artifact after release. AI products may depend on model versions and provider behavior that change independently of the product team. A release can improve a particular workload, degrade it, alter cost, or invalidate prompts and evaluations without a conventional code change.

## What is currently known

- One enterprise observation argues that companies continue to budget AI as finite plan–build–ship projects: [[if-ai-is-so-great-why-isnt-it-working-evi-9451a32b064d#Claim 1|If AI is so great, why isn’t it working? — claim 1]].
- The same source identifies model improvement and silent degradation as continuing operational change: [[if-ai-is-so-great-why-isnt-it-working-evi-9451a32b064d#Claim 2|claim 2]].
- The MenuGen case reports outdated API and model knowledge creating integration failures: [[vibe-coding-menugen-evi-0ce549d72b42#Claim 2|Vibe coding MenuGen — claim 2]].
- Enterprise optimization may shift toward intelligence per dollar as deployment cost grows: [[the-ai-economy-the-next-chapter-evi-855e88c44057#Claim 1|The AI Economy — claim 1]] and [[the-ai-economy-the-next-chapter-evi-855e88c44057#Claim 2|claim 2]].
- [[when-correct-systems-produce-the-wrong-outcomes-evi-7be149645e41#Claim 2|When Correct Systems Produce the Wrong Outcomes — claim 2]] broadens drift from model behavior to continued alignment between activity and purpose.
- [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 4|When the Models Get Better — claim 4]] proposes recurring strategic pivots after capability step changes; [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 5|claim 5]] argues that UX and workflow assumptions can be more fragile than architecture; and [[when-the-models-get-better-your-tam-should-go-up-evi-29342fde9096#Claim 6|claim 6]] reports four months of diff work becoming obsolete after GPT-4o.
- Sloan proposes avoiding a runtime model dependency where a finished conventional tool will do: use the agent to build, then run the tool without it. This addresses prospective AI API outages, price changes, and response drift rather than continually adapting an AI-dependent feature: [[ask-for-what-you-want-is-a-key-skill-for-the-21st-century-evi-1ec76f5e388c#Claim 4|construction without permanent runtime AI]] and [[ask-for-what-you-want-is-a-key-skill-for-the-21st-century-evi-1ec76f5e388c#Claim 17|dependency risks]]. His Gmail client illustrates why model independence is narrower than independence from external services: [[ask-for-what-you-want-is-a-key-skill-for-the-21st-century-evi-1ec76f5e388c#Claim 6|a tailored email client]].

## Missing or discriminating evidence

- Longitudinal records of behavior change across model upgrades, distillation, routing, and provider policy changes.
- Effective regression suites for probabilistic workflows and open-ended outputs.
- Contractual or technical controls for version pinning, rollback, portability, and disclosure.
- Budget models that include continuous evaluation, prompt migration, human retraining, and switching costs.
- Comparative records that distinguish productive recurring adaptation from pivot churn, team exhaustion, and destroyed customer continuity.
- Which capabilities can become conventional standalone tools, and which genuinely require inference during use.
- Maintenance and recovery outcomes for generated tools when the original building agent is no longer available.

## Suggested next sources or actions

- Collect product postmortems triggered by upstream model change.
- Compare managed APIs, open-weight models, and multi-model routing for operational control.
- Separate ordinary data drift from supplier-driven model drift and changing product requirements.
- Compare eliminating runtime inference with retaining it under version, evaluation, and fallback controls.

## Resolution

_Open. The current Evidence establishes the lifecycle problem and one scoped recurring-pivot heuristic, but not durable versioning, regression, rollback, migration, or switching controls._

## Relationships

- Raised by the [[activity-alignment-gap|Activity-alignment gap]], which makes continued purpose testing part of product operations.
- Raised by the [[ai-native-services-adaptation-tests|AI-native services adaptation tests]], whose recurring-pivot and UX-migration tests leave technical and governance controls unresolved.
