---
id: con-a9cad3cc483c
type: concept
title: Agent experience
status: candidate
created_at: 2026-07-14
updated_at: 2026-08-24
tags: ["ai-agents", "interfaces", "software-design"]
relationships:
  - type: raises_question
    target: "[[which-ai-interfaces-preserve-human-agency]]"
  - type: supports
    target: "[[capability-to-architecture-loop]]"
description: "The usability of a tool, platform, or protocol from the perspective of an AI agent acting under human authority."
evidence:
  - "[[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 1]]"
  - "[[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 2]]"
  - "[[automating-software-engineering-evi-7ef15bf9b270#Claim 1]]"
  - "[[previously-unmanufacturable-evi-4d49249b45d7#Claim 3]]"
  - "[[previously-unmanufacturable-evi-4d49249b45d7#Claim 4]]"
  - "[[previously-unmanufacturable-evi-4d49249b45d7#Claim 5]]"
---

# Agent experience

## Definition

Agent experience is the degree to which an AI agent can discover, interpret, operate, and verify a tool or service. It includes machine-readable interfaces, predictable state, permissions, error feedback, observability, and the handoff through which a human can inspect or redirect action.

Agent-mediated products can invert familiar interface design: the person receives a simpler intent surface while the product exposes richer schema, documentation, permissions, and failure behavior to the agent. This is a redistribution of complexity rather than its removal.

## Provenance

Mathias Biilmann names “AX” as an analogue to developer and user experience. Andrej Karpathy's software-engineering account adds the missing human side: an agent-compatible environment must also make oversight, nudging, and debugging workable. Tomasz Tunguz describes the complementary product-design inversion: natural language simplifies the end-user surface while applications become more explicit and evaluable for agents.

## Aliases and related terms

- AX
- Agent usability
- Machine-operable interface
- Agent-compatible infrastructure

## Distinctions and contested meanings

- Optimizing for agent access is not equivalent to removing human control.
- Agent experience is wider than an API: it includes feedback, authorization, recovery, and evaluability.
- Human-facing simplicity can require greater agent-facing complexity; hiding that complexity from the person does not make its consequences disappear.
- A tool can be easy for an agent and unsafe for the person represented by that agent.
- Agent compatibility may concentrate power in dominant personal-agent layers even as it opens individual services.

## Evidence

- [[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 1|Introducing AX — claim 1]] forecasts penalties for tools agents cannot use.
- [[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 2|Introducing AX — claim 2]] forecasts adoption advantages for agent-compatible tools.
- [[automating-software-engineering-evi-7ef15bf9b270#Claim 1|Automating software engineering — claim 1]] adds human oversight and debugging to the interface problem.
- [[previously-unmanufacturable-evi-4d49249b45d7#Claim 3|Previously Unmanufacturable — claim 3]] forecasts natural language as an intent layer over application-specific grammars.
- [[previously-unmanufacturable-evi-4d49249b45d7#Claim 4|Previously Unmanufacturable — claim 4]] identifies the paired design inversion: a simple human surface depends on a richer, safer agent harness.
- [[previously-unmanufacturable-evi-4d49249b45d7#Claim 5|Previously Unmanufacturable — claim 5]] moves documentation and agent evaluation into application product design.

## Relationships

- Raises [[which-ai-interfaces-preserve-human-agency|Which AI interfaces preserve human agency?]].
- Informs the interface-and-assurance step of the [[capability-to-architecture-loop|Capability-to-architecture loop]].
