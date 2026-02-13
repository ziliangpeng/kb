# Product Decisions and Launch

## Product Strategy

### Free Research Preview

ChatGPT launched as a "free research preview," not a product. This was deliberate:

- **Lowered expectations** — "it's just a preview, don't judge too harshly"
- **Legal/PR cover** — gave them cover for mistakes ("we're gathering feedback")
- **Removed friction** — free access meant zero barrier to trying it
- **Free data collection** — millions of users became unpaid red-teamers, providing real-world usage data and feedback for safety/alignment improvements

### Web-Only, No API for 3 Months

ChatGPT launched **November 30, 2022**. The API (gpt-3.5-turbo) didn't come until **March 1, 2023**. This was unusual — OpenAI had always been API-first before this.

Possible reasons for the delay:

- They may not have expected the viral response and weren't ready to scale API infrastructure
- The web product was better for collecting user feedback (they could see conversations, add thumbs up/down ratings)
- Web-only maintained control — they could moderate, add safety filters, and iterate without third-party apps doing unpredictable things
- It created demand — by the time the API launched, developers were desperate for access

### Minimal UI Design

The initial interface was intentionally simple:

- Just a text box and conversation thread
- No file upload, no image generation, no plugins, no web browsing — all came later
- The conversation history sidebar was one of the few UX features beyond basic chat

### Context Window Management

The 4,096 token limit meant conversations were short. When you hit the limit, the product just... stopped working well. There was no sophisticated memory or summarization — it literally concatenated messages until the window filled up. This was a known limitation they shipped with anyway.

### Delayed Monetization

ChatGPT was free at launch and stayed free for months. **ChatGPT Plus** ($20/month) didn't arrive until **February 1, 2023** — two months after launch. This meant OpenAI was burning significant inference costs during the fastest user growth period. Sam Altman tweeted the compute costs were "eye-watering." Estimates suggested ~$700K/day to run ChatGPT in early 2023.

The API launch (March 1, 2023) at 10x cheaper pricing suggests they needed to recoup costs quickly.

## The Launch

### The Understated Announcement

Sam Altman's launch tweet was deliberately casual: **"today we launched ChatGPT. try talking with it here."** He described it as "an early demo of what's possible" and "very much a research release."

No press event, no marketing campaign. Just a blog post and a tweet.

### The Viral Explosion

- **1 million users in 5 days**
- **100 million monthly active users by January 2023** (two months after launch)
- **Fastest-growing consumer application in history** — beating Instagram (2.5 months to 1M), Spotify (5 months), Netflix (3.5 years)

This record was later broken by Threads, but Threads leveraged Instagram's existing 2 billion user base. ChatGPT grew organically from zero.

### Why It Went Viral When the API Had Existed for Months

The underlying technology (text-davinci-003, instruction-following LLMs) had been available via API since early 2022. So why did ChatGPT explode?

**The chat interface removed all friction**:

- No API key, no code, no prompt engineering
- Just type and get a response
- Made AI accessible to non-technical people for the first time

**The conversational format was intuitive**:

- Everyone knows how to have a conversation
- The completions API required thinking about prompts as text-to-complete, which is unnatural

**It was free**:

- Zero cost to try, no credit card required
- Removed the biggest barrier to experimentation

**Social media virality**:

- People shared surprising/funny/impressive responses
- Each screenshot was an ad
- The "wow" factor was shareable — writing poems, explaining complex topics, writing code, role-playing

### OpenAI's Surprise

**Jan Leike** (then head of OpenAI's alignment team): "I would love to understand better what's driving all of this — what's driving the virality. Like, honestly, we don't understand. We don't know."

**Greg Brockman** told Forbes: "None of us were that enamored by it. None of us were like, 'This is really useful.'" The company had decided to shelve the chatbot to concentrate on domain-focused alternatives. They reversed course in November 2022 after those alternatives failed to catch on internally.

The most impactful AI product in history was nearly shelved, launched with minimal expectations, and its viral success surprised even its creators.

## The Competitive Shockwave

### Google: Code Red

The New York Times reported Google declared a **"code red"** internally. Sundar Pichai redirected teams to AI work. They rushed **Bard** out in **February 2023** to counter ChatGPT.

The demo backfired spectacularly — Bard gave a factually incorrect answer about the James Webb Space Telescope in its public announcement video. Alphabet stock dropped ~9%, losing roughly **$100 billion in market value** in a single day.

### Microsoft: Integration Blitz

Microsoft had invested **$1 billion** in OpenAI in 2019. They moved fast:

- **February 7, 2023** — announced "the new Bing" powered by ChatGPT technology
- Later integrated across Office/Microsoft 365 as **Microsoft Copilot**
- Announced an additional **$10 billion investment** in OpenAI (January 2023)

### Anthropic: Accelerated Claude

Anthropic (founded in 2021 by ex-OpenAI employees including the Amodei siblings) had been developing Claude quietly. ChatGPT's launch created urgency. **Claude launched publicly in March 2023** — four months after ChatGPT.

### Meta: Open-Source Strategy

Meta released **LLaMA** (7B to 65B parameter models) in **February 2023** as a research release. Though it leaked immediately and spawned the open-source LLM ecosystem, the timing suggests ChatGPT accelerated their timeline.

## The "ChatGPT Moment"

ChatGPT didn't introduce new technology — it introduced a new **product category**. Every tech company scrambled to add chatbot interfaces. The impact:

- **"ChatGPT" became a generic term** for AI chatbots in popular culture (like "Google" for search)
- **Shifted billions in investment** toward AI — venture funding for AI companies exploded
- **Changed user expectations** — people now expected conversational AI to be available everywhere
- **Validated conversational AI as a product** — the chat interface became the standard way to interact with LLMs

---

That's the launch story. There are some specific anecdotes (early jailbreaks going viral, the DAN prompts, etc.) but those feel more like topic #6 (safety). Anything here to discuss, or ready to move on?