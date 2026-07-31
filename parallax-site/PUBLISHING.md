# Publishing to the Parallax website

The live site: **https://parallax-analytics.github.io/Parallax-Research/**
The repository: **https://github.com/Parallax-Analytics/Parallax-Research**

A website is just a folder of files. This folder *is* the website. Whatever is in
the GitHub repository is what the world sees, and it updates within about a
minute of you committing a change.

---

## What each file is

| File | What it is |
|---|---|
| `index.html` | The homepage. **Generated — never edit it directly.** See below. |
| `posts/` | One finished article per file, plus `tokens.css` which supplies their fonts and colours. |
| `_source/homepage.html` | The readable homepage source. This is the one you (or Claude) edit. |
| `_source/build-homepage.py` | Turns `_source/homepage.html` back into `index.html`. |
| `.nojekyll` | Tells GitHub to serve the files as-is. Leave it alone. |

### Why the homepage has a source file and a built file

`index.html` is a *packed* file. Most of its 4 MB is photographs and code
libraries encoded as text, and the page's actual content sits on a single
unreadable line inside it. Editing that by hand is not realistic.

So the readable copy lives in `_source/homepage.html`. You edit that, run the
build script, and it folds your changes back into `index.html`. The script has
been checked to reproduce the original file byte-for-byte when nothing has
changed, so it is safe to run repeatedly.

---

## Publishing a new article — the routine

### Step 1 — Ask Claude to add it

> "Add the [topic] article to the website."

Claude will:

1. Copy the finished `.html` from the article's `Outputs/` folder into `posts/`,
   named after the topic (e.g. `posts/housing-elasticity.html`).
2. Add the article to the list in `_source/homepage.html` — the block marked
   **THE ARTICLE LIST**. Newest goes at the top.
3. Run `python3 _source/build-homepage.py` to rebuild `index.html`.

### Step 2 — Check it yourself, before anyone else sees it

Double-click `index.html` in this folder. It opens in your browser, running off
your own Mac — nothing is public yet. Confirm:

- the new article appears at the top of **Latest Insights**
- clicking its row opens the article
- the article's charts render, and "← All research" gets you back

If something is wrong, say so and it gets fixed before you upload anything.

### Step 3 — Upload to GitHub

1. Go to https://github.com/Parallax-Analytics/Parallax-Research
2. Click **Add file** → **Upload files**.
3. Drag in the files that changed. For a new article that is:
   - `index.html`
   - the new file from `posts/`
   - `_source/homepage.html`
4. In the box at the bottom, type what you did — e.g. "Add Brexit article".
5. Click **Commit changes**.

Uploading a file with a name that already exists replaces it. That is what you
want for `index.html` — it is meant to be overwritten each time.

### Step 4 — Check it live

Wait about a minute, then open the live site. If you still see the old version,
hold **Shift** and click reload — your browser is showing you a cached copy.

---

## Notes and gotchas

**The first time only.** The repository currently contains just the old
`index.html`. On your first upload, drag in *everything* in this folder,
including the `posts` and `_source` folders. After that you only upload what
changed.

**Article links.** Articles live in `posts/`, one level down from the homepage,
so their "back to home" links must read `../index.html`, not `index.html`. The
article template in the Brexit project has been corrected, so anything built
from it is already right.

**`tokens.css` must sit beside the articles.** It carries every colour and font.
An article without it in the same folder renders as unstyled text. There is one
copy in `posts/` and it serves all articles — you do not need another.

**If the build script refuses to run**, it will tell you what it found and will
not have touched `index.html`. Nothing is broken; report the message.

**Nothing is ever lost.** Every commit is kept. If an upload goes wrong, the
repository's **History** tab lets you look at, and restore, any earlier version.
