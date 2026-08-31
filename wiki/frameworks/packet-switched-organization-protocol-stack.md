---
id: frm-49e1edd24c41
type: framework
title: Packet-switched organization protocol stack
status: candidate
created_at: 2026-08-31
updated_at: 2026-08-31
tags: ["organization-design", "networks", "coordination", "ai-agents"]
relationships:
  - type: supports
    target: "[[does-ai-flatten-hierarchy-or-intensify-management]]"
  - type: raises_question
    target: "[[how-can-firms-distribute-control-without-losing-coordination]]"
description: "A speculative protocol stack for routing work through capabilities, reliability classes, feedback loops, and bounded trust rather than fixed managerial paths."
evidence:
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 1]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 2]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 6]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 7]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 8]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 9]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 10]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 11]]"
  - "[[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 12]]"
---

# Packet-switched organization protocol stack

## Purpose

Use this Framework to test whether a proposed “networked” or “flat” organization has the operating protocols needed to distribute work without making coordination and accountability disappear. It translates Sam Schillace's packet-switching analogy into inspectable design questions. It is a candidate architecture, not evidence that network organizations outperform hierarchies.

## Architectural shift

A circuit-like organization reserves durable paths through roles and reporting lines. A packet-like organization describes work, routes it toward capabilities, and relies on shared protocols for legibility, delivery, recovery, and authorization. The design objective is not hierarchy removal. It is to separate the functions currently bundled inside hierarchy and decide which should remain human, become protocol, or be assisted by AI.

## The eight protocol functions

### 1. Work packet

Define the smallest useful unit that can travel: intended outcome, context, constraints, provenance, sensitivity, dependencies, owner, deadline, and acceptance evidence. If essential meaning cannot travel with the packet, the work is not ready for decentralized routing.

### 2. Reliability class

Choose a guarantee proportionate to consequence. Some work needs ordered delivery, acknowledgment, review, and retry; other work benefits from timely best effort and cheap abandonment. Do not impose maximum coordination overhead on every task or use a low-assurance path for irreversible decisions.

### 3. Capability address

Describe the capability required independently of the current org chart. Candidate signals may include demonstrated work, availability, interests, permissions, and development goals. Make the registry contestable and correctable so historical opportunity does not harden into a permanent capability score.

### 4. Routing

Match work to a person, team, agent, or mixed system able and authorized to act. Expose the basis of the match, workload effects, conflicts, and fallback path. Routing removes neither responsibility nor the need to resolve competing priorities.

### 5. Translation and handshake

Before work flows across a boundary, surface assumptions about format, vocabulary, interfaces, constraints, decision rights, and success. Confirm that sender and receiver share the same interpretation rather than using generated documentation as proof of agreement.

### 6. Acknowledgment and error correction

Specify what counts as receipt, progress, blockage, failure, and completion. Detection should trigger proportionate retry, clarification, escalation, rollback, or abandonment. Monitor outcomes and downstream repair, not only message movement or task closure.

### 7. Trust and accountability domain

Define where work may route freely and where additional authorization is required. Permission boundaries, accountable owners, audit evidence, shutdown authority, recourse, and affected-party voice must remain legible even when no manager sits in the path.

### 8. Peer exchange

For coordination across autonomous teams or organizations, specify how peers advertise capabilities, negotiate terms, exchange routing information, handle disputes, and exit. No party should need total control, but every party needs enforceable boundaries and a way to refuse.

## How to apply it

1. Select one recurring cross-boundary workflow rather than redesigning the whole organization.
2. Map the managerial functions currently carrying each of the eight protocols.
3. Classify the workflow's consequences, reversibility, latency needs, and required evidence.
4. Design the work packet and handshake before automating routing.
5. Establish a limited capability registry with consent, correction, and expiry.
6. Run parallel or reversible trials and measure routing time, coordination effort, failure detection, recovery, outcome quality, participant agency, and developmental effects.
7. Expand only when trust domains, escalation, and recourse work under ambiguity and failure.
8. Retain or rebuild the interpretive, developmental, and meaning-making functions that protocol automation does not supply.

## Failure tests

- Work moves faster but objectives and rule-setting become less contestable.
- Capability matching reproduces prior opportunity and routes growth work to the already visible.
- Continuous legibility becomes continuous surveillance.
- Automated status signals reward local metrics while hiding system outcomes.
- “Best effort” becomes an excuse for avoidable harm or unacknowledged labor.
- Trust boundaries exist technically but affected people lack recourse.
- The organization adopts network aesthetics before delivery, recovery, and accountability protocols work.

## Applicability and limitations

- Networking is an analogy, not an organizational law. People interpret, learn, negotiate, resist, and bear consequences; packets do not.
- Protocols can distribute execution while concentrating ownership of the routing layer, objectives, data, and infrastructure.
- Formal hierarchy can supply meaning, development, legitimate authority, and care in addition to routing information.
- The source reports early experimentation but no comparative organizational outcome. The proposed stack should be evaluated as a set of testable design hypotheses.

## Evidence

- [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 1|The Network Always Beats the Castle — claim 1]] supplies the circuit-to-packet analogy; [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 2|claim 2]] maps fixed paths onto managerial hierarchy.
- [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 6|The Network Always Beats the Castle — claim 6]] supplies capability routing; [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 7|claim 7]] supplies cross-boundary translation.
- [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 8|The Network Always Beats the Castle — claim 8]] supplies monitoring and recovery; [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 9|claim 9]] supplies protocol negotiation.
- [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 10|The Network Always Beats the Castle — claim 10]] supplies the capability address; [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 11|claim 11]] supplies differentiated reliability, trust domains, and peer exchange.
- [[the-network-always-beats-the-castle-evi-1a4b91886b9a#Claim 12|The Network Always Beats the Castle — claim 12]] makes protocol maturity a prerequisite and warns against decentralization as an aesthetic.

## Relationships

- Supports [[does-ai-flatten-hierarchy-or-intensify-management|Does AI flatten hierarchy or intensify management?]] by separating routine routing from the control and meaning functions that may persist.
- Raises [[how-can-firms-distribute-control-without-losing-coordination|How can firms distribute control without losing coordination?]] by turning distributed coordination into explicit protocol and evidence questions.
