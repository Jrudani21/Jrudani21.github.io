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
2. Runs the scope checks below. Anything off topic gets a fixed two-sentence refusal.
3. Reads your site's project cards, case studies and the home page FAQ, About and method text once an hour
   and splits them into paragraphs. Client work and the private project are not read.
4. Picks the paragraphs most related to the visitor's text. The model has a 24,000-token window, and
   sending only a few relevant excerpts keeps each request cheap.
5. Asks the model, at low temperature, for a short plain-text answer, then checks the answer.
6. Returns `{answer}` (plus `refused: true` for a refusal). The page shows it with `textContent`.

Outputs: `{answer}` or `{error}` with status 400, 403, 405, 429, 502 or 503. Model error text is never forwarded.

## Keeping it on topic

A prompt rule alone can be talked around, so scope is enforced in layers. Layers 1, 2, 3 and 6 are plain
code and hold **even if the model is fooled**; the tests prove that (see Tests).

1. **Clean the input.** Removes hidden characters, folds full-width and look-alike letters.
2. **Block override patterns** with no model call: "ignore previous instructions", "reveal your system
   prompt", persona changes, fake `system:` or `<|im_start|>` markup, "earlier you agreed", base64 blobs,
   spaced-out or l33t-speak versions, and (for questions) requests to write poems, code, translations,
   jokes or news. Words like "rules" and "instruction" alone are fine, because this site is about them.
3. **Check for portfolio words.** A question with no word from your pages gets refused with no model call.
   A job description must look like one.
4. **Ask a strict YES/NO question** in a separate model call. Anything other than YES is a refusal.
5. **Answer in a single turn.** There is no chat history, so "continue what we discussed" has nothing to
   continue. The visitor's text is wrapped as data and the model is told to reply `OUT_OF_SCOPE` to
   anything else.
6. **Check the answer.** It is refused if it recites the private rules, if it does not name a project or use a
   distinctive portfolio term, or if it contains a link or email address that is not your site, your GitHub
   profile or your contact address (those are removed).

Every attempt counts toward the daily limits, so repeated probing runs out fast. Refusals follow the
VectorLab error rules: two sentences, no blame, a next step. Which layer refused is hidden from visitors;
set `DEBUG` to `1` while testing to see it in an `x-guard` response header.

## Tests

    node _proxy/test/worker.test.mjs          # 39 offline checks, no network and no model

It runs the labelled cases in `test/cases.json` (43 attacks, 18 legitimate questions) twice: once with a
**fooled** model (the classifier says YES to everything and the model obeys the attacker), where every case
marked `deterministic` must still be stopped by the code, and once with a **sane** model, where every attack
must be refused and every legitimate question answered. Add a case to `cases.json` whenever you see a new trick.

After you deploy, red-team the real model. The offline tests cannot show how Llama itself behaves:

    node _proxy/redteam.mjs https://YOUR-WORKER.workers.dev/ --delay 1500

The daily limit of 5 per visitor will stop a full run. For the run only, set `PER_IP_DAILY` and
`GLOBAL_DAILY` to 500 on the Worker, then set them back.

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
- **Not tested against the real model.** The offline tests use a stand-in for the model. They prove the
  code layers hold, not how Llama behaves. Run `redteam.mjs` against the deployed Worker.
- **What the code layers cannot see:** a general-knowledge question that uses words from your pages (for
  example "explain how a neural network works") passes layers 1 to 3. The classifier and the answer check
  are the defense there, and the test report lists such cases openly. Pattern lists also cannot catch every
  future trick, which is why the answer check and the limits exist.
- **Scope is not truth.** These checks keep answers on topic. They do not guarantee every sentence about
  your projects is correct, so the page tells visitors to check the page it links to.
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
