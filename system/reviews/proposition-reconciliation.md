---
review_id: proposition-reconciliation
generated_at: 2026-07-20
scope: mature-synthesis-propositions
status: implemented
---

# Proposition reconciliation review

## Decision boundary

This review reconciled the 21 propositions whose status was `strengthened` or `qualified` in `system/synthesis-backlog.json` after bootstrap. Its recommendation has now been implemented: 19 reader-facing Proposition pages were published, two misleadingly qualified records were returned to `open`, and the Atlas is prepared to assess propositions during individual-source ingestion.

## Executive recommendation

| Disposition | Strengthened | Qualified | Total |
|---|---:|---:|---:|
| Publish as a Wiki Proposition | 14 | 5 | 19 |
| Retain in the internal backlog | 0 | 2 | 2 |
| Merge now | 0 | 0 | 0 |
| Promote directly to a Trend | 0 | 0 | 0 |

The 19 recommended propositions are now distinct pages under `wiki/propositions/`. Their overlaps are preserved through links and navigation clusters rather than merges: the apparent overlaps generally concern different units of analysis, mechanisms, or outcomes.

`prp-e5fc4d5c24c3` and `prp-7650797f1cdc` remain internal and are now `open`. Both name useful research directions, but their present wording asserts a relationship that the corpus has not adequately isolated or observed. Their qualifying assessments remain intact as history; those assessments no longer masquerade as the maturity of the propositions themselves.

No proposition is ready for direct Trend promotion. At review time, the original 21 records cited 111 Evidence claims: 39 conceptual claims, 25 interpretations, 24 normative positions, 14 predictions, and only 9 observations. Several propositions have support across collections, but support for a mechanism or design rationale is not the same as repeated observation of a direction over time.

## Reconciliation findings

### 1. The propositions fill a real gap in the Wiki

The mature propositions are not redundant with the existing Wiki types. Concepts name mechanisms, Frameworks operationalize them, and Signals preserve bounded cases. The propositions make conditional, causal, comparative, or future-facing claims that those pages often imply but do not state as claims to be tested.

### 2. The original Evidence lists were not publication-ready

The original top-level `evidence` arrays mostly preserved the claims attached when each proposition was opened. Later assessments often described strengthening or qualifying material without adding stable Evidence anchors to that array. Publication therefore reconstructed cumulative exact claim anchors from the named collection assessments; assessment prose was preserved as history, not treated as a substitute for citations.

### 3. Overlap should become navigation, not premature merging

Four useful neighborhoods recur:

- **Governance and agency:** `prp-7c60b5f08327`, `prp-2bb29cadf400`, `prp-1e7cfdce9b4a`, `prp-6a50ba86b4e2`, and `prp-34559bf974bb`.
- **Human work and capability:** `prp-516df0a73843`, `prp-8a332364c8a2`, `prp-cd8e403699a7`, and `prp-661114a04536`.
- **Adaptation and organizational renewal:** `prp-eb6b438dce8a`, `prp-6b7b24b95b33`, `prp-2d0c19cae51e`, `prp-69e1497e1057`, `prp-be860f298fbf`, and `prp-47dacc22a69f`.
- **Attention, culture, and economic selection:** `prp-b77689287c42`, `prp-148e7962f080`, and `prp-de32f067c458`.

Within these neighborhoods, the propositions should link to one another while retaining their distinct scope. For example, loss of collegial interaction, removal of entry-level work, and individual capacity erosion are related but not interchangeable outcomes.

### 4. Debates and Questions are already natural companions

The strongest existing connections are to Debates and Questions about agency, expertise, collaboration, model drift, human review, and transition. Publication should add reciprocal, readable links. A Debate should expose competing interpretations of a Proposition; a Question should state what evidence could change its status.

### 5. The existing Trend remains distinct

Several propositions relate to [[wiki/trends/software-work-is-shifting-from-code-production-to-orchestration-and-assurance|Software work is shifting from code production to orchestration and assurance]]. They should not be absorbed into it mechanically. The Trend records a bounded directional pattern in software practice; the related propositions make broader claims about organizational roles, architecture, assurance, product operation, and human capability.

## Recommended public Propositions

### Governance, agency, and control

