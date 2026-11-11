# Ask-my-portfolio proxy (optional, free)

Powers two panels in the "Try it" section of `index.html`: **Ask my portfolio** and **Job-fit check**.
Both stay hidden until the page is given this Worker's address, so the site is complete without it.

This folder starts with `_`, so Jekyll does not publish it. It holds code only. There is no API key
anywhere in this setup.

## What it uses

A free open model on **Cloudflare Workers AI**: `@cf/meta/llama-3.3-70b-instruct-fp8-fast` (Llama 3.3 70B).
It runs inside the Worker through a binding, so there is no key to leak and no separate account to pay.
Cloudflare lists zero data retention for this model. Check the model page again before you deploy,
because the catalog changes: https://developers.cloudflare.com/workers-ai/models/

## Cost: $0 on the Workers Free plan

Workers AI gives 10,000 Neurons a day at no charge. On the Workers Free plan, going past that makes
requests fail with an error instead of billing you. One answer here is roughly 120 Neurons, so the free
allowance covers about 80 answers a day. The default caps are 5 per visitor and 40 overall per day, which
leaves headroom. **Stay on the Workers Free plan.** On Workers Paid, usage past the free allowance is
billed.

## What it does

Trigger: the page sends `POST {mode: "ask" | "jobfit", text}` from `https://jrudani21.github.io`.
Inputs: the visitor's text (3 to 400 characters for a question, 20 to 4,000 for a job description).
What happens:
1. Checks the origin, the method, the size and the daily limits.
2. Reads your site's project cards and case studies once an hour and splits them into paragraphs.
3. Picks the paragraphs most related to the visitor's text. The model has a 24,000-token window, and
   sending only a few relevant excerpts keeps each request cheap.
4. Asks the model, at low temperature, for a short plain-text answer, and strips any markdown.
5. Returns `{answer}`. The page shows it with `textContent` and links project titles.

Outputs: `{answer}` or `{error}` with status 400, 403, 405, 429, 502 or 503. Model error text is never forwarded.

## Deploy (Cloudflare dashboard)

1. Workers and Pages, Create, Worker. Paste the contents of `ask-worker.mjs`, Deploy.
2. Settings, Bindings, Add, **Workers AI**. Set the variable name to `AI`.
3. Optional but recommended: Storage and Databases, KV, create a namespace, then bind it as `RATE`.
   Without it the limits live in memory and reset when the Worker restarts.
4. Optional variables: `PER_IP_DAILY` (5), `GLOBAL_DAILY` (40), `MODEL`, `ALLOWED_ORIGIN`
   (`https://jrudani21.github.io`), `SITE_ORIGIN` (same), `DISABLED` (`1` switches it off at once).
5. In `index.html`, set the section's address: `<section id="labs" data-endpoint="https://YOUR-WORKER.workers.dev/">`.
6. Commit as `portfolio: enable the ask panels`, then push.

Check it from a terminal. A request without a matching `Origin` header must be refused:

    curl -s -X POST https://YOUR-WORKER.workers.dev/ -H 'content-type: application/json' \
      -d '{"mode":"ask","text":"What is Ken?"}'            # expect {"error":"origin"} (403)

    curl -s -X POST https://YOUR-WORKER.workers.dev/ -H 'content-type: application/json' \
      -H 'Origin: https://jrudani21.github.io' \
      -d '{"mode":"ask","text":"What is Ken?"}'            # expect {"answer":"..."}

## Limits and honest caveats

- **Quality:** an open 70B model follows instructions less reliably than the biggest paid models. It can
  miss a match or word things loosely. The page tells visitors to check the page it links to. Read a few
  real answers after you deploy and tighten `RULES` in the Worker if it drifts.
- **Not tested against the real model.** The tests in this repo use a stand-in for the model, so they
  cover the plumbing (checks, retrieval, limits, error handling), not the quality of real answers.
- **Origin check:** it stops other websites from using the Worker in a browser. It does not stop someone
  scripting requests with a forged `Origin` header. The daily caps are what bound the use.
- **Model changes:** Cloudflare retires models on a schedule. If answers start failing with a 502, check
  the model page and set `MODEL` to a current instruct model. For a long context, try
  `@cf/mistralai/mistral-small-3.1-24b-instruct` (128k tokens, higher cost per request).
- **Privacy:** visitor text goes to Cloudflare Workers AI to produce the answer. The page says so next to
  each panel. Answers use only your public pages. The private assistant project and the client work cards
  are not in the context on purpose.
- No streaming: an answer arrives all at once.

## Turning it off

Set `DISABLED` to `1` in the Worker (the panels then show "switched off"), or empty `data-endpoint` in
`index.html` (the panels disappear).
