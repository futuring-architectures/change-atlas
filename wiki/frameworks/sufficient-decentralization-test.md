---
id: frm-f3a657b6fca5
type: framework
title: Sufficient decentralization test
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - decentralization
  - social-networks
  - censorship-resistance
relationships:
  - type: operationalizes
    target: "[[contextual-decentralization]]"
  - type: refined_by
    target: "[[what-kind-of-decentralization-creates-agency]]"
description: "A minimum social-network test: two users must remain able to find and communicate with each other despite opposition from the rest of the network."
evidence:
  - "[[sufficient-decentralization-for-social-networks-evi-7d067bde8a5b#Claim 1]]"
  - "[[sufficient-decentralization-for-social-networks-evi-7d067bde8a5b#Claim 2]]"
---

# Sufficient decentralization test

## Purpose

Use this Framework to replace an undefined demand for “more decentralization” with a falsifiable minimum capability for social communication: can two willing users still find and communicate with one another when other network participants or operators try to prevent it?

## Structure

### Adversarial communication threshold

Choose two willing users and an adversary representing the rest of the network. The system passes only if the users can continue to discover one another and exchange messages.

### Multi-client requirement

No single client can be the exclusive path to the audience. Independent developers must be able to build alternative clients on the network.

### Three decentralized capabilities

1. Claim a unique name.
2. Publish messages under that name.
3. Read messages published by any valid name.

These components reproduce Varun Srinivasan’s proposed minimum rather than an Atlas-authored expansion.

## How to apply it

1. Define the two users, the communication they intend, and the relevant adversary.
2. Test whether identity remains discoverable without a privileged directory.
3. Test whether either user can publish through an alternative client or service.
4. Test whether the other user can retrieve the message without permission from a single gatekeeper.
5. Record dependencies—hosting, naming, discovery, app stores, networks, and law—that can still break communication.
6. Treat a pass as a minimum threshold, then evaluate privacy, moderation, abuse, governance, usability, and contextual agency separately.

## Worked example

If a primary social client removes a speaker, the test asks whether the speaker can retain a valid network identity, publish through another client, and remain readable to a willing recipient. If identity or retrieval depends on the removed client’s private directory, the system fails the proposed threshold.

This is an illustrative test case, not an observed event in the Networks Evidence.

## Applicability and limitations

- The test is intentionally narrow. It does not prove equitable governance, privacy, safety, discoverability, economic viability, or broad public benefit.
- Absolute resistance to “the rest of the network” may conflict with legitimate abuse prevention, legal obligations, or collective self-governance.
- Technical reachability may be meaningless if alternative clients are unusable, unaffordable, or dependent on centralized infrastructure.
- Contextual decentralization may require collective decision rights beyond bilateral communication.

## Evidence

- [[sufficient-decentralization-for-social-networks-evi-7d067bde8a5b#Claim 1|Sufficient Decentralization for Social Networks — claim 1]] defines the adversarial communication threshold.
- [[sufficient-decentralization-for-social-networks-evi-7d067bde8a5b#Claim 2|Sufficient Decentralization for Social Networks — claim 2]] supplies the multi-client and three-capability structure.

## Relationships

- The test [[contextual-decentralization|operationalizes one minimum technical dimension of contextual decentralization]].
- [[what-kind-of-decentralization-creates-agency|The decentralization Debate]] refines the test by showing why reachability is not the whole of agency.
