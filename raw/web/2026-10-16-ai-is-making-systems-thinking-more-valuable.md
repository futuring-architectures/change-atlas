# AI Is Making Systems Thinking More Valuable

## Capture metadata

- Requested URL: <https://camilleesq.substack.com/p/ai-is-making-systems-thinking-more>
- Final URL: <https://camilleesq.substack.com/p/ai-is-making-systems-thinking-more>
- Canonical URL: <https://camilleesq.substack.com/p/ai-is-making-systems-thinking-more>
- Captured on: 2026-10-16

## Captured article

AI Is Making Systems Thinking More Valuable

As AI makes individual capabilities easier to access, advantage may increasingly come from knowing how to assemble them into systems that actually work.

Camille Stewart Gloster

Oct 01, 2026

Share

A recent conversation with security leaders started with a practical question: what does it actually take to deploy AI agents across an organization?

One idea kept surfacing: platform engineering, the practice of creating shared infrastructure and services so individual teams can build without repeatedly solving the same problems around deployment, security, access, and operations. As agents connect to more systems and take more actions, that function becomes increasingly important because agents need identities, access to data and applications, permission to act, and records of what they have done. The ⁠Cloud Native Computing Foundation’s work on platform engineering for the agentic enterprise describes how this discipline is evolving as AI agents become consumers of enterprise platforms alongside people.

What interested me most about the conversation, though, was what platform engineering reveals about a much broader shift. AI is making it cheaper and easier for more people and teams to create sophisticated capabilities. Every new agent, automated workflow, and integration also becomes part of a larger system that someone has to understand and coordinate.

As creation gets easier, coordination becomes more important. Platform engineering is one organizational response to that challenge, while systems thinking may be the corresponding human capability.

By systems thinking, I mean looking beyond the task in front of you to understand the dependencies, incentives, authority, feedback loops, and consequences that shape how the larger system behaves. As AI makes it easier to change one part of a system, understanding what that change does to the rest becomes more valuable.

AI is changing the system around the work

In ⁠last week’s article on what happens to human expertise when AI does more of the work, I asked what people should become better at as AI performs more of their existing work. Systems thinking offers one answer because it shifts our attention from performing a task to understanding and designing the system in which that task occurs.

Consider something as ordinary as employee onboarding. An HR team could deploy an agent that answers questions, schedules training, sends reminders, initiates account requests, and updates records. Each task may work well, but the agent’s place in the larger organization raises additional questions. Which employee data can it access? Which systems can it change? Are this changes reversible? Who approves sensitive access? What happens when someone’s role changes? Who owns the agent, where are its actions recorded, and who can intervene when something goes wrong?

Whether that automation works reliably depends on much more than the agent itself. It depends on people, data, technology, permissions, vendors, controls, and decisions made elsewhere in the organization.

As AI makes it easier for individual teams to automate work, these relationships multiply. That decentralization is already visible in enterprise environments. Opsin Labs’ 2026 analysis found that two-thirds of agents it observed were built by nontechnical departments. Customer service can build an agent, finance can automate reconciliation, and IT can create an operations assistant, with each team making reasonable decisions about its own integrations, credentials, logging, and controls. In aggregate, those choices can leave an organization with duplicated infrastructure, excessive permissions, unmanaged credentials, fragmented logging, and dependencies no one deliberately designed.

Systems thinking helps us see what those local decisions create together.

Reuse turns individual decisions into organizational capability

Platform engineering provides a useful example of what that looks like in practice. Instead of every team separately deciding how an agent authenticates, what systems it can access, how credentials are managed, what gets logged, and when a human needs to intervene, organizations can establish common services and patterns that teams inherit as they build. CNCF describes platform engineering as a response to precisely this kind of complexity, using shared platforms, standardized environments, and self-service capabilities so individual development teams do not have to master every operational requirement themselves.

That matters because organizational maturity depends in part on the ability to turn good individual decisions into capabilities other people can reuse. A policy requiring least privilege becomes more useful when narrowly scoped access is built into the environment. A traceability requirement becomes easier to satisfy when identity, logging, and telemetry are already available. A decision that certain actions require human approval becomes more reliable when the operating environment can enforce that requirement.

Pieces of this infrastructure are already emerging. ⁠NIST’s AI Agent Standards Initiative is supporting work on secure and interoperable agents, including research into agent authentication and identity infrastructure and work on agent identity and authorization. ⁠Microsoft Entra Agent ID provides identity, access management, lifecycle governance, and protection for AI agents, while CNCF is examining how platforms themselves evolve when agents operate alongside human users.

The specific technologies will change, but the organizational principle is more durable:

