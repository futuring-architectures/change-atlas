# The Network Always Beats the Castle

## Capture metadata

- Requested URL: <https://sundaylettersfromsam.substack.com/p/the-network-always-beats-the-castle?r=1tkru9>
- Final URL: <https://sundaylettersfromsam.substack.com/p/the-network-always-beats-the-castle>
- Canonical URL: <https://sundaylettersfromsam.substack.com/p/the-network-always-beats-the-castle>
- Captured on: 2026-08-31
- Capture method: complete article retrieved from the rendered Substack page through the web reader

## Captured article

The Network Always Beats the Castle

Why AI is Chaos that Scales, and why organizations are about to completely change.

Sam Schillace

Jun 28, 2026

I am so sorry that this is so long. I really like shorter things and simpler ideas. But this feels a bit larger to me, and it puts into words something that’s been banging around my head a bit. I wanted to work through some of the implications more completely (and, full disclosure, unusually for me, I worked with an AI - Sonnet - on writing this. But I promise I have read and edited and reworked every single word of it - it’s all me).

Here’s a nerdy TL;DR if you want it: I think AI will enable a switch from what is essentially circuit switching today, in all kinds of organizations, to something that will look and feel a lot more like packet switching. This will happen partially because it can now (AI is to this problem what fast processors were to distributed networking protocols), and because networks are almost always more powerful, flexible, and scalable.

This idea is going to feel super uncomfortable and be rejected by business leaders, employers and academics in much the same way that network engineers rejected the idea of packet-switched networks.

OK - that’s the whole thing at light speed. Read on if you want to wade through the reasoning a little more leisurely with me.

In 1965, making a long-distance phone call in America was a feat of engineering coordination. A call from New York to Los Angeles required a dedicated copper path, physically reserved, for the duration of the conversation, and AT&T had to employ armies of switching engineers to manage this. The Bell System was one of the great technical achievements of the twentieth century, and the people who built it were not fools.

They worked ferociously for what they were optimizing for: guaranteed, high-quality, reliable connections between two points.

It seemed fine - expensive, but that’s what everyone was used to. If you are my age, you remember when long-distance was even a thing, and those calls cost more and were precious. I still get a tiny bit nervous talking to my parents 3000 miles away in Michigan, that was so deeply ingrained. Part of me still can’t believe that phone calls all cost the same.

