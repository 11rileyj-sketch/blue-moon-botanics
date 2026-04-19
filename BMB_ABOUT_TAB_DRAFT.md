# Blue Moon Botanics — About Tab Draft

*For review and refinement before implementation*

---

## Tab label suggestion

**✦ About** — consistent with the ✦ June tab styling

---

## Content

---

### What is this?

Blue Moon Botanics is a plant care companion that actually knows your plants.

Not generic advice pulled from a search result. Not a one-size-fits-all watering schedule. A care profile built around the specific plant in your specific home. And eventually, around the real-time environmental data of your space.

The goal is a personal plant care professional in your pocket. One who can help you identify what you're growing, tell you what it needs, and (down the road) read the humidity sensor in your greenhouse and tell you if your Calathea is in its happy place.

We're not there yet. But we're growing.

---

### Who is it for?

If you just brought home your first pothos and have no idea what you're doing, this is for you.

If you've got a jungle for a living room and you're thinking about wiring up environmental sensors to monitor your collection, this is for you.

The gap between those two people is mostly confidence and vocabulary, not capability. Blue Moon Botanics aims to close that gap.

---

### Who made this?

My name is Justin. Most mornings I'm the last link in a long, interconnected chain of logistics that I rarely get to see in its entirety. My workdays are siloed. Nothing carries over and every morning is a clean slate.

I came to this project via a confluence of a persistent curioiusity in how things work and the recognition that growth is rarely easy but routinely rewarding. I asked myself in which direction could I point my attention to engage my curiousity and maximize my learning potential.  And I realized almost immediately I wanted to learn about a topic rich in data and high in practical application so I could really get my hands dirty.  Literally, as it turned out.  

So I landed on plants. Partly because they're everywhere. Partly because the data pool is extraordinarily deep. Partly because they're just beautiful. But why limit myself to experiencing growing pains in learing one subject when I could double my discomfort?  In for a penny, in for a pound. 

I was always interested in computers and electronics and equally intimidated by how complex they were.  Tinkering with them felt like it came with a high barrier to entry. Turns out that feeling, standing at the edge of something unfamiliar and not sure if you have what it takes, is exactly how a lot of people feel about keeping a plant alive or building an app.

Into the deep end I went.  I hope to help people understand their plants better, first and foremost.  Behind the scenes, I hope people can take away the realization that complex electronic systems are built on very basic principles.  Buildling your own is well within your reach.  And maybe if only as the part of the iceberg beneath the surface, I hope I can help people realize that it's okay to feel out of your depth.  

Jump and find your wings on the way down.

---

### About June

June is the AI at the heart of Blue Moon Botanics.

The goal for June is to be the kind of expert who doesn't make you feel stupid for asking.  The goal is for her to feel like someone who knows considerably more than you do and doesn't feel the need to perform enthusiasm about it. Warm through competence, not through cheerfulness.

Right now June's scope is focused. She's growing.

---

### A note on where things stand

This is a beta. An early one.

The app works. The care data is real. But there are rough edges, missing features, and more than a few things on the list that haven't been built yet.

Good plant care isn't rushed. Neither is this.  

Expect updates of every strip from the functional to the cosmetic and eventually dipping int0 community-based features. If something feels broken or missing, it probably is, and it's probably already on the list. If it's not, tell me.

Thanks for being here early.

---

## Implementation notes for session

- Tab order becomes: **Add a Plant → My Collection → ✦ June → ✦ About**
- Or consider merging June and About — June's tab is currently a placeholder anyway. Could reframe it as "✦ June & About" or just put the About content beneath the June intro in the same tab.
- Styling: use existing `.june-intro` card style for section blocks, `.bmb-tagline` for section labels, keep it consistent with the existing design system.
- No new CSS classes needed — everything maps to what's already there.
- Content should be editable — consider whether this lives in app.py directly or gets pulled from a markdown/json file for easier future edits.
