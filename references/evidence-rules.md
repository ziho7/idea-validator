# Evidence rules and JSON contract

## Interpretation

Separate observations, source self-reports and analyst inference. A forum claim of
spending is a self-report, not a verified transaction. A competitor's paying customers
do not prove willingness to buy this proposed product.

Behavior can carry more decision value than enthusiasm, but there is no universal
numeric ladder. A recurring pain may strongly support problem reality without
supporting adoption. Judge directness, target fit, independence, recency, coverage and
contradictions separately; explain confidence instead of calculating a post-count score.

- Low: snippets, thin context, unclear segment, promotion-heavy sample or key unknowns.
- Medium: detailed relevant experiences with limited diversity or unresolved conflicts.
- High: direct, independent, matched evidence converges after active counter-search.
  Confidence applies to the specific claim, never automatically to profitability.

Use supported, mixed, contradicted or unknown for hypotheses in the report.

## Independence and roles

Group threads, cross-posts, repeated authors and shared incidents when dependencies
are known. Do not count replies as independent experiences without grounds. Report
pages separately from people; say when identity independence is uncertain.

Flag founder research, affiliate content and promotion. Vendor material can establish
advertised features, not customer validation. Retain contradictory reports and check
segment/plan/version/time differences. Quotes must be short, exact, original-language;
label translations as paraphrases and respect tool/source quotation limits.

## File contract v1

This JSON contract is for web-source ledgers with real original URLs. For supplied-only
notes without URLs, use a clearly labeled table instead. Such notes can conditionally
support a hypothesis within the supplied account, but are not independently verified
original-source evidence. Synthetic material is never real market evidence. Do not
invent URLs or misclassify supplied notes as inspected pages just to export JSON.

Use UTF-8 JSON. Unknown values are null, never invented zeros, dates or payment amounts.
Inline tables need equivalent information, not JSON syntax.

| Root field | Meaning |
| --- | --- |
| `schema_version` | Integer `1` |
| `idea` | Nonempty string |
| `research_date` | Actual retrieval date, `YYYY-MM-DD` |
| `mode` | `quick`, `standard`, `deep`, `custom` |
| `hypotheses` | Array of `{id, statement}`, e.g. H1 |
| `search_log` | Array of `{query, purpose, outcome}`; purpose: `support`, `counter`, `alternatives`, `context` |
| `evidence` | Array of records below; may be empty if nothing accessible |
| `limitations` | Array of strings, including scope limits and stop reason |

Required evidence fields:

| Field | Type / meaning |
| --- | --- |
| `id` | Unique nonempty string, e.g. E1 |
| `url` | Original HTTP(S) page/comment URL |
| `title`, `platform` | Nonempty strings |
| `source_type` | `user_discussion`, `user_review`, `issue`, `vendor_documentation`, `promotion`, `other` |
| `published_at` | Exact `YYYY-MM-DD` if known; otherwise null |
| `retrieved_at` | Exact `YYYY-MM-DD` |
| `access` | `full`, `partial`, `snippet`, `unavailable` |
| `excerpt` | Short exact quote or null; null for snippet/unavailable records |
| `summary` | Nonempty claim-specific paraphrase; label inference |
| `segment` | Target fit and unknown attributes |
| `identity_basis` | `self_reported`, `inferred`, `unknown` |
| `behavior` | Reported action, or null |
| `payment_signal` | `reported_spend`, `stated_intent`, `inferred`, `none`, `unknown` |
| `stance` | `supports`, `contradicts`, `mixed`, `context` |
| `hypothesis_ids` | Nonempty array of existing hypothesis IDs |
| `independence_group` | Nonempty grouping key, e.g. reddit-thread-abc |
| `limitations` | Array of strings |

Optional: `pain`, `frequency`, `cost`, `workaround`, `updated_at`, `author_reference`,
`quote_locator`. Keep public identity only as necessary for deduplication; do not add
private profiles or contact details to a public ledger.

Snippet/unavailable records are leads and require `stance: context`. They do not count
as verified user experiences. `reported_spend` must have a described behavior; vendor
pricing alone is not spending. `none` means no payment signal in the inspected material,
not proof that the person refuses to pay. Missing information is `unknown`.

The validator checks fields, types, IDs, date formats, references and lead handling;
it warns about repeated URLs and missing counter-search. It cannot verify webpage
truth, judge whether authors are independent or certify a decision. See the explicitly
synthetic fixture in `tests/fixtures/synthetic-ledger.json` for a complete valid file.
