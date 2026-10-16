# Data storage - portfolio

There is no server-side database. The only persisted state is client-side, owned by the
Puter.js to-do demo in `index.html`.

| Store | Key | Written by | When |
|---|---|---|---|
| Puter cloud KV (`puter.kv.get/set`) | `portfolio-todos:v1` (`TODOS_KEY`) | to-do widget | visitor is signed in to Puter |
| Browser `localStorage` | `portfolio-todos:v1` | to-do widget | fallback when not signed in or Puter fails |

Value shape: a JSON snapshot of the visitor's task list (`JSON.stringify(snap)`); the input is
capped at `maxlength="300"` per task. Reads and writes are wrapped in `try/catch`, so a blocked
`localStorage` degrades silently.

Data belongs to each visitor (their browser or their own Puter account). The site owner
does not receive it.

Fill in more here only if a backend, form submission, or analytics store is added.

## Verified against

`index.html` lines 1128-1147 (widget markup) and 2686-2860 (`TODOS_KEY`, `puter.kv`,
`localStorage` calls).
