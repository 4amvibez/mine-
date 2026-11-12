# Claude setup: plugins, skills and connectors

All of these are public plugins (from GitHub or the official Claude plugin directory). Nothing private is included.

---

## Option A: Claude Code (terminal). Copy and paste

Paste these lines into Claude Code one at a time. Each `marketplace add` line adds a GitHub repo, and the `install` line after it installs the plugin from that repo.
If an install line fails because the marketplace name is different, run `/plugin` and pick the plugin from the menu.

### 1. Anthropic official skills (Word/Excel/PPT/PDF, example skills, Claude API)
```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
/plugin install claude-api@anthropic-agent-skills
```

### 2. Video, film and reels
```
/plugin marketplace add bradautomates/claude-video
/plugin install watch@claude-video

/plugin marketplace add lemomo-ai/lemo-opuscar
/plugin install lemo-opuscar@lemo-opuscar

/plugin marketplace add MarcinSufa/claude-watch-video
/plugin marketplace add itpartypattaya/reels-montage
/plugin marketplace add i-afaqrashid/claude-animation-studio
/plugin marketplace add ClipWave-io/clipwave-plugins
/plugin marketplace add abracadabrax-app/claude-plugins
```
(The last five repos contain: watch-video, it-reelsmaker, animation-studio, anime-story-video + logo-maker + clipwave-video-image-maker, and the abracadabrax image/video/music generators. Run `/plugin` and install the ones you want.)

### 3. UI / UX / website design
```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

/plugin marketplace add uxkin/agent
/plugin marketplace add superdesigndev/superdesign-skill
/plugin marketplace add enoevol81/enoevol-plugins
/plugin marketplace add bryntay/a1-mcp
/plugin marketplace add iboss21/animatedwebs-claude
/plugin marketplace add umairalisadaqat/weinc-claude-plugin
/plugin marketplace add europetechnologie/seo-records-website-checkup
```
(These repos contain: website-design, superdesign, design-steward, a1-gallery, animatedwebs, weinc and seo-records-website-checkup.)

### 4. Social media, Instagram, ads
```
/plugin marketplace add ayrshare/ayrshare-social-media-api-claude-plugin
/plugin marketplace add gitroomhq/postiz-agent
/plugin marketplace add mesmerlord/admakeai-claude-plugin
/plugin marketplace add canva-sdks/canva-skills
```

### 5. Dev, backend, data, slides
```
/plugin marketplace add sheitabrk/backend-design
/plugin marketplace add neondatabase/agent-skills
/plugin marketplace add brightdata/skills
/plugin marketplace add Atomic-man007/pptx-deck-plugin
```

### 6. From the official Claude plugin directory (no repo to add)
```
/plugin install frontend-design@claude-plugins-official
/plugin install firebase@claude-plugins-official
/plugin install design@claude-plugins-official
/plugin install diagrams@claude-plugins-official
```
(If a name isn't found, run `/plugin` → Discover and search for it.)

---

## Option B: claude.ai (website or app)

Go to **Settings → Plugins/Customize → Browse plugins**, search for these names and click Install:

watch, lemo-opuscar, document-skills, example-skills, claude-api, ui-ux-pro-max, website-design, superdesign, design-steward, frontend-design, design, a1-gallery, animatedwebs, weinc, seo-records-website-checkup, watch-video, it-reelsmaker, animation-studio, anime-story-video, logo-maker, clipwave-video-image-maker, abracadabrax-ai-video-generator, abracadabrax-image-video, abracadabrax-background-music-generator, admakeai, ayrshare, postiz, canva, backend-design, neon, firebase, brightdata-plugin, diagrams, pptx-deck

For plugins that aren't listed there, add the GitHub repo (`owner/repo` from the Claude Code section above) as a custom marketplace.

---

## Connectors (claude.ai → Settings → Connectors → Browse)

These don't have GitHub repos. Search for each name and click Connect, then sign in with your own account:

- **Apify**: Instagram/web scraping
- **Canva**
- **ElevenLabs**: voice and AI media
- **Fish Audio**: voice / text to speech
- **Higgsfield**: AI image and video
- **Publora**: schedule social posts
- **Google Drive**
- **Vercel**: deploy websites
- **PPT Depot**: PowerPoint templates (no login needed)
- **PoweredTemplate**: templates (no login needed)
- Optional: Gmail, Google Calendar, Neon

---

## Repo list only (to star or browse)

```
https://github.com/anthropics/skills
https://github.com/bradautomates/claude-video
https://github.com/lemomo-ai/lemo-opuscar
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
https://github.com/MarcinSufa/claude-watch-video
https://github.com/itpartypattaya/reels-montage
https://github.com/i-afaqrashid/claude-animation-studio
https://github.com/ClipWave-io/clipwave-plugins
https://github.com/abracadabrax-app/claude-plugins
https://github.com/uxkin/agent
https://github.com/superdesigndev/superdesign-skill
https://github.com/enoevol81/enoevol-plugins
https://github.com/bryntay/a1-mcp
https://github.com/iboss21/animatedwebs-claude
https://github.com/umairalisadaqat/weinc-claude-plugin
https://github.com/europetechnologie/seo-records-website-checkup
https://github.com/ayrshare/ayrshare-social-media-api-claude-plugin
https://github.com/gitroomhq/postiz-agent
https://github.com/mesmerlord/admakeai-claude-plugin
https://github.com/canva-sdks/canva-skills
https://github.com/sheitabrk/backend-design
https://github.com/neondatabase/agent-skills
https://github.com/brightdata/skills
https://github.com/Atomic-man007/pptx-deck-plugin
```