#### `prp-7c60b5f08327` — Distributed stewardship may counteract concentrated firm power

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 1 observation, 2 interpretations, 3 normative positions; source dates 2020–2024.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Governance, Ecosystems, Organization, and Communities independently add mechanisms involving stakeholder voice, de-bossification, trust, local agency, and maintainer boundaries. The claim is distinct from the Concepts and Frameworks that describe those mechanisms.
- **Connect to:** [[wiki/concepts/orbital-stakeholders|Orbital stakeholders]], [[wiki/concepts/power-as-an-organizing-design-value|Power as an organizing design value]], [[wiki/frameworks/ecosystem-boundary-audit|Ecosystem boundary audit]], [[wiki/debates/does-ai-flatten-hierarchy-or-intensify-management|Does AI flatten hierarchy or intensify management?]], [[wiki/questions/how-can-firms-distribute-control-without-losing-coordination|How can firms distribute control without losing coordination?]], and [[wiki/questions/what-rights-follow-from-ecosystem-contribution|What rights follow from ecosystem contribution?]].
- **Publication caveat:** State plainly that no comparative case yet demonstrates a transfer of formal decision power or a better outcome.

#### `prp-2bb29cadf400` — Inference-first interfaces may reduce friction while weakening visible user agency

- **Current status:** `qualified`
- **Evidence profile:** 3 claims; 1 interpretation, 1 normative position, 1 prediction; source dates 2024–2025.
- **Recommendation:** Publish as a qualified Proposition.
- **Why:** Paradigms, Culture, Gameplay, Architectures, and Sustaining repeatedly expose the same trade-off between machine inference and inspectable human control. The proposition gives a testable claim to a concern distributed across several interface Concepts.
- **Connect to:** [[wiki/concepts/agent-experience|Agent experience]], [[wiki/concepts/the-human-in-the-loop-paradox|The human-in-the-loop paradox]], [[wiki/frameworks/automation-posture-matrix|Automation posture matrix]], [[wiki/debates/does-cheap-software-distribute-agency-or-relocate-control|Does cheap software distribute agency or relocate control?]], and [[wiki/questions/which-ai-interfaces-preserve-human-agency|Which AI interfaces preserve human agency?]].
- **Publication caveat:** Preserve the qualification that comparative evidence across predictive, conversational, copilot, and direct-manipulation interfaces is absent.

#### `prp-1e7cfdce9b4a` — Natural-language creation may distribute capability faster than ownership, maintenance, and recourse

- **Current status:** `qualified`
- **Evidence profile:** 5 claims; 1 conceptual claim, 1 interpretation, 2 normative positions, 1 prediction; source dates 2023–2026.
- **Recommendation:** Publish as a qualified Proposition.
- **Why:** Gameplay, Architectures, Sustaining, and Transitions converge on the gap between creating an artifact and owning, maintaining, evaluating, or obtaining recourse for it. This is broader than user-programmability and more specific than generic agency loss.
- **Connect to:** [[wiki/concepts/user-programmable-agents|User-programmable agents]], [[wiki/concepts/signal-collapse-after-cheap-production|Signal collapse after cheap production]], [[wiki/frameworks/ai-agency-audit|AI agency audit]], [[wiki/debates/does-cheap-software-distribute-agency-or-relocate-control|Does cheap software distribute agency or relocate control?]], [[wiki/debates/does-cheap-implementation-improve-innovation-or-obscure-understanding|Does cheap implementation improve innovation or obscure understanding?]], and [[wiki/questions/how-should-products-manage-model-drift|How should products manage model drift?]].
- **Publication caveat:** Capability distribution is observed more directly than the ownership, maintenance, and recourse outcomes; do not imply that all four move together.

#### `prp-6a50ba86b4e2` — AI governance may shift from capability access to deployment conditions

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 1 observation, 2 conceptual claims, 1 interpretation, 2 normative positions; source dates 2024–2025.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Futuring, Architectures, Sustaining, and Transitions repeatedly relocate governance from model access alone into interfaces, workflows, evaluation, institutional context, and continuing outcome review.
- **Connect to:** [[wiki/concepts/capability-deployment-gap|Capability-deployment gap]], [[wiki/frameworks/transition-integration-stack|Transition integration stack]], [[wiki/debates/does-ai-progress-require-scaling-or-new-paradigms|Does AI progress require scaling or new paradigms?]], [[wiki/debates/is-technology-resistance-an-obstacle-or-design-input|Is technology resistance an obstacle or design input?]], and [[wiki/questions/how-should-products-manage-model-drift|How should products manage model drift?]].
- **Publication caveat:** Describe a shift in governance emphasis as a supported hypothesis, not as an observed regime-level transition.

