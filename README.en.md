<p align="center"><img src="docs/hero.svg" alt="Idea Validator: Before you build, find the evidence" width="100%"></p>

# Idea Validator

**Is your idea worth your next month? Start with evidence.**

[中文](README.md) · [Real research example (Chinese)](examples/video-feedback/report.zh-CN.md) · [Releases](https://github.com/ziho7/idea-validator/releases)

An open-source Agent Skill that investigates product ideas through real complaints,
workarounds, existing alternatives, and counterevidence. It produces a cited decision
and a concrete next experiment. Problem existence, solution effectiveness and actual
purchase behavior are assessed separately.

## Install and use

Ask Codex:

```text
Use $skill-installer to install the idea-validator skill from the root of
https://github.com/ziho7/idea-validator at version v0.1.0.
```

Or install manually on macOS/Linux (Git required; destination must not exist):

```bash
mkdir -p "$HOME/.agents/skills"
git clone --branch v0.1.0 --depth 1 \
  https://github.com/ziho7/idea-validator.git \
  "$HOME/.agents/skills/idea-validator"
```

The user-level directory follows the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).
Restart Codex if the skill does not appear. Project-local installation can use
`.agents/skills/idea-validator/`; avoid duplicate copies with the same skill name.

```text
Use $idea-validator to investigate a tool for freelance video editors that
consolidates client feedback from email and chat into revision tasks.
Focus on English-speaking users, real workarounds, existing alternatives,
and evidence of spending. Actively look for counterevidence.
```

The skill answers in your language. A one-sentence idea is enough; consequential
assumptions are stated and only material missing information triggers questions.

## What you get

- A decision: test a small experiment, narrow/change the idea, defer, or insufficient evidence.
- Linked evidence with dates, short excerpts, segment fit and access limitations.
- Pain clusters and observed workarounds, separated from analyst inference.
- Current alternatives and counterevidence that could change the decision.
- A low-cost experiment with observable behavior and proposed decision criteria.
- Optional structured JSON evidence and a dependency-free consistency validator.

## How it works

```text
Idea → falsifiable hypotheses → pain + counter-queries → original sources
     → evidence ledger → deduplication + alternative checks → decision + experiment
```

The host agent performs search/retrieval and reasoning. This package provides the
workflow, source-selection guidance, evidence contract, report template and local
validation code. It contains no scraper, platform API integration or credentials.

Candidate sources include Reddit, Hacker News, GitHub Issues, specialist forums,
Stack Exchange, app stores, G2/Capterra/Trustpilot, V2EX/Zhihu/Xiaohongshu, X and official
product documentation. These are research destinations, not guaranteed connectors.
Choose sources for the target audience; disclose inaccessible pages and source bias.
[Full source map and query patterns](references/search-playbook.md).

Search snippets remain leads. Promotional posts are flagged. Same-thread replies are
not automatically independent users. Official documentation establishes advertised
features, not customer demand. Unknown dates or payment behavior remain unknown.

| Mode | Query ceiling | Page-open ceiling |
| --- | ---: | ---: |
| Quick | 12 | 15 |
| Standard (default) | 24 | 30 |
| Deep | 40 | 50 |

Caps include failures and are not evidence quotas, accuracy thresholds or time guarantees.
Research stops at the cap or after two expansion rounds without material new evidence;
the actual reason is disclosed. User-specified budgets and supplied-only research are supported.

## A real example

A bounded study on 2026-10-10 examined cross-channel feedback for freelance editors.
Public discussions showed fragmented communication and difficulty getting clients to
use review tools. Current Frame.io documentation already described timestamped comments,
completion status and exports. The recommendation was to test a narrower cross-channel
intake service while preserving client habits. Payment for the proposed product remained
unverified. See the [cited report](examples/video-feedback/report.zh-CN.md) and
[ledger](examples/video-feedback/evidence.json).

Seven source pages are not seven validated customers. The report explicitly records
promotional content, older evidence, uncertain dates and imperfect target-segment fit.
This is a development example, not an effectiveness benchmark.

## Requirements and validation

A skill-capable host with web search and original-page retrieval is needed for live
research. Without browsing, the skill can analyze supplied material or prepare a plan,
but must disclose the limitation. Python 3.10+ is needed only for the optional validator;
there are no third-party Python dependencies.

```bash
python3 scripts/validate_evidence.py examples/video-feedback/evidence.json
python3 -m unittest discover -s tests -v
```

Validation checks field types, dates, IDs, hypothesis references, unverified-lead handling
and required behavior for spending claims. Duplicate URLs and absent counter-search
produce warnings. It does not verify web content, identity independence or conclusions.
Exit codes: 0 structurally valid (warnings possible), 1 invalid data, 2 unreadable file/JSON.

Read [evidence rules](references/evidence-rules.md), [report template](references/report-template.md)
and [quality-check scope](docs/quality.md). CI checks the validator and real-example ledger.

## Boundaries

Public discussion is a self-selected sample: no market-size extrapolation or invented
success probability. Research is read-only by default. Posting, messaging, recruitment,
purchases and external publication require user authorization. No access-control bypasses.

The core SKILL.md is portable to compatible hosts, but v0.1.0 installation guidance is
for Codex. Other hosts' discovery and tool integrations have not been certified.

Contributions are welcome: provide an anonymized idea, executed searches, source links
and a specific unsupported inference. Preserve dates and limitations in example updates.

[MIT](LICENSE) for original code, documentation and design. Third-party excerpts and
trademarks remain with their respective owners; links imply no affiliation or endorsement.