Governance becomes more scalable when good decisions can be translated into reusable capabilities rather than repeatedly rediscovered through individual reviews.

Organizations have always benefited from turning good individual decisions into institutional capabilities that others can reuse. AI raises the stakes because decisions about automation, access, and authority will multiply faster than any central team can reasonably review them one at a time.

The principle applies to smaller organizations too. They may never have a dedicated platform engineering team, but they can still decide which approaches to identity, access, logging, data, and approval should carry across AI deployments rather than allowing every new tool or workflow to establish its own rules.

Authority has to become enforceable

One particularly important part of this system is authority. In The Insider You Built, I focus on what AI systems are allowed to access, decide, change, communicate, or spend in pursuit of an objective. I describe the approach as Authority-Centered Enforcement, or ACE, which starts with deliberate decisions about the authority an AI system receives and carries those decisions through to the controls that govern what it can actually do.

Platform infrastructure is one place those decisions become operational. Identity establishes who or what is acting, permissions determine what the agent may access and do, runtime controls shape which actions remain available, and observability and revocation help organizations understand how authority was exercised and intervene when necessary.

If an agent is authorized to retrieve information, for example, the environment can withhold the permission required to change a record. As systems move from reading information to recommending actions and then acting independently, the authority they receive and the controls surrounding that authority should change with them.

Recent enterprise telemetry shows why that distinction matters. In the environment, Opsin Labs analyzed, 60% of agents were over permissions, with access beyond what their intended purpose required.

We are beginning to see versions of this principle implemented directly in enterprise infrastructure. Microsoft’s ⁠Entra Agent ID authorization architecture explicitly blocks agent identities from receiving certain high-privilege roles and permissions, including sweeping administrative privileges, while allowing appropriately scoped access. Microsoft describes the design as reflecting the principle that agents should operate with limited scope and least privilege.

NVIDIA’s recently announced ⁠Open Agent Safety Platform addresses another part of the problem. Its OpenShell software establishes a runtime boundary that can trace actions and enforce policy while an agent operates, while Sentry provides separate monitoring and can quarantine agents that move outside established boundaries. NVIDIA explicitly argues that enterprises need an enforceable boundary outside the model and agent harness as agents take on more work across more systems.

Microsoft and NVIDIA are addressing different layers of the technology stack, but both illustrate a broader architectural shift: decisions about machine authority increasingly need to be enforceable where action occurs. That is ACE in practice, even when it goes by other names.

Systems thinking can also make accountability clearer

The same perspective helps with a problem that will become harder as AI-enabled work crosses more organizational boundaries: who is accountable for what?

An AI-enabled outcome may depend on a business leader who defined the objective, a team that designed the workflow, a platform that supplied the agent’s identity, a security team that established access requirements, a vendor that supplied the model, data maintained by another part of the organization, and a person responsible for reviewing or acting on the result.

Trying to assign accountability only after something goes wrong can obscure how the system actually worked. Mapping the system in advance makes it easier to distinguish different responsibilities. Who owns the outcome? Who decides what the agent is supposed to do? Who grants its authority? Who owns the data and systems it uses? Who monitors its behavior? Who can stop it? Who is responsible for learning from failures and changing the system afterward?

Those questions matter because meaningful responsibility depends in part on the decisions, information, and control different actors actually have within the system. A team cannot effectively manage a risk without the information or authority needed to address it, while governance functions cannot substitute for clear ownership across the rest of the system.

Systems thinking therefore supports more than technical architecture. It can help organizations make accountability clearer by mapping dependencies, decision rights, authority, and intervention points before an incident forces everyone to reconstruct them.

Scale should create leverage

Reusable capabilities can give organizations both governance leverage and greater room to experiment. When identity, logging, credential management, and other controls are incorporated into the environment teams already use, organizational requirements can travel with the technology rather than depending on every team to reconstruct them.

This also gives us a more useful way to think about scale. An organization can deploy more agents while accumulating bespoke integrations, credential schemes, review processes, and logging approaches that make every subsequent deployment harder to manage.

An organization is building the capacity to scale AI when it can deploy useful AI repeatedly without increasing cost, risk, and complexity at the same rate.

A practical test follows: Does deployment N+1 become easier, safer, more observable, and more efficient because of what the organization learned and built during deployments 1 through N? If the answer is consistently no, more AI may be entering the organization without a corresponding increase in organizational capability.

That capability includes more than infrastructure. Organizations also need to maintain and develop the human knowledge and judgment their AI-enabled systems depend on. One response to last week’s article raised a useful question: if AI can help spread the practices of experienced workers, how will people continue developing the expertise behind those practices as AI takes on more of the work through which it was historically acquired?