#### `prp-34559bf974bb` — Agent-compatible infrastructure may improve machine performance while reducing human agency

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 2 conceptual claims, 3 normative positions, 1 prediction; source dates 2024–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Architectures, Sustaining, and Transitions converge on a distinct infrastructure trade-off: machine legibility and operability can improve while inspection, disagreement, provenance, recovery, and recourse weaken for people.
- **Connect to:** [[wiki/concepts/agent-experience|Agent experience]], [[wiki/concepts/database-reality-inversion|Database-reality inversion]], [[wiki/frameworks/capability-to-architecture-loop|Capability-to-architecture loop]], [[wiki/frameworks/transition-integration-stack|Transition integration stack]], [[wiki/debates/is-technology-resistance-an-obstacle-or-design-input|Is technology resistance an obstacle or design input?]], and [[wiki/questions/which-ai-interfaces-preserve-human-agency|Which AI interfaces preserve human agency?]].
- **Publication caveat:** No comparative deployed-interface outcome yet establishes the trade-off empirically.

### Human work, learning, and capability

#### `prp-516df0a73843` — Human roles may shift toward orchestration, evaluation, judgment, and exceptions

- **Current status:** `strengthened`
- **Evidence profile:** 9 claims; 4 conceptual claims, 1 interpretation, 1 normative position, 3 predictions; source dates 2024–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Five collections converge on a broad organizational-role hypothesis that extends beyond software engineering. It is related to, but wider than, the existing candidate software-work Trend.
- **Connect to:** [[wiki/trends/software-work-is-shifting-from-code-production-to-orchestration-and-assurance|Software work is shifting from code production to orchestration and assurance]], [[wiki/frameworks/ai-native-organizational-trust-stack|AI-native organizational trust stack]], [[wiki/frameworks/automation-posture-matrix|Automation posture matrix]], [[wiki/debates/does-ai-flatten-hierarchy-or-intensify-management|Does AI flatten hierarchy or intensify management?]], [[wiki/debates/does-cheap-intelligence-reduce-the-need-for-human-collaboration|Does cheap intelligence reduce the need for human collaboration?]], and [[wiki/questions/what-replaces-hierarchy-as-meaning-infrastructure|What replaces hierarchy as meaning infrastructure?]].
- **Publication caveat:** Most evidence forecasts or interprets role change; it does not establish representative adoption or employment outcomes.

#### `prp-8a332364c8a2` — Substituting AI for colleagues may erode apprenticeship, recognition, and shared meaning

- **Current status:** `strengthened`
- **Evidence profile:** 5 claims; 4 conceptual claims, 1 prediction; source dates 2023–2025.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Culture, Gameplay, Architectures, Sustaining, and Transitions distinguish individual task output from the relational functions of work. This proposition concerns collegial and collective consequences, not merely individual skill loss.
- **Connect to:** [[wiki/concepts/epistemic-fluency|Epistemic fluency]], [[wiki/frameworks/collaboration-architecture-choice|Collaboration architecture choice]], [[wiki/debates/does-cheap-intelligence-reduce-the-need-for-human-collaboration|Does cheap intelligence reduce the need for human collaboration?]], and [[wiki/questions/how-can-ai-mediated-work-preserve-apprenticeship-and-meaning|How can AI-mediated work preserve apprenticeship and meaning?]].
- **Publication caveat:** Present the outcomes as plausible mechanisms awaiting longitudinal workplace evidence.

#### `prp-cd8e403699a7` — Removing entry-level production may weaken the future supply of expert judgment

