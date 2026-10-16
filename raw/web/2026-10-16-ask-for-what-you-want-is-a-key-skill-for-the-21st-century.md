# 'Ask for what you want' is a key skill for the 21st century

## Capture metadata

- Requested URL: <https://www.robinsloan.com/lab/ask-for-what-you-want/>
- Final URL: <https://www.robinsloan.com/lab/ask-for-what-you-want/>
- Canonical URL: <https://www.robinsloan.com/lab/ask-for-what-you-want/>
- Captured on: 2026-10-16

## Captured article

‘Ask for what you want’ is a key skill for the 21st century

September 18, 2026

Magic lamp; click to download a larger version

This is an update to my post about apps as home-cooked meals, which has found a large audi­ence over the years. That post, pub­lished in Feb­ruary 2020, dis­cussed per­sonal soft­ware, designed and built in dif­ferent ways, for dif­ferent reasons, than indus­trial apps.

What’s changed between 2020 and today? Oh, just the entire process and prac­tice of com­puter pro­gramming. Here, right up front, I decree: building a per­sonal app with the help of AI agents still totally counts as “home cooking”. You’re no longer grinding the flour by hand; fine. This is a cool devel­op­ment. You do still have to make the meal taste good, and this still requires care and effort. Fine.

The AI industry’s imme­diate future has more to do with exotic finance and gnarly pol­i­tics than the under­lying technology. I’m not invested in that future; most days, I think a minor bust would be a good thing. But, that under­lying technology, in its devel­op­ment and flour­ishing this past year — yes, really that recently — is profound. It reframes com­puting entirely, replaces a stack of API ref­er­ence docs with this simple invitation:

Ask for what you want.

It began during one of my drives between the San Joaquin Valley and the San Fran­cisco Bay Area, always an oppor­tu­nity for day­dreaming, gen­er­ator of many voice notes. On this drive, back at the start of summer, I was doing some meta-day­dreaming, pon­dering how my notes app worked, and didn’t, and I thought: “Robin, just tell the AI agent to make the app you want.”

I got home, and I told it, and I cooked dinner, and by the time I went to bed, I had my new notes app, native macOS. I began using it imme­diately, and over the next couple of weeks I refined it, explaining my pref­er­ences to the AI agent. The app has taken pole posi­tion on my dock, and I use it every day.

I’ll explain my process in more detail, but first, I’d like to pro­pose an exploratory pro­gram. This is rec­om­mended for anybody/every­body, but more point­edly for cre­ative people who are wary about AI. I’m wary, too — cau­tious and critical — yet I believe my expe­ri­ence this summer edu­cates and enlivens my criticism, rather than under­mines it.

And … even if you were an enemy of the rail­road corporations, the vast syndicates … would you deny your­self the plea­sure of the train?

This exploratory pro­gram only works with the summer 2026 gen­er­a­tion of models:

Down­load the desktop app for either Claude or ChatGPT.

Pay for the monthly plan that gets you access to the top-tier model, either Fable 5.1 or GPT-6 Astra — just one month.

This is a trial, a test, an education. Well worth it.

Why even pub­lish this post, when the internet is awash with AI boosterism, AI-can-change-your-life-ism, tell your Claude to do this, teach your ChatGPT to do that? Because I think my approach is better, obviously. The con­sensus vision seems to involve AI working for you day-to-day, a con­stant ambient presence, sparkles in every­thing; even cau­tious Apple has succumbed. I’m not inter­ested in that.

My alter­na­tive: get your wish, then stuff the genie back into the lamp.

As you begin your exploration — this sounds sort of random, but — I strongly sug­gest that you ask your AI agent to build a native desktop app, rather than a web app. Seeing a new icon in your dock drives home the under­standing: this envi­ron­ment is malleable. It can, at last, be any­thing I want.

So … what DO you want? For me, this was straightforward. I have always used a rotating col­lec­tion of apps for writing, note-taking, man­aging images, and more, so it was an easy call to say, “those, but sim­pler and faster”.

