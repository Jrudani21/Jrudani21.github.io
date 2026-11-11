# Ask-my-portfolio proxy (optional)

Powers two panels in the "Try it" section of `index.html`: **Ask my portfolio** and **Job-fit check**.
Both stay hidden until the page is given this proxy's address, so the site is complete without it.

This folder starts with `_`, so Jekyll does not publish it. It holds code only. No key is in the repo.

## Why a proxy

A public page cannot hold an API key: anyone could copy it and spend your money. The page calls this
Worker, and the Worker holds the key, checks the request, limits use, then calls Claude.

## What it does

Trigger: the page sends `POST {mode: "ask" | "jobfit", text}` from `https://jrudani21.github.io`.
Inputs: the visitor's text (3 to 400 characters for a question, 20 to 4,000 for a job description).
What happens:
1. Checks the origin, the method, the size and the daily limits.
2. Reads your site's own pages (the project cards and the case studies) once an hour.
3. Calls `claude-fable-5-2` at low effort with that text as context, with refusal fallbacks turned on.
4. Returns `{answer}` as plain text. The page shows it with `textContent` and links project titles.

Outputs: `{answer}` or `{error}` with status 400, 403, 405, 429, 502 or 503. Upstream error text is never forwarded.

## Cost

Claude Fable 5.2 is $8 per million input tokens and $40 per million output tokens. The portfolio text is
roughly 25,000 tokens and is prompt-cached for an hour, so a typical answer costs a few cents.
The default caps (15 requests per visitor per day, 300 per day overall) keep the worst case under about
$10 a day. Also set a monthly spend limit on the API key's workspace in the Anthropic Console.

## Deploy (Cloudflare Workers, free plan is enough)

1. Cloudflare dashboard, Workers and Pages, Create, Worker. Paste the contents of `ask-worker.mjs`, Deploy.
2. Settings, Variables and Secrets: add the secret `ANTHROPIC_API_KEY`. Use a key made for this only,
   in its own workspace with a spend limit.
3. Optional but recommended: Storage and Databases, KV, create a namespace, then bind it to the Worker
   as `RATE`. Without it the limits live in memory and reset when the Worker restarts.
4. Optional variables: `PER_IP_DAILY` (15), `GLOBAL_DAILY` (300), `EFFORT` (`low`), `ALLOWED_ORIGIN`
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

- The origin check stops other websites from using it in a browser. It does not stop someone from scripting
  requests with a forged `Origin` header. The daily limits and your spend cap are what bound the cost.
- Answers come only from your public pages. The private assistant project and the client work cards are not
  in the context on purpose.
- Visitor text is sent to Anthropic to produce the answer. The page says so next to each panel.
- No streaming: an answer arrives all at once, usually in a few seconds. Fable 5.2 can think for longer on a
  hard job description, so the page waits up to 60 seconds.
- To change models later, set the `MODEL` variable. If a newer model rejects a parameter, check
  Anthropic's migration notes before changing this file.

## Turning it off

Set `DISABLED` to `1` in the Worker (the panels then show "switched off"), or empty `data-endpoint` in
`index.html` (the panels disappear).
