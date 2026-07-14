---
id: con-4c0ce7571c35
type: concept
title: Activity-alignment gap
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags: ["ai-agents", "alignment", "monitoring"]
relationships:
  - type: exemplified_by
    target: "[[recommendation-algorithms-projected-cultural-pasts-forward]]"
  - type: operationalized_by
    target: "[[transition-integration-stack]]"
  - type: raises_question
    target: "[[how-should-products-manage-model-drift]]"
description: "The gap between a system continuing to operate successfully and continuing to advance the purpose it should serve."
evidence:
  - "[[when-correct-systems-produce-the-wrong-outcomes-evi-7be149645e41#Claim 1]]"
  - "[[when-correct-systems-produce-the-wrong-outcomes-evi-7be149645e41#Claim 2]]"
  - "[[yesterday-once-more-evi-05bf12374ad2#Claim 2]]"
---

# Activity-alignment gap

## Definition

The activity-alignment gap is the distance between a system remaining busy, available, and internally correct and the system continuing to produce the outcomes it ought to serve. Long-lived agents can cross the gap gradually without triggering ordinary uptime or error alarms.

## Provenance

An O'Reilly Radar account names the failure mode for long-lived agents. The recommendation-culture evidence supplies an adjacent example: a loop can update correctly while projecting an increasingly frozen cultural future.

## Aliases and related terms

- Outcome drift
- Purpose drift
- Correct-system failure
- Activity without alignment

## Distinctions and contested meanings

- Model drift concerns changing model behavior; activity-alignment also includes changing goals and context.
- Purpose is not always stable or singular and requires legitimate revision.
- Outcome monitoring can itself create narrow metrics and gaming.
- A system may fail ethically while meeting every technical service-level objective.

## Evidence

- [[when-correct-systems-produce-the-wrong-outcomes-evi-7be149645e41#Claim 1|When Correct Systems Produce the Wrong Outcomes — claim 1]] defines functioning without desired outcome.
- [[when-correct-systems-produce-the-wrong-outcomes-evi-7be149645e41#Claim 2|When Correct Systems Produce the Wrong Outcomes — claim 2]] makes continued purpose testing a governance requirement.
- [[yesterday-once-more-evi-05bf12374ad2#Claim 2|Yesterday Once More — claim 2]] supplies a cultural feedback-loop example.

## Relationships

- Exemplified by [[recommendation-algorithms-projected-cultural-pasts-forward|Recommendation algorithms projected cultural pasts forward]].
- Operationalized by the monitoring layer of the [[transition-integration-stack|Transition integration stack]].
- Raises [[how-should-products-manage-model-drift|How should products manage model drift?]].