- **Current status:** `qualified`
- **Evidence profile:** 6 claims; 4 conceptual claims, 2 predictions; source dates 2024–2026.
- **Recommendation:** Publish as a qualified Proposition.
- **Why:** The proposition isolates the workforce-pipeline mechanism: today’s routine production can also be tomorrow’s expert formation. It overlaps with apprenticeship and capacity erosion but has a distinct unit of analysis and delayed labor-market outcome.
- **Connect to:** [[wiki/concepts/capacity-erosion-through-assistance|Capacity erosion through assistance]], [[wiki/concepts/task-boundary-work|Task-boundary work]], [[wiki/frameworks/ai-agency-audit|AI agency audit]], [[wiki/debates/does-ai-expand-expertise-or-hollow-it-out|Does AI expand expertise or hollow it out?]], and [[wiki/questions/how-can-ai-mediated-work-preserve-apprenticeship-and-meaning|How can AI-mediated work preserve apprenticeship and meaning?]].
- **Publication caveat:** Neither removal of entry-level work nor a later expert-supply effect is yet observed directly.

#### `prp-661114a04536` — AI assistance may hide delayed capacity loss behind short-term productivity

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 4 conceptual claims, 1 interpretation, 1 prediction; source dates 2025–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Sustaining and Transitions specify a distinct measurement problem: assistance can improve visible output while bypassing practice, challenge, verification, disagreement, and participation that sustain future capability.
- **Connect to:** [[wiki/concepts/capacity-erosion-through-assistance|Capacity erosion through assistance]], [[wiki/concepts/epistemic-fluency|Epistemic fluency]], [[wiki/frameworks/sustaining-capacity-loop|Sustaining capacity loop]], [[wiki/debates/does-ai-expand-expertise-or-hollow-it-out|Does AI expand expertise or hollow it out?]], and [[wiki/questions/how-can-ai-assistance-preserve-persistence-verification-and-participation|How can AI assistance preserve persistence, verification, and participation?]].
- **Publication caveat:** The delayed-loss claim needs longitudinal measurement and counter-cases where assistance preserves or improves capacity.

### Adaptation, architecture, and renewal

#### `prp-eb6b438dce8a` — AI-dependent products may require continuous revalidation

- **Current status:** `strengthened`
- **Evidence profile:** 5 claims; 2 conceptual claims, 2 interpretations, 1 observation; source dates 2025–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Paradigms, Organization, and Architectures connect upstream model churn with evaluation, monitoring, governance, learning loops, and red teaming. The proposition states the operational claim that the related Framework makes actionable.
- **Connect to:** [[wiki/frameworks/ai-native-organizational-trust-stack|AI-native organizational trust stack]], [[wiki/questions/how-should-products-manage-model-drift|How should products manage model drift?]], and [[wiki/questions/what-replaces-human-review-when-software-exceeds-human-attention|What replaces human review when software exceeds human attention?]].
- **Publication caveat:** A longitudinal product case demonstrating revalidation across upstream model changes is still absent.

#### `prp-6b7b24b95b33` — Legacy expertise may be infrastructure for long technological transitions

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 3 conceptual claims, 2 interpretations, 1 observation; source dates 2020–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Culture, Sustaining, and Transitions connect legacy-system dependence, tacit context, cumulative engineering, task-boundary work, and pace layers. The proposition makes explicit why apparently obsolete expertise can remain enabling infrastructure.
- **Connect to:** [[wiki/signals/legacy-mainframes-underwrite-digital-services|Legacy mainframes underwrite digital services]], [[wiki/concepts/task-boundary-work|Task-boundary work]], [[wiki/concepts/pace-layering|Pace layering]], [[wiki/frameworks/transition-integration-stack|Transition integration stack]], [[wiki/debates/does-progress-require-acceleration-or-productive-friction|Does progress require acceleration or productive friction?]], and [[wiki/questions/how-can-institutions-preserve-tacit-knowledge-through-transition|How can institutions preserve tacit knowledge through transition?]].
- **Publication caveat:** Avoid generalizing from dependency and mechanism to comparative transition success.

#### `prp-2d0c19cae51e` — Reversible probes and explicit revision may improve adaptation

