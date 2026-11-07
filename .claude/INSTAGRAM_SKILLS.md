# Instagram skills

22 Claude Code skills for growing @raj_in_jp. Because they live in this repo's
`.claude/skills/` folder, they load automatically in any Claude Code session
opened on this repo. Type `/` to see them, or just ask ("fix my bio", "write a
caption for this reel").

## Where they came from

Both packs are MIT licensed. The license texts are in `licenses/`.

**[Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)**, 13 skills:

| Skill | Use it for |
|---|---|
| `ig-profile` | Score the profile out of 100 and rewrite what loses points |
| `ig-audit` | Read your insights: which posts worked, what to stop |
| `ig-reel` | Reel hook options, script, on-screen text, beat sheet |
| `ig-caption` | Caption, search terms, three hashtags, lint |
| `ig-carousel` | Carousel cover and slide copy |
| `ig-story` | Daily story sequence and stickers |
| `ig-plan` | The week: what to post, when, who to engage with |
| `ig-viral` | Find reels working in your niche, build a swipe file |
| `ig-repurpose` | Turn a long video or post into a week of content |
| `ig-comment` | Comments on other people's posts |
| `ig-reply` | Replies to comments on your posts |
| `ig-dm` | DMs: keyword delivery, collab pitches, follow-ups |
| `ig-human` | Strip AI tells from any draft and score it |

**[sergebulaev/instagram-skills](https://github.com/sergebulaev/instagram-skills)**, 9 skills:

| Skill | Use it for |
|---|---|
| `ig-profile-optimizer` | Second-opinion profile and bio audit |
| `ig-caption-writer` | Caption with the hook in the first 125 characters |
| `ig-carousel-planner` | Slide-by-slide carousel plan |
| `ig-content-planner` | Weekly plan built on content pillars |
| `ig-hashtag-strategist` | 3 to 5 hashtags sized niche / mid / broad |
| `ig-hook-extractor` | Work out the hook formula of a post you admire |
| `ig-audience-insights` | Niche and competitor stats |
| `ig-repurposer` | Rebuild YouTube / blog / X content for Instagram |
| `ig-humanizer` | Remove AI tells, audit before posting, build a voice profile |

## Folder layout

- `skills/`: the 22 skills
- `references/`: shared guides the second pack reads (hook formulas, voice rules, hashtags)
- `lib/`: the second pack's Python helpers, used only for optional auto-publishing (Publora), live data (Apify) and image generation (Pixfaro)
- `instagram/voice.template.md`: template for your voice file. The first pack looks for it at `~/.claude/instagram/voice.md`.
- `licenses/`: MIT licenses for both packs

## Optional keys

Everything works without keys: you paste in screenshots or stats, and you copy
the finished text into Instagram yourself. Nothing posts without your approval.

To turn on the extras, copy `lib/.env.example` to `lib/.env` and fill in only
the keys you want. `.env` is gitignored, so never commit real keys. To use the
helpers, install `lib/requirements.txt` and run Python with `PYTHONPATH=.claude`.

## Profile work so far

See `../instagram/raj_in_jp-profile.md`.
