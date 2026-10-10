# Search playbook

## Query construction

Translate an idea into a situation before naming the solution. “AI for client
feedback” becomes missing revisions, scattered emails, conflicting notes, version
confusion and clients ignoring review links. Product labels often find founders
and competitors rather than customers.

| Intent | English patterns | 中文模式 |
| --- | --- | --- |
| Pain | `"[task]" "frustrating"`, `"[task]" "takes hours"` | `[任务] 太麻烦`, `[场景] 浪费时间` |
| Consequence | `"[task]" "missed"`, `"[workflow]" "rework"` | `[任务] 漏掉`, `[流程] 返工` |
| Help | `"how do you" "[task]"`, `"[task]" "recommend"` | `[任务] 大家怎么做`, `[场景] 求推荐` |
| Workaround | `"[task]" "spreadsheet"`, `"[task]" "manually"` | `[任务] 手动`, `[任务] Excel` |
| Switching | `"[competitor]" "alternative"`, `"[competitor]" "cancelled"` | `[竞品] 替代`, `[竞品] 退订` |
| Spending | `"[task]" "pay for"`, `"[task]" "hired"` | `[任务] 付费`, `[任务] 外包` |
| Counterevidence | `"[competitor]" "works well"`, `"[task]" "don't need"` | `[竞品] 够用`, `[任务] 没必要` |

Use site filters where useful, e.g. `site:reddit.com/r/editors "client feedback"`.
Start broad to learn vocabulary, then focus on relevant communities. Adapt phrasing;
do not mechanically expand every cell. Log only executed queries.

## Source map

Candidate sources, not bundled connectors or guaranteed accessible feeds:

| Source | Useful signal | Limitation |
| --- | --- | --- |
| [Reddit](https://www.reddit.com/) | Situations, workarounds, help and alternatives | Audience bias, self-promotion, access limits; popularity is not prevalence |
| [Hacker News](https://news.ycombinator.com/) | Technical buyer discussion, Ask HN experiences | Strong technical/startup audience bias |
| [GitHub Issues](https://github.com/) | Reproducible friction, workflow gaps | Requests can be niche; check whether closed issues were fixed |
| [Stack Exchange](https://stackexchange.com/) / vendor forums | Detailed constraints and resolutions | Read answers and check versions/dates |
| [G2](https://www.g2.com/), [Capterra](https://www.capterra.com/), [Trustpilot](https://www.trustpilot.com/) | Usage complaints, migration context | Incentivized/unverified reviews and unclear buyer identity |
| [App Store](https://apps.apple.com/), [Google Play](https://play.google.com/store/apps) | Friction and version history | Rating bias, region/version differences, indexing limits |
| [V2EX](https://www.v2ex.com/), [知乎](https://www.zhihu.com/), [小红书](https://www.xiaohongshu.com/) | Chinese workflows, vocabulary and context | Login/indexing limits, promotion, nonrepresentative samples |
| [X](https://x.com/) / public communities | New complaints, recommendations, switching | Viral duplication and thin context; private groups require authorized access |
| Official docs, changelogs, pricing | Current features and plan constraints | Vendor claims do not establish demand, satisfaction or actual outcomes |

Select by customer presence, not platform prestige. English Reddit data for a Chinese
consumer product is adjacent context, not proof of local demand. For B2B, separate
operator frustration from the buyer's purchase criteria.

## Research rounds

1. Discover task, consequences and workarounds; learn users' vocabulary.
2. Focus on relevant pain/segment combinations.
3. Challenge with satisfied users, cheaper alternatives, resolved issues and adoption
   barriers. Inspect current official docs for consequential feature claims.
4. Resolve contradictions that could change the decision with the remaining budget.

Interleave counterevidence; this is a guide, not a forced sequence. Do not claim
saturation if the actual reason was a cap or blocked access.

## Access and date handling

- Missing post text cannot be inferred from a headline or snippet. Mark leads clearly.
- A rendered page can be partial; record what relevant content was actually visible.
- Prefer comment permalinks. Otherwise locate the comment by date/context and retain
  the same thread independence group.
- Check whether old complaints still apply through changelogs and responses.
- Unknown dates stay null; record relative dates as uncertain text rather than inventing
  an exact day. Do not use a crawl date as the publication date.
- After one normal retry, record unavailable sources and move on; no access bypasses.
- If one source family dominates, disclose it rather than padding with irrelevant sites.