Then a small group of researchers, largely funded by ARPA, mostly working in universities,[1](#footnote-1) proposed something that sounded to the Bell engineers like a joke. Instead of reserving a dedicated path, you would break messages into small pieces, label each piece with a destination, and release them into the network to find their own way. Different pieces of the same message might travel completely different routes. They might arrive out of order.

There was no guarantee that any particular piece would arrive at all. A phone call, under this scheme, would be like mailing a letter by tearing it into a hundred pieces and dropping each one in a different mailbox, hoping they’d all show up. (Kind of like training a giant AI model on lots of small fragments of language (tokens) and hoping that somehow intelligence would emerge from putting them back together randomly - which largely worked).

The Bell engineers had a name for this general idea: chaos. They had a specific critique too, which was that you couldn’t make any guarantees about quality of service. Voice needs low, consistent latency: you can’t have some syllables arriving seconds after others. And of course, data needs reliability: a corrupted file is useless. The engineers were right about all of this. Packet switching, in its early forms, was genuinely worse at the things circuit switching was designed to do.

It also, within a few decades, made the Bell System irrelevant. The internet didn’t improve on the telephone network; it made the telephone network a minor application running on top of something much larger. Today your phone calls travel as packets (which is why they all cost the same - there’s no such thing as a “long circuit” now), just like everything else. The Bell engineers optimized for the wrong thing. I love that this also has a flavor of “worse is better”.

The Bell engineers were optimizing for “correct, complete, but complex and rigid” and the internet is more “simple and recoverable beats correct and complex”.

What actually happened was a philosophical shift about where intelligence should live. Circuit switching is a centralized control philosophy. Someone, somewhere, reserves the path before any message travels it. The network takes responsibility for delivery. The endpoints are dumb; they just send and receive. All the complexity, all the guarantee-making, lives in the infrastructure itself.

This works, and it scales up to a point, and then it hits a wall, because the central system has to know everything about every connection, and that knowledge becomes impossible to manage as the network grows. (Sound familiar? This is how we build companies these days. We’ll come back to that idea)

Packet switching inverts this entirely. The network is dumb and the endpoints are smart. A router doesn’t understand the content of the packets it handles - it reads a destination address and forwards the packet one hop closer. The intelligence about what the message means, whether it arrived correctly, what to do if it didn’t - all of that lives at the edges, in the devices doing the communicating. The protocol defines what the endpoints must do. The network just moves bits.

You have seen this argument before, in a different domain. Central planning versus markets is the same disagreement. The Soviet planning apparatus tried to do for an economy what circuit switching does for a telephone network: reserve resources, guarantee outcomes, manage the whole system from the center.

It failed not because the planners were stupid but because the information required to run a complex system centrally exceeds what any center can hold (it also failed because many of them were corrupt, and centralized systems are vulnerable to this, since there’s no way to build in mechanisms to correct, outcompete or otherwise reverse that corruption).

Prices, in a market, are packets. They carry information about supply and demand from the edges without anyone at the center having to understand or coordinate it. Markets are chaotic, wasteful, frequently unfair, and they consistently outperform central planning at scale for the same reason the internet outperformed the Bell System. The network always wins, eventually, because the network is where the information actually lives.

Let’s think about companies now. Companies love to do re-orgs. Or at least, they have to do them. They’re a lot of work, just like it was a lot of work to organize and change the old Bell network, and for the same reasons. Companies have to deal with the pain of organizational overhead, because to a large extent, they try to do central planning - circuit switching.

A manager, in an org chart, is a leased line. From an organizational perspective, they’re like a circuit between strategy and execution, reserved whether or not signal is flowing. The org chart is the circuit map. It tells you the paths that exist, which means it also tells you the paths that don’t.

If you need to get information or work from point A to point B and there’s no line between them on the chart, you have a problem - you need to go up to a common node and back down, or you need to get someone to lay a new line. When a company needs to change how it behaves, it rewires the circuit map, which we call a reorg.

Why do we do this? This is not because companies are stupid or because the people running them lack imagination (hopefully). It’s because circuit-switched organizations are the only kind that could be managed without the infrastructure that packet-switched organizations require (which isn’t unlike what happened with the internet - we needed cheap processors to be able to build routers that could handle packets fast enough. Before we had that, we had no choice but to set up dedicated circuits).

If you can’t do the things an organization needs - observing and judging work, finding capabilities, holding people accountable - without the overhead of a fixed org chart, well, you just have to have it.

The cost of this solution is enormous and mostly invisible because it’s so normalized. The cost isn’t just the reorg itself - the lost productivity, the damaged relationships, the months of internal politics while the new structure settles. Even in steady state, a circuit-switched organization spends huge amounts of bandwidth on path maintenance: the status meeting, the update email, the weekly one-on-one, the steering committee that exists to keep the connections live. Most of this is not work.

It is the overhead of maintaining dedicated paths between people, so that when work needs to travel, the path is ready. It is, in network terms, keeping the circuit open even when nobody is talking.

It’s what we’re used to, and even though it’s expensive, cumbersome and hard, it seems ok, just like the old phone system did.

When packet switching was proposed, the experts who objected most loudly were the most qualified people in the room. They were “right” in an engineering sense, but wrong in the systems sense. And they did what most people do, asking a “why not” question (against the old design and constraints) instead of a “what if” one: what if the new processors could enable a new network design?

Most people looking at AI are making the same mistake, and I predict we will see a lot of this from the orthodox “business advisor” community. I hear this from engineers and leaders already, and it sounds just like the Bell folks: You can’t guarantee accountability in a decentralized system. You can’t audit a network that routes around hierarchy. Regulators will never accept this. Sophisticated investors will raise concerns about governance.

All of these objections will be correct in the short term and beside the point in the long term. They are right from some kind of local engineering perspective but wrong from an emergent systems perspective. The question is not whether packet-switched organizations perform better on the metrics that circuit-switched organizations were built for. They won’t, at least at first, just like packet-switched networks didn’t at first.

The question is whether the new architecture unlocks things the old one couldn’t do at all. And I think it will - I think we will get levels of scale, creativity and responsiveness by using these new tools to push intelligence to the edge of all kinds of organizations - not just businesses but political, social, educational and creative ones. We’re just talking about business here because this is already a monster of a post, but I’ll probably dig into the others later.

There is a useful heuristic here, which is that disruptive ideas tend to produce a room that’s roughly split in half. Usually something like half the people think the idea is obviously correct (the folks asking “what if”), and half think it’s obviously wrong (the “why not” crowd).

I’ve written about this kind of bifurcation before - this is the sign of something that is genuinely disruptive, and the split is between people who are rejecting it because it feels threatening, and people who have internalized the new world view and are beginning to extrapolate it.

People have tried versions of packet-switched organizations before. So why might this work now? Holacracy, self-managing teams, flat hierarchies, network organizations - the management consulting literature has been circling this idea for decades. These experiments mostly failed, and the failure was usually attributed to culture or leadership or change management. Occasionally that was true. More often, the infrastructure simply wasn’t there.

You cannot run a packet-switched network without routers, protocols, addressing, and error correction, and you can’t build any of that until you had cheap enough, and fast enough, processors to put everywhere. Building a self-managing organization in 2010 was like trying to run the internet before TCP/IP existed - the vision was right, but the stack was missing.

AI is that missing piece - cheap enough intelligence to put “everywhere” and enable a bunch of these ideas for real. It’s the equivalent of those cheap processors finally showing up, except it’s a much more complete stack arriving all at once.

We can see this already in little bits. We are just starting to make use of AI giving us intelligence at the edge. We can do more work, sure, and we have issues with that work being high quality (work slop). But the really interesting things are the new capabilities - people being able to make use of expertise “on tap” that used to be hard or slow or expensive. Ask any designer or product lead how awesome it is to not have to ask engineers to build prototypes for them.

As we learn to trust these tools, more and more decisions and behaviors will be pushed out to the edge where they can be used fluidly.

AI can also be the routing layer itself. In a packet network, a router doesn’t need to understand what’s in the packet - it reads the destination address and makes a local decision. An AI system can do the organizational equivalent: read a piece of work, understand what it requires and what constraints it carries, and match it to the right human capability without a manager in the path. Work can find the people who can do it, rather than being handed down a chain.

We are starting to work with systems like this on my own teams. Right now, again, it’s in fits and starts because all of the plumbing isn’t there, so the AI doesn’t always have all the context (and we don’t fully trust it always yet). I think this will get better, fast - we’re going to start to see teams soon that don’t do scrum, they just talk to the AI about what the goals are and what needs doing, moment-to-moment.

AI can also be the translation layer. A significant fraction of what managers do is not coordination - it’s making the work of their teams legible to people above them or next to them in the hierarchy. This is genuinely necessary in a circuit-switched system, because the only way information gets from the edge to the center is through the human chain. AI can make edge work directly legible to whoever needs to see it, continuously and without the translation cost.

When you can see the packets, you don’t need to own the pipe.

Networks and organizations also have to do error correction, and AI helps here too. TCP/IP’s reliability doesn’t come from perfect transmission - packets get dropped constantly. Reliability comes from detection and retransmission: something notices the dropped packet and asks for it again. In organizations, that function is the follow-up email, the status check, the escalation path, all the daily meetings and OKRs and reports ad nauseam (my ADHD is showing).

All of that is expensive human attention spent on what is essentially a signaling problem. AI can run that loop continuously, noticing when something hasn’t arrived, or is blocked or when a metric is off, without burning anyone’s working memory on the monitoring. This will mean organizations can do more things - remember, human attention is the most important resource now. Anything like this that optimizes for it, will win, eventually.

We don’t think of it this way, but in companies as well as networks, there is also protocol negotiation. Before two systems (or teams) can communicate, they have to agree on terms: what format the data is in, what the constraints are, what counts as success. In organizations, this is scoping and contracting and alignment, and it is largely not done, because it is tedious and humans are bad at being tedious on purpose (I definitely am).

The result is that work starts without the interface definitions in place and everything becomes expensive later. AI can do this rote work: given a task and the people who will do it, surface the assumptions that need to be agreed on before anything flows, and check to make sure the goals were met consistently.

Finally, there is the address space problem. In a network, every node needs an address so that packets can find it. Before DNS, finding a machine required knowing its numeric address, which meant knowing the topology. In organizations today, finding the right person or team for a given problem requires knowing the org chart, again, knowing the topology. AI can create a capability address space independent of org structure, so that work can find the right node without anyone needing to know the map.

This is a precondition for packet-switched organizations working at all.

The point is not that any one of these is transformative on its own. TCP/IP was not one protocol - it was a suite of interlocking ones that only worked as a system. DNS, BGP, TCP, UDP, IP - each solves a different piece of the problem, and you need all of them before the network actually functions. We got the internet because all of these good ideas were waiting for processors and networking hardware to be able to support them.

We have similar ideas waiting for something like AI to support them inside companies and organizations. Modern AI is providing analogous coverage for organizations, and it is doing so in a compressed timeframe.

What do the organizational protocols actually look like? I don’t quite know yet - I think we are still working that out. But if you have patience, we can explore a bit.

The internet was proposed in the late 1960s and didn’t have a stable protocol suite until the early 1980s. There were false starts, competing proposals, ideas that seemed right and turned out to be wrong. The packet-switched organization is probably somewhere around 1972 right now: the architecture is becoming clear, but the protocols are not finished, and some of what we think we know will turn out to be wrong.

That said, the analogy gives useful guidance about what shape the protocols need to take. (This section is going to be super nerdy - skip it if you like).

TCP and UDP represent a distinction that organizations have mostly refused to make: not all work needs the same reliability guarantee. TCP is expensive - it establishes a connection, numbers every packet, requires acknowledgment, retransmits anything that gets dropped. You use it when order and completeness matter and you can afford the overhead. UDP doesn’t do any of that. It sends packets and doesn’t look back.

You use it for things where timeliness matters more than completeness, like streaming video or a live sensor reading where a stale packet is worthless. Organizations currently treat almost everything like a phone call: maximum overhead, guaranteed path, constant connection maintenance. Some work genuinely requires that. But a lot of work is and can be UDP: best-effort, async, fire-and-move-on. Knowing the difference, and building processes around it, is a protocol decision.

We don’t have a good way to deal with this now - all we have are expensive humans, so even the discussion of “is this work UDP or TCP” is too expensive. AI makes that cheaper.

DNS is the discovery problem. The internet needed a system where you could find a machine by name without knowing its address - a layer of indirection between what you wanted and where it lived. Organizations need a capability registry that is similarly independent of org structure: a way to say “I need someone who can do X” and have the system surface the right people, without the questioner needing to know the hierarchy.

This probably looks like a combination of skills graphs, project history, and AI-mediated matching. It does not currently exist in any mature form. Again, this is now largely a “plumbing and context” problem. We have this info, sort of, but the AI can’t make use of it. My team has been exploring tools for this, too.

Subnets and domains address the trust and permission problem. The internet is not flat, it has hierarchy, but the hierarchy is about addressing and permission boundaries, not about controlling the path of every packet. A corporate subnet can be isolated from the public internet. A domain can have its own DNS. These boundaries define what can talk to what without specifying how the conversation has to go.

Organizations need analogous structures: nested trust boundaries, permission scopes, accountability domains that define the space within which work routes freely, and the boundaries at which additional authorization is required. This is not the same as a management hierarchy. It is a different, more flexible structure that enables local autonomy within defined boundaries.

BGP, the protocol by which autonomous networks negotiate with each other about how to exchange traffic, addresses something organizations haven’t had to think about yet but will: how do packet-switched teams, or companies, or AI agent networks, communicate across their boundaries without any of them being “in charge” of the others? The answer in networking is a protocol for exchanging routing information between peers.

Something like that will be needed for inter-organizational work in an AI-native world, and we don’t have it yet. I feel this pain already on development teams, and I know others do: as agentic coding makes us hugely more capable, it’s really hard to coordinate with each other, since we all have so much going on. I suspect this is a large, hard problem that we will need to solve, and I don’t know how to solve it yet.

The process of designing these protocols will be messy and hard - ironically, it will likely not happen in a central way, but through distributed experimentation and competition. The network will design the next network!

The internet’s apparent freedom runs on extremely strict, hard-won, boring contracts between machines. If packet-switched organizations get adopted as an aesthetic before the protocols are built, the result won’t be decentralized empowerment, it’ll be chaos with good marketing. The management consultants who tried to implement holacracy without the infrastructure mostly produced that. The protocol work is unglamorous, slow, and essential.

The Bell engineers who resisted packet switching were not, in the end, wrong about what they said. Voice quality did suffer in early VoIP, packets did get dropped a lot, and for a while, quality was worse. But they were wrong about what would matter in ten years, and catastrophically wrong about what would be possible in thirty.

Email was not a better telegram, the web was not a better encyclopedia, and streaming was not a better cable network. Each of these looks, in retrospect, like an obvious evolution, but none of them were conceivable from inside the circuit-switched world (I remember the freak out about how video was going to break even the highly scalable new internet. It wasn’t even thinkable in the circuit switched world). They required the new infrastructure before anyone could imagine what to build on it.

The organizational equivalent is similarly hard to see in advance. It is likely that packet-switched, AI-native organizations will not just do existing organizational things more efficiently, but that they will do things that are not currently possible. There might be organizations that form around specific problems and dissolve when the problem is solved, rather than persisting as structures in search of purpose, or expertise that routes to where it is needed rather than being allocated by headcount.

We might have large groups with a degree of strategic flexibility and sophistication that have never existed together - we might get political or creative movements in radically different shapes because of that. We are definitely going to see an evolution in the creation, management and use of institutional memory. Training will probably look very different, as will job descriptions.

And almost certainly: we will get things we cannot name yet. Nobody in 1975 could have described Google, or Facebook, or VOIP, or even Google Docs.

The phone company’s engineers built something extraordinary. The Bell System was a genuine engineering achievement, and the people who designed it were some of the best technical minds of their era. They lost anyway. Networks are more robust, once the infrastructure to support them exists, and the right protocols to create and maintain them are adopted.

My bet is that the organizations of the future, the ones that compete and thrive, will make use of AI to build networks the same way the internet made use of those cheap processors and new protocols to build huge scale and new capabilities.

This will feel controversial, and might even be worse at first, but networks always win. The age of centrally planned organizations is coming to an end.

Thanks for reading Sunday Letters! I promise they’re not usually this long.

<a id="footnote-1"></a>1. The irony of right-wing antigovernment propaganda largely existing because of something created by that very kind of government program they hate, is rich.