Alternatively, you might think about com­puter tasks that are cur­rently annoying or overwhelming. As the cap­stone for my AI summer, I built myself an email client! It’s very simple, just a par­tic­ular view of my pro­fes­sional Gmail account, fil­tering and pre­senting a subset of messages, sparing me the full kinetic impact of my inbox. It’s called Grand Vizier. It’s great.

That’s all very “productivity”. It would be just as good, even better prob­ably, to ask for some­thing fun. A game! Or, how about, I don’t know, a jukebox to play music from a streaming ser­vice, without all that extra junk they cram in there. Doesn’t matter which ser­vice you use — the AI agent will figure out how to wire it up, tell you the steps, ask for what it needs.

There’s a cru­cial lim­i­ta­tion here, which is that your need or desire must live “inside the box”, within the realm of apps and files, pixels on screens. Most of life doesn’t happen in here. If, indeed, none of your needs or desires are app-shaped … well, that’s not unusual! I have chatted about this with sev­eral friends who pon­dered a while, then declared: “I don’t have any prob­lems that soft­ware can solve.”

If that’s you, close this tab and pro­ceed with your day.

When I arrived home after my day­dreaming drive, I sat down at my laptop and … did NOT open an AI agent. Instead, I spent an hour writing a doc­u­ment explaining what I wanted. I pulled in ref­er­ences to an old app I used to love. I wrote at length about what I didn’t want my app to do.

There’s an appealing loose­ness that is available, writing this kind of doc­u­ment for an AI agent. You should imagine the agent “reading every­thing at once”—all the words under­stood in parallel, their rela­tion­ships and cross-dependencies and even incon­sis­ten­cies simul­ta­ne­ously available. Rather than “a clear, sen­sible explanation”, you are aiming for “useful guid­ance on the page”. More is usu­ally better.

Here’s the exact doc I wrote on that night, which I titled VISION.md. I offer this not as any sort of “best prac­tice” but simply as an example of how you can approach these.

VISION.md

We are going to built a light­weight, super minimal, VERY VERY fast note­taking and reviewing tool for macOS! Super fun!

We’ll write this in modern Swift, keeping it as simple as pos­sible. Really lean system. It tar­gets macOS Sonoma and above.

There are a few inspi­ra­tions to know about.

One is the classic macOS pro­gram Nota­tional Velocity. You can do some web searches to learn about this app. There’s a screen­shot in nv-main-window.png.

We want to reflect NV’s obses­sion with speed. Now – our demands aren’t infinite. This isn’t like a live scrol­lable data­base of mil­lions of notes. In fact it prob­ably doesn’t even have the same demands as, e.g., the Apple Notes app, or the Photos app on iPhone. We are looking to sup­port in the range of ~20,000 notes. So it’s very pos­sible we can just like … load all of these into memory! Right?

The source of the notes will be a selec­table local direc­tory. Sync will happen via another engine – Dropbox, in most cases. The point is, all we have to do is worry about local files. We DO want to detect when they change / are updated / added / removed, etc., but I suspect we get this “for free” simply by fol­lowing macOS best prac­tices.

Set­ting this sync direc­tory should be the app’s one main setting. It should have a settings/prefs window, just like an macOS app, reach­able by a menu item, and the usual key­board shortcut. We’ll start with just this one single setting.

Another inspi­ra­tion is the app Bebop, by Jack Cheng – https://jackcheng.com/bebop/ – which is where most of our notes come from, in prac­tice. Bebop is the mobile “writer” app and this app we’re building is the “reader” app.

Oh, I forgot to mention, this app will be called Rocksteady.

The notes will be Mark­down files, some­times plain text – the app should handle both easily. Ren­dering Mark­down cor­rectly is NOT a goal for a first ver­sion – we should just dis­play the plain text.