- **Current status:** `strengthened`
- **Evidence profile:** 6 claims; 2 interpretations, 4 normative positions; source dates 2021–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Futuring, Architectures, Sustaining, and Transitions converge on reversible experimentation and revision as an adaptation mechanism. The Proposition preserves the claim to be tested; the existing Concept and Frameworks explain and operationalize it.
- **Connect to:** [[wiki/concepts/action-without-prediction|Action without prediction]], [[wiki/frameworks/adaptive-futuring-cycle|Adaptive futuring cycle]], [[wiki/frameworks/uncertainty-to-action-matrix|Uncertainty-to-action matrix]], [[wiki/frameworks/transition-integration-stack|Transition integration stack]], and [[wiki/debates/does-cheap-implementation-improve-innovation-or-obscure-understanding|Does cheap implementation improve innovation or obscure understanding?]].
- **Publication caveat:** All current direct claims are interpretations or prescriptions; no organizational comparison shows better adaptation outcomes.

#### `prp-69e1497e1057` — Capability-centered workflow and authority redesign may outperform role substitution

- **Current status:** `strengthened`
- **Evidence profile:** 5 claims; 1 conceptual claim, 1 interpretation, 3 normative positions; source dates 2025–2026.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Architectures, Sustaining, and Transitions repeatedly contrast work-system redesign with inserting agents into inherited roles. The performance hypothesis remains distinct from the Concept and Framework that prescribe capability-centered design.
- **Connect to:** [[wiki/concepts/capability-not-role-as-unit-of-organization-design|Capability, not role, as the unit of organization design]], [[wiki/concepts/capability-is-not-competence|Capability is not competence]], [[wiki/frameworks/capability-to-architecture-loop|Capability-to-architecture loop]], [[wiki/debates/should-ai-agents-be-designed-as-workers-or-capabilities|Should AI agents be designed as workers or capabilities?]], and [[wiki/signals/ai-adoption-failure-exposed-work-system-tensions|AI adoption failure exposed work-system tensions]].
- **Publication caveat:** No comparative performance evidence yet supports “outperform.”

#### `prp-be860f298fbf` — Faster generation may increase the relative value of architecture, assurance, and absorption

- **Current status:** `strengthened`
- **Evidence profile:** 7 claims; 4 conceptual claims, 2 interpretations, 1 normative position; source dates 2024–2026.
- **Recommendation:** Publish as a strengthened Proposition and link it closely to the existing candidate Trend.
- **Why:** Architectures, Sustaining, and Transitions converge on post-generation constraints while distinguishing them from code production itself. The proposition supplies a causal and scarcity interpretation; the Trend records bounded changes in software practice.
- **Connect to:** [[wiki/concepts/architecture-is-the-scaling-constraint|Architecture is the scaling constraint]], [[wiki/concepts/signal-collapse-after-cheap-production|Signal collapse after cheap production]], [[wiki/frameworks/capability-to-architecture-loop|Capability-to-architecture loop]], [[wiki/debates/does-cheap-code-retire-technical-debt-or-amplify-architectural-debt|Does cheap code retire technical debt or amplify architectural debt?]], [[wiki/debates/does-cheap-implementation-improve-innovation-or-obscure-understanding|Does cheap implementation improve innovation or obscure understanding?]], and [[wiki/trends/software-work-is-shifting-from-code-production-to-orchestration-and-assurance|Software work is shifting from code production to orchestration and assurance]].
- **Publication caveat:** Do not use the proposition’s conceptual and interpretive evidence as additional observation-level proof for the Trend.

#### `prp-47dacc22a69f` — Measuring renewal capacity may preserve capability through transitions

- **Current status:** `strengthened`
- **Evidence profile:** 5 claims; 2 conceptual claims, 3 interpretations; source dates 2021–2025.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Sustaining and Transitions connect renewal metrics with S-curves, career infrastructure, pace layers, legacy expertise, and institutional variation. The proposition turns the existing renewal Concept and Framework into a comparative hypothesis.
- **Connect to:** [[wiki/concepts/capability-renewal-infrastructure|Capability-renewal infrastructure]], [[wiki/frameworks/sustaining-capacity-loop|Sustaining capacity loop]], [[wiki/frameworks/transition-integration-stack|Transition integration stack]], and [[wiki/questions/what-institutions-can-support-a-career-in-invention|What institutions can support a career in invention?]].
- **Publication caveat:** No throughput-versus-renewal comparison currently demonstrates preservation of capability.

