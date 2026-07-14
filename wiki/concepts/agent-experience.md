---
id: con-a9cad3cc483c
type: concept
title: Agent experience
status: candidate
created_at: 2026-07-14
updated_at: 2026-07-14
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
---

# Agent experience

## Definition

Agent experience is the degree to which an AI agent can discover, interpret, operate, and verify a tool or service. It includes machine-readable interfaces, predictable state, permissions, error feedback, observability, and the handoff through which a human can inspect or redirect action.

## Provenance

Mathias Biilmann names “AX” as an analogue to developer and user experience. Andrej Karpathy's software-engineering account adds the missing human side: an agent-compatible environment must also make oversight, nudging, and debugging workable.

## Aliases and related terms

- AX
- Agent usability
- Machine-operable interface
- Agent-compatible infrastructure

## Distinctions and contested meanings

- Optimizing for agent access is not equivalent to removing human control.
- Agent experience is wider than an API: it includes feedback, authorization, recovery, and evaluability.
- A tool can be easy for an agent and unsafe for the person represented by that agent.
- Agent compatibility may concentrate power in dominant personal-agent layers even as it opens individual services.

## Evidence

- [[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 1|Introducing AX — claim 1]] forecasts penalties for tools agents cannot use.
- [[introducing-ax-why-agent-experience-matters-evi-effc684d312e#Claim 2|Introducing AX — claim 2]] forecasts adoption advantages for agent-compatible tools.
- [[automating-software-engineering-evi-7ef15bf9b270#Claim 1|Automating software engineering — claim 1]] adds human oversight and debugging to the interface problem.

## Relationships

- Raises [[which-ai-interfaces-preserve-human-agency|Which AI interfaces preserve human agency?]].
- Informs the interface-and-assurance step of the [[capability-to-architecture-loop|Capability-to-architecture loop]].