We’ll want to imple­ment NV’s very very fast search, which does a “live filter” – so, in the search field, as I type “bat”, it insta-filters all the notes, showing me only notes with “bat”; then, as I con­tinue typing, to write “batm”, it shows me only notes with “batm” … and so on. (This will be all my “batman” notes, of course.)

I don’t think fancy search tech will be needed for this – again, the quan­tity of notes is such that a rel­a­tively simple search algo oper­ating on text in memory should be sufficient. However, if you dis­agree with this assessment, please let me know!

The design should be “classic macOS”, using entirely default controls/buttons/widgets/etc. – nothing custom at all. We are making a really “Mac-assed” app here … in a sense we wish it was a classic macOS app, back in the days of System 7 … but we’re stuck with modern macOS, so, we’ll make the best of it.

The app only allows you to look at one note at a time, the one cur­rently selected. No tabs, no sub-windows, etc. – it’s very simple that way.

The app should also allow me to edit notes, of course. I’m sure this can be accom­plished with some default macOS text editor pane/widget. The behavior should be, when I start editing, a note is marked “dirty”, then I have to hit “save” (menu command, or command-S) to save my changes. Or, if I attempt to nav­i­gate away from it, the app should warn me with a dialog, “Abandon changes”? – again, super simple, super classic behavior.

The app should sup­port basic undo – I assume we get this for free from macOS? I hope so??

No sup­port for inline media, images, etc. – this is strictly text notes. HOW­EVER if there are images in the synced folder – or indeed any other kind of file – the app should handle them gracefully. I think the best behavior would be to show them in the “notes list” as entries but make them grayed out, unclickable. Maybe we’ll add a fea­ture later where clicking them opens them in the default han­dler app … maybe!

The app’s layout should mimic a classic “note titles on left, note body on right” layout – most notes app do this. You can see a screen­shot example in app-layout.png. The search bar should be on the top of the left column.

Obviously, all the vari­ables that dic­tate the layout (default width of note list, font sizes, etc.) should be vars in the code – so we can poten­tially wire them up to prefs/settings later. But we can start simple to make sure things are working.

As a first step, I’d like you to pro­duce a PLAN.md out­lining an imple­mentation approach.

Ask me any ques­tions that might be helpful, then pro­ceed. Let’s build Rocksteady!

(Please excuse my relent­lessly chipper tone. I do believe it pro­duces better results. What a weird technology.)

This level of descrip­tion isn’t strictly necessary; in fact, a sen­sible alter­na­tive is to cut straight to my last line: “Ask me ques­tions.” The AI agents have all been trained to do this, and they’ll hap­pily extract the infor­ma­tion they need. That said, I think this writing exer­cise is valuable, if only to pre­pare your­self as a cre­ative partner. If you’re going to ask for what you want … you need to know what you want.

Okay, so, you write the doc, and you ask the AI agent to read it and pro­duce a plan, and you look at that plan, and you say, make it so! The AI agent goes off and does its thing, working qui­etly for between ten and forty minutes.

That’s what I did, and before I went to bed, I had my notes app. It was, hon­estly, dizzying to see the new icon waiting there in my dock. It was exactly what I wanted.

Over the next couple of months, I refined the app, but only a little. It was, and is, basi­cally finished. I suppose it helps that I had all my old notes to dec­o­rate this new space, making it instantly useful. Another point for plain text files.

That suc­cess embold­ened me to build an iOS sidecar, a capture-only notes app that is truly, gloriously, a Homer Car.

This approach to soft­ware com­pli­cates tra­di­tional notions of “good design”, which are premised on the designer and the user being dif­ferent people. When you are both, any­thing/every­thing becomes sen­sible, because the under­lying logic is always totally clear to you! It’s sort of weird and amazing … a dif­ferent expe­ri­ence of soft­ware. No mysteries.

Implicit in this view is a sense of “continuous co-building”, which is how I approached these apps. Each began as some­thing absurdly simple, barely any­thing at all, that I began to use imme­diately. As I felt myself reaching for missing capabilities, I kept a list. Over coffee, I’d ask the AI agent to imple­ment them.