### Attention, culture, economics, and stewardship

#### `prp-3f7dbd5fcbe7` — Design stewardship may require imagination and meaning-making beyond instrumental business logic

- **Current status:** `strengthened`
- **Evidence profile:** 4 claims; 1 conceptual claim, 1 interpretation, 2 normative positions; source dates in 2022.
- **Recommendation:** Publish as a strengthened Proposition.
- **Why:** Governance, Culture, Vibe, Futuring, Architectures, and Sustaining independently add design-practice, art, foresight, narrative, emergence, simplicity, and critical-inquiry rationales. The proposition is a normative claim that connects but is not replaced by the existing Concepts.
- **Connect to:** [[wiki/concepts/design-for-emergence|Design for emergence]], [[wiki/concepts/future-narratives-allocate-permission|Future narratives allocate permission]], [[wiki/concepts/vibe-as-contextual-judgment|Vibe as contextual judgment]], and [[wiki/questions/who-gets-to-author-organizational-culture|Who gets to author organizational culture?]].
- **Publication caveat:** Label the normative basis explicitly and note the absence of evaluated participatory stewardship practice.

#### `prp-b77689287c42` — AI content abundance may concentrate attention on already legible creators

- **Current status:** `qualified`
- **Evidence profile:** 4 claims; 1 conceptual claim, 1 observation, 2 predictions; source dates 2022–2023.
- **Recommendation:** Publish as a qualified Proposition.
- **Why:** Networks, Paradigms, Culture, Niches, Vibe, Gameplay, and Futuring repeatedly support abundance and legibility mechanisms while also surfacing niche-entry counter-mechanisms. The unresolved distributional outcome is precisely what makes the proposition valuable to readers.
- **Connect to:** [[wiki/concepts/attention-is-the-scarce-layer|Attention is the scarce layer]], [[wiki/concepts/abundance-relocates-bottlenecks|Abundance relocates bottlenecks]], [[wiki/debates/do-niches-democratize-creative-opportunity|Do niches democratize creative opportunity?]], [[wiki/debates/does-cheap-creation-democratize-expression-or-cheapen-culture|Does cheap creation democratize expression or cheapen culture?]], and [[wiki/questions/who-controls-the-path-between-publication-and-attention|Who controls the path between publication and attention?]].
- **Publication caveat:** Do not imply that incumbents, new entrants, and niches have been compared; prominently retain the counter-mechanisms.

#### `prp-148e7962f080` — A culturally owned new internet wave may emerge among younger participants

- **Current status:** `qualified`
- **Evidence profile:** 6 claims; 2 conceptual claims, 2 normative positions, 1 observation, 1 prediction; source dates 2023–2024.
- **Recommendation:** Publish as a qualified Proposition, with the prior contested assessment prominently included.
- **Why:** Networks, Culture, Futuring, and Transitions preserve a recurring demand for culturally ownable spaces. Paradigms supplies important counter-evidence: an earlier reform movement overlapped, fragmented, and did not establish a coherent successor. A public qualified page can hold both the persistent motive and the fragmented-movement evidence.
- **Connect to:** [[wiki/concepts/contextual-decentralization|Contextual decentralization]], [[wiki/concepts/openness-is-not-self-determination|Openness is not self-determination]], [[wiki/debates/is-technology-resistance-an-obstacle-or-design-input|Is technology resistance an obstacle or design input?]], [[wiki/questions/what-business-model-can-support-a-prosocial-social-network|What business model can support a prosocial social network?]], and [[wiki/questions/who-controls-the-path-between-publication-and-attention|Who controls the path between publication and attention?]].
- **Publication caveat:** State that near-term emergence is contested and that neither a younger-led migration nor a new wave has been observed at scale.

#### `prp-de32f067c458` — Enterprise AI optimization may shift toward useful intelligence per dollar