That leads to a broader systems question: What capabilities does this system depend on today, and how will it maintain and develop them over time?

A system can perform well today while gradually weakening a capability it will need later. Understanding those dependencies, including how they are maintained and replenished, is part of designing the system itself.

The organizational capability is bigger than the platform

Platform engineering can make identity, access, monitoring, and other technical capabilities reusable across AI deployments. The larger challenge is deciding how those capabilities should fit into the way the organization actually works: what AI should be allowed to do, where human judgment matters, who has authority to make which decisions, how responsibility is distributed, and what happens when something goes wrong.

Those questions cannot be resolved by technology alone because they depend on the purpose and context of the work. Deciding which data an agent should access, how much autonomy it should have, which failures are tolerable, and when an action requires escalation draws on business context, technical expertise, security, risk, legal judgment, and the experience of people who understand the work being redesigned.

The same systems problem is becoming visible across the technology industry. In September, companies spanning identity, cloud, data, applications, infrastructure, and cybersecurity formed the ⁠Blueprint Alliance to develop an open, multi-vendor reference architecture for securing AI agents. Its principles include treating agents as identities, scoping access to the task, keeping delegation traceable, continuously monitoring runtime behavior, and enabling containment that is reversible.

The breadth of that coalition illustrates the challenge: agents cross boundaries among models, data, applications, identity systems, networks, and infrastructure that organizations and technology providers have historically managed as separate domains. AI increasingly connects those domains while simultaneously making it easier for more people and teams to create new capabilities that depend on several of them working together.

Platform engineering helps organizations manage some of those connections technically.

Systems thinking helps organizations decide how those pieces should work together, who is responsible for what, and whether the resulting system can reliably produce the outcomes they want.

We may all need to become better systems thinkers

The same logic extends beyond technology teams and organizations. As AI performs more individual tasks, a durable human capability may be understanding the system around a task well enough to redesign it.

A lawyer using AI for contract review needs to know which analysis can be delegated, what evidence must be preserved, which decisions require legal judgment, and where errors become consequential. A security analyst working alongside automated investigations has to understand how evidence is gathered, where an agent could be misled, and which actions require approval. A manager redesigning a business process has to account for the data AI requires, how exceptions move through the organization, where authority should be constrained, and whether the redesigned process still creates value once downstream work is counted.

These roles share a growing need to see work as a system rather than a collection of tasks. Deep domain expertise remains essential because it helps people recognize when an AI-enabled process is subtly wrong or missing important context. Alongside that depth, AI may increase the value of a more architectural way of thinking: understanding how specialized capabilities interact and how changing one part of the work affects the rest.

The architecture does not have to be technical. It can be the architecture of a workflow, a decision process, a team, a customer experience, or an organization.

A few questions can help put that thinking into practice. What are we trying to optimize, and what does that outcome depend on? What changes elsewhere when we automate or redesign this part of the work? Who owns the decisions and authority at the points that matter? What capabilities must we maintain, develop, or make reusable for the system to keep working over time?

Those questions move us beyond asking whether AI can perform a task and toward understanding what happens to the larger system when it does.

The advantage may move up a level

Having access to capable models will increasingly tell us less about whether an organization is good at using AI. The surrounding system will tell us much more: whether the organization can connect AI to useful context, allocate authority deliberately, understand and interrupt what agents are doing, make accountability clear, reuse successful patterns, maintain the human capabilities it still depends on, and learn from one deployment in ways that improve the next.

That is why a conversation about platform engineering among security leaders felt much bigger to me than a conversation about technology infrastructure. It was really a conversation about what organizations and people need to become good at as intelligence becomes easier to access and action becomes easier to automate.

In The Insider You Built, I focus on delegated authority because AI systems create greater value as they gain the ability to act on our behalf. The identity, permissions, boundaries, observability, intervention, learning, and accountability surrounding that authority are part of a larger systems challenge that will appear under different names and be owned by different teams. As AI gains the ability to act, organizations need to translate decisions about its authority into the systems where that action occurs.

The same shift has implications for individuals. As AI takes on more individual tasks, more of our value may come from understanding how those tasks connect to everything around them and using that understanding to design better workflows, decisions, and organizations. The next advantage may belong less to the people and organizations with access to the most AI capability than to those who know how to assemble capability into systems that work.

Leave a comment

Subscribe

Share

PreviousNext

## Curator pin

The specific technologies will change, but the organizational principle is more durable: Organizations have always benefited from turning good individual decisions into institutional capabilities that others can reuse. AI raises the stakes because decisions about automation, access, and authority will multiply faster than any central team can reasonably review them one at a time.