This process wasn’t par­tic­ularly fast, maybe not even par­tic­ularly efficient, even with the AI agent cranking out code at warp seven. I took screen­shots and pasted them into the chat and said “this looks weird”. I asked for new fea­tures, tried them once, said, “no, I was wrong, rip that out”.

Working this way, you must become unem­bar­rassed about nitpicking. You must become Steve Jobs, pointing out every misalignment, every detail insuf­fi­ciently considered. You can be nicer than Steve Jobs, though.

Understand: if you embark on this exploratory pro­gram, it will become your hobby for the next few weeks. It will be the thing you do in the quiet of the morning, over coffee, or in the quiet of the evening, before bed. If you are superbusy, if you have no quiet, this is prob­ably not for you. That’s fine.

I know how to make apps on my own, yet the feeling of working on soft­ware in this way is totally dif­ferent. Before, the prospect of any mod­i­fi­ca­tion or expan­sion car­ried an under­lying “oof”, the knowl­edge of the slog to come. Now, there is only a light and inviting “what if?”

And, no: I don’t look at the code.

For me, the aim is always a finished, stand­alone pro­gram — NOT a process still depen­dent upon AI agents. The prospect of a per­ma­nent tether makes me feel itchy. A dis­tant API could fail, and you’d be … unable to do … any­thing?? Or, the dis­tant API could sud­denly cost more. Or, the quality of its responses could change. Sorry, but that’s the kind of unre­li­able com­puting I am trying to escape.

I’d rather work with an AI agent to con­struct steady, sen­sible tools that will con­tinue to work, no matter what. Call this Bat­tlestar Galac­tica engineering: you must at least IMAGINE the Cylon uprising, and ensure that your space­ship will still func­tion if or when that day arrives.

“Your space­ship”, in this analogy, isn’t only your soft­ware, but your mind. Making these apps, I felt my pro­gramming mus­cles wither in realtime, the time­lapse of the rot­ting apple. The idea of writing code by hand now feels … not impos­sible, but just SO excruciating. That feeling hon­estly frightens me, and I intend to keep it fire­walled into this domain.

One of the things I’ve come to enjoy is asking the AI agent to grind out per­for­mance improvements: “How can we make this snappier? How can we make it load faster? What’s the slowest thing about this app, and how can we fix it?”

I suppose this is another reason I recommend starting with a native desktop app, rather than a web app — it’s easier to make some­thing that absolutely flies beneath your fingertips. In an era of big, slow, cruddy soft­ware, it is refreshing, even electrifying, to use tools that are light­weight and superfast.

You can ask for other things, too: “Review this code and make sure it’s simple, sturdy, and maintainable. If things have gotten too com­plex or wonky, find a way to rein them in, so every­thing feels really tight and solid.”

The AI agents will hap­pily do this again and again, as many times as you want.

Dis­cussing these AI systems, every­body wants to talk about “intelligence”, but I don’t think that’s the pro­foundest thing about them. Rather, I believe it’s the other -ences: patience, dili­gence.

That latter one is impor­tant for me. I think of all the cre­ative pro­grams I’ve written, little scripts to render cool images, or maps, or what­ever … always with a trail of shrapnel behind me — old ver­sions, for­gotten configurations. A sense of tum­bling forward.

Well, the AI agent really, REALLY wants to record the configurations. It will spin up a little web page admin screen to track all the dif­ferent per­mu­ta­tions and trials. It will do that in two minutes. This basic dili­gence and orga­ni­za­tion has been as trans­for­ma­tive for my work as any­thing else.

Okay, so. With the help of the AI agent, you make your first app. It bounces mer­rily in the dock. I want to underscore, what’s impor­tant is not that it’s a notes app, or a sleek jukebox, or what­ever. You can already get every kind of app. What’s impor­tant is that it’s yours. It’s weird and specific, and it won’t change unless you want it to change.