- **Current status:** `strengthened`
- **Evidence profile:** 3 claims; 2 observations, 1 prediction; source dates 2024–2026.
- **Recommendation:** Publish as a strengthened Proposition; treat it as a measurable future Trend candidate, not a Trend today.
- **Why:** Paradigms and Organization connect model choice with deployment economics and show that technical task exposure can remain economically unattractive. Its evidence base is small but unusually observable and measurable.
- **Connect to:** [[wiki/signals/ai-automation-remains-constrained-by-deployment-economics|AI automation remains constrained by deployment economics]], [[wiki/concepts/abundance-relocates-bottlenecks|Abundance relocates bottlenecks]], [[wiki/frameworks/automation-posture-matrix|Automation posture matrix]], [[wiki/debates/who-captures-the-gains-from-automation|Who captures the gains from automation?]], [[wiki/questions/how-should-firms-measure-value-when-software-is-easy-to-replace|How should firms measure value when software is easy to replace?]], and [[wiki/questions/how-should-products-manage-model-drift|How should products manage model drift?]].
- **Publication caveat:** The corpus does not yet compare enterprise model-selection decisions or useful-intelligence-per-dollar measures over time.

## Propositions to retain internally

#### `prp-e5fc4d5c24c3` — Extended incumbent leadership tenure may create a generational ceiling on innovation

- **Current status:** `open` (reclassified from `qualified` on 2026-07-20)
- **Evidence profile:** 4 claims; 1 conceptual claim, 3 interpretations; source dates 2020–2024.
- **Recommendation:** Retain in the internal backlog; do not publish in its current form.
- **Reason:** The corpus does not separate chronological age, generational cohort, leadership role, tenure, institutional position, incentives, or succession pattern. Publishing the causal wording would give a confounded interpretation more authority than its evidence warrants.
- **Better next form:** A Question such as “How do leadership tenure, cohort, role, and institutional incentives affect technological and institutional innovation?”

#### `prp-7650797f1cdc` — Distributed startup playbooks may become ecosystem infrastructure

- **Current status:** `open` (reclassified from `qualified` on 2026-07-20)
- **Evidence profile:** 4 claims; 1 conceptual claim, 2 interpretations, 1 observation; source dates in 2022.
- **Recommendation:** Retain in the internal backlog; do not publish in its current form.
- **Reason:** The corpus supports ecosystem learning and experienced-workforce mechanisms, but does not observe a distributed playbook becoming shared infrastructure or demonstrate portability across contexts. No current substantive Wiki page shares its cited Evidence, which is a useful warning that the synthesis has not yet entered the graph.
- **Better next form:** Preserve it for individual-source testing or formulate a Question about when shared operational playbooks transfer competence rather than suppress contextual variation.

## Publication implementation

Completed on 2026-07-20:

1. Add a `proposition` type and `wiki/propositions/` directory to the schema, template set, indexes, validator fixtures, and documentation.
2. Reconstruct cumulative Evidence anchors for every published proposition from its assessment history.
3. Preserve each `prp-` identifier on the Wiki page. Mark the corresponding backlog record as `promoted` with the Proposition page as `resolution_target`, so there is one authoritative mature record rather than two.
4. Add readable links to related Signals, Concepts, Frameworks, Debates, Questions, and the existing Trend. Add reciprocal typed relationships where the relationship vocabulary supports them; propose any missing relationship type before changing the ontology.
5. Generate a Proposition index that lists `strengthened` and `qualified` pages. Keep published `contested` pages accessible with a clear warning rather than erasing their history.
6. Replace collection-triggered assessment with source-ingest assessment for published Propositions and remaining internal backlog records.
7. Run `tools/wiki doctor`, `tools/wiki validate`, `tools/wiki index --check`, and the full unit test suite after implementation.

## Continuing editorial decisions

- The two retained records remain internal research prompts unless the editor later elects to turn them into explicit Questions.
- A published Proposition that later becomes `contested` remains accessible with a warning, even if omitted from the normal Proposition index.
- Trend remains a distinct page type rather than a Proposition status.

## Changes made through implementation

- Added the `proposition` schema, template, directory, index integration, fixture coverage, and operating rules.
- Published 19 Proposition pages with their original `prp-` identities and cumulative exact Evidence anchors.
- Marked the 19 corresponding backlog records `promoted` with page resolution targets; reclassified the two retained records as `open`.
- Added readable graph navigation and reciprocal typed relationships to relevant Signals, Frameworks, and Questions; retained Debate, Concept, Hub, and Trend links as readable contextual links where the current ontology has no more precise typed relation.
