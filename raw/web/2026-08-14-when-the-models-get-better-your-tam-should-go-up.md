# When the Models Get Better, Your TAM Should Go Up

## Capture metadata

- Requested URL: <https://x.com/ponnappa/status/2086092033647927533>
- Final URL: <https://x.com/ponnappa/status/2086092033647927533>
- Canonical URL: <https://x.com/ponnappa/status/2086092033647927533>
- Captured on: 2026-08-14
- Capture method: rendered X article inspected in the Codex in-app browser because the source requires client-side rendering

## Captured article

Sidu Ponnappa

@ponnappa

When the Models Get Better, Your TAM Should Go Up

I've spent the last 3 years building an AI Native Services business. From zero traction, product-oriented execution to a services + platform strategy. From thesis limited execution to a fitness function focused on revenue and margin. From $100K of rev in 2025 to ~$3M of rev in the first half of 2026, with over $1M of that from the US.

Over the last month I've had a few founders who are contemplating starting AI Native Services businesses reach out to chat. This list is a distillation of those conversations.

One caveat before the list. Everything below applies to AI Native Services, early stage, selling B2B into the enterprise. Consumer and SMB dynamics are different, and I'm not claiming any of this transfers.

### 1. When models get better, your TAM should go up

The first thing every AI Native business needs to ensure. Most AI businesses are, structurally, the gap between what the models can do and what the customer needs - scaffolding, retrieval, orchestration, evals. Every model release eats a layer of that, and your market shrinks with it. If a better model is bad news for your business, you're arbitraging a capability gap on a timer.

For a services business the test works in your favour, if you build for it. Better models make more work economically viable to take on. Projects that made no sense at 40 hours of human effort make plenty of sense at 8. The frontier of "worth doing at all" moves outward with every release, and your job is to be standing on it when it does.

### 2. Pivoting isn't a problem, it's mandatory

Every step change in AI capabilities should be accompanied by a pivot that takes advantage of the changes. Founders treat pivots as an admission that something went wrong, and in most categories that instinct is fair. Not here. The capability ground moves every 2 quarters, and a strategy that hasn't moved with it has simply gone stale. Plan for the pivot the way you plan for hiring: a recurring part of doing business in a space where the fundamentals change every quarter, not a response to an emergency.

### 3. The rebuild trap is the UX, not the architecture

Whatever you build has to be re-engineerable to take advantage of the next step change without starting over. Everyone thinks the hard part of that constraint is the architecture or the technology, but architectures survive model swaps surprisingly well. What doesn't survive is the UX - the workflow assumptions, the interaction grain, the places where the product quietly encoded how capable the model used to be. That's where the ground-up rebuilds come from, and it's the part nobody budgets for.

In 2023 and 2024 we were building a unit test writing harness for Salesforce Apex code, before the term 'harness' came into use - and we spent 4 months of it solving for accurate diffs, because bad diffs shift the burden to the human, which is bad UX. Then 4o dropped and solved the problem. 4 months wasted.

The risk to mitigate here is time, effort and capital thrown at problems where there is no multi-year window to monetise the solution.

### 4. Product is extracted from Real Work

Not designed in a thesis document, not refined in debates with VCs. Real Work is work an actual enterprise client pays for, ideally executed profitably. Those 2 constraints - someone pays, you profit - are what filter out the product ideas that only work in sales and fundraising decks. The product is already latent in the work; delivery is how you find it.

And to be clear, there's plenty of product left to build - the thing that died was software as an amortisable asset, not product itself. What's scarce now is PMF. Which has quietly become a 2-stage problem: PMF in the market, then PMF in the customer. A product that isn't married to change management services never achieves the second one - it becomes shelfware. Shelfware was a survivable outcome in the 2010s, because B2B SaaS only ever paid lip service to adoption - once the contract was signed, whether anyone used the thing was somebody else's problem. Consumer software never had that luxury; consumer companies die without adoption. And it's early days, but those consumer dynamics - rapid iteration, engagement, adoption - are entering the enterprise now.

In essence: Beware Sales Market Fit without Product Market Fit. The era where the former sufficed to create multi billion dollar B2B SaaS empires is ending.

### 5. Segment users by cognitive load