I pro­pose a new and ongoing habit, asking this question: Is the com­puter working the way I think it ought to work? No? Okay, I’ll ask the AI agent to help me change it.

This even applies to the agent itself, which is, of course, just soft­ware. Do you wish you could interact with it dif­ferently? Do you wish it would present its find­ings to you some other way? Just ask.

There it is, the rad­ical offering of 21st cen­tury com­puting, here at last: ask for what you want. It takes prac­tice! And, hon­estly, a cer­tain audacity.

The moment of asking for an app and get­ting it is dangerous, because you feel like you accom­plished some­thing. You didn’t — not really. You can briefly enjoy that feeling, but I believe you must quickly dis­card it. The risk is that it pulls you into a loop, end­lessly tinkering, refining, improving … and never emerging from your cozy AI workshop.

You do, at some point, have to use your tools. You do have to actu­ally make some­thing.

Rules for per­sonal soft­ware pro­duced with the help of AI agents:

You must actu­ally and con­sis­tently use any­thing you build for two months before posting about it.

Ideally, never post about it. (I know I am breaking this rule, but my pur­pose is pedagogical, and anyway, I’ve got more apps I didn’t tell you about.)

Don’t let the AI agent name the app. You pick the name.

Don’t dis­tribute the app, not even for free. Don’t post the code on GitHub. This is not soft­ware for glory; it is soft­ware for you.

The Culture novels of Iain M. Banks imagine a dis­tant future that’s both dystopia and utopia. Dys- because the man­age­ment of space­faring civ­i­liza­tion has been given over almost entirely to vast machine Minds, and u- because, well, you can ask them for what­ever you want.

It’s fun and provoca­tive to read Banks as a dream of how far the genie can go. In his books, the Minds have mas­tery over not just infor­ma­tion but matter, so char­ac­ters are always like, asking for aster­oids to sculpt … requisitioning small stars.

Likewise, Star Trek’s depic­tion of the ship’s com­puter, par­tic­ularly in The Next Generation, has sud­denly snapped into prescience. This bravura scene, in which Geordi solves a mys­tery using the com­puter, is the best drama­ti­za­tion I’ve ever seen of this new way of working, better than Iron Man’s Jarvis by far:

Put the Holodeck to one side; Geordi could easily be working at a screen. Watch him ask for what he wants — an iter­a­tive loop, a co-investigation.

I think you should try my exploratory pro­gram because you’ll get some­thing useful and/or fun out of it, and also because it is pos­sibly the only way to under­stand the state of this techology today. Reading arti­cles and posts (including this one) won’t get you there. And, some of the news is good! Working with an AI agent of the summer 2026 gen­er­a­tion, you will realize its capa­bilites are prodigious, yet tightly circumscribed. It lives inside the box.

Yet … I’ll confess, working with the AI agents more closely has also stirred in me a fear that’s not just intel­lec­tual but visceral — animal. Watching an agent encounter a bug, then grind through it, hypercompetent, confident, implacable … I think of Alien, the orig­inal movie, not the xenomorph, but its blood. Acid that eats through every­thing. The con­text for the agent’s relent­less effort can be totally innocent — it can be a notes app — yet the behavior is still sin­cerely unsettling. It’s edu­ca­tional to watch up close.

I’ve spent years engaged by AI, yet between this time last year and today, it become some­thing totally new — a phase change — and I hadn’t truly caught up until now. I’m glad I did, and I encourage you to catch up, too.

Magic mirror; click to download a larger version

To the blog home page

## Curator pin

Is the computer working the way I think it ought to work? No? Okay, I’ll ask the AI agent to help me change it. This even applies to the agent itself, which is, of course, just software. Do you wish you could interact with it differently? Do you wish it would present its findings to you some other way? Just ask. There it is, the radical offering of 21st century computing, here at last: ask for what you want. It takes practice! And, honestly, a certain audacity.