Every AI solution splits along one line: does the user get more and better work without taking on more cognitive load, or with it?

The first category is the dream - big TAM, respects Krug's "don't make me think". It's also risky, UX-intensive, hard to reach PMF in and brittle in the face of step changes. The second is the opposite trade: fast to PMF, easy to iterate, but talent-intensive and smaller TAM, because the user is paying for productivity with their own attention - they're heavily involved in mitigating slop. Claude Code and Codex live here, and so do their users, happily.

The cardinal sin is building without this distinction.

The Lovables and Emergents of the world genuinely start in the first category, and it genuinely works. But there's a boundary, and the boundary is lindy output. Anything meant to survive and be built upon - a codebase, a large piece of copy - starts demanding cognitive load from the user, usually at an exponential rate. Small snippets of high-quality copy, fine. Lindy larger pieces, demanding. Otherwise code, copy, whatever - it all turns to slop.

And since models and agents glazing their users is now a bedrock feature of the stack, self awareness, taste, judgement and execution discipline are all the responsibility of the human in the loop.

### 6. Don't sell AI Native Services like B2B SaaS

AI Native Services, by definition, should deliver workflows - and business impact - that are humanly impossible. The client starts to move in ways their competition simply cannot keep up with manually. This outcome is the business equivalent of crack cocaine.

And you don't sell something addictive like you do B2B SaaS, which is anything but.

### 7. If it matters, it matters this quarter

The key value prop of AI Native is humanly impossible speed and quality. Here's the uncomfortable part: enterprises mostly don't want it. Speed and quality matter at the top, if at all - and there are industries like banking and insurance where speed is viewed as a serious risk even at the top, and rightly so. Below that, in the middle and bottom layers of the enterprise you find demand in occasional pockets, and usually capped by limited risk-taking ability.

So you sell speed and quality to the segments and the individual decision makers to whom it matters. And there's a clean test for whether it actually matters to them: if it matters, it matters this quarter. Something that matters next year is by definition slow.

### 8. Don't lock into your thesis - follow the money

Your fitness function is revenue, immediately followed by margin. This is a new category. All the look-ahead optimisations - the B2B SaaS ones and the trad services ones - are tuned for categories that already exist, which makes them wrong for this one. Run a greedy algo: take the best-paying work in front of you, extract what compounds, repeat. The TAM test in point 1 is a constraint on what you'll chase, not a 5-year plan - greedy search inside a fence is still greedy search.

The B2B SaaS GTM hangover is what kills momentum in the early days. Back then it made sense to pick a vertical, then a segment, then a channel - and then lock into that at a thesis level. An AI Native GTM is a totally new beast, with different advantages as well as different points of friction in the selling motion. Bad assumptions here can kill all chance at PMF. We lost a year to that - a premature thesis level lock-in into Salesforce implementations. Iterate to an ICP using a greedy search and the fitness function above; don't lock in going in.

### 9. The hype cycle has always been wrong so far

The frontier lab model is baked. The rest of the ecosystem is not - category creation continues. And the tpot/VC hype cycle's track record on where that creation lands is unblemished: fine tuning, RAG, LangChain, "wrapper tech is bad" (haha - Claude Code, Codex and Pi are all wrapper tech, and they gave us the first actual agents) and now software factories. Don't anchor on any of these as a thesis.

The fitness function in the previous point is what you act on as you search the solution space for PMF and growth.

### 10. Talent is always a core pillar

AI Native Services as a model is capped by needing humans in the loop. If no humans are needed in the loop anymore, most of the rules above stop holding and the frontier labs come eat your lunch - and that's assuming the global economy hasn't collapsed from humans not being needed anymore. Which is to say the cap is also the moat - the human requirement is the thing the labs can't route around, and taste, judgement and execution discipline (point 5 again) is what the humans are for.

So talent is always a core pillar of any AI Native Services strategy. Without it, it's just sparkling B2B SaaS.

16:07 · 8 Aug 2026

## Curator pin

Every step change in AI capabilities should be accompanied by a pivot that takes advantage of the changes. Founders treat pivots as an admission that something went wrong, and in most categories that instinct is fair. Not here […] Plan for the pivot the way you plan for hiring: a recurring *part* of doing business in a space where the fundamentals change every quarter, not a response to an emergency.
