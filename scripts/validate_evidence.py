#!/usr/bin/env python3
"""Validate ledger structure and provenance consistency; never certify source truth."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ENUMS = {
    'source_type': {'user_discussion', 'user_review', 'issue', 'vendor_documentation', 'promotion', 'other'},
    'access': {'full', 'partial', 'snippet', 'unavailable'},
    'identity_basis': {'self_reported', 'inferred', 'unknown'},
    'payment_signal': {'reported_spend', 'stated_intent', 'inferred', 'none', 'unknown'},
    'stance': {'supports', 'contradicts', 'mixed', 'context'},
}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def string_list(value):
    return isinstance(value, list) and all(nonempty(item) for item in value)


def validate(data):
    """Return (errors, warnings). Accept incomplete research, but label its limits."""
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ['root must be an object'], warnings
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        errors.append('schema_version must be integer 1')
    if not nonempty(data.get('idea')):
        errors.append('idea must be a nonempty string')
    if not valid_date(data.get('research_date')):
        errors.append('research_date must be YYYY-MM-DD')
    if not isinstance(data.get('mode'), str) or data['mode'] not in {'quick', 'standard', 'deep', 'custom'}:
        errors.append('mode must be quick, standard, deep, or custom')
    if not string_list(data.get('limitations')):
        errors.append('limitations must be an array of nonempty strings')
    elif not data['limitations']:
        warnings.append('document coverage limits and the actual stopping reason')

    hypotheses = data.get('hypotheses')
    hypothesis_ids = set()
    if not isinstance(hypotheses, list) or not hypotheses:
        errors.append('hypotheses must be a nonempty array')
    else:
        for index, item in enumerate(hypotheses):
            label = f'hypotheses[{index}]'
            if not isinstance(item, dict):
                errors.append(f'{label} must be an object')
                continue
            ident = item.get('id')
            if not nonempty(ident):
                errors.append(f'{label}.id must be a nonempty string')
            elif ident in hypothesis_ids:
                errors.append(f'{label}: duplicate hypothesis id {ident}')
            else:
                hypothesis_ids.add(ident)
            if not nonempty(item.get('statement')):
                errors.append(f'{label}.statement must be a nonempty string')

    searches = data.get('search_log')
    counter_search = False
    if not isinstance(searches, list):
        errors.append('search_log must be an array')
    else:
        for index, item in enumerate(searches):
            label = f'search_log[{index}]'
            if not isinstance(item, dict):
                errors.append(f'{label} must be an object')
                continue
            for field in ('query', 'outcome'):
                if not nonempty(item.get(field)):
                    errors.append(f'{label}.{field} must be a nonempty string')
            purpose = item.get('purpose')
            if not isinstance(purpose, str) or purpose not in {'support', 'counter', 'alternatives', 'context'}:
                errors.append(f'{label}.purpose is invalid')
            elif purpose == 'counter':
                counter_search = True
        if not counter_search:
            warnings.append('no explicit counterevidence query recorded')

    records = data.get('evidence')
    if not isinstance(records, list):
        return errors + ['evidence must be an array'], warnings
    seen_ids, seen_urls = set(), {}
    verified = 0
    for index, record in enumerate(records):
        label = f'evidence[{index}]'
        if not isinstance(record, dict):
            errors.append(f'{label} must be an object')
            continue
        for field in ('id', 'url', 'title', 'platform', 'summary', 'segment', 'independence_group'):
            if not nonempty(record.get(field)):
                errors.append(f'{label}.{field} must be a nonempty string')
        ident = record.get('id')
        if nonempty(ident):
            if ident in seen_ids:
                errors.append(f'{label}: duplicate evidence id {ident}')
            seen_ids.add(ident)
        url = record.get('url')
        if nonempty(url):
            try:
                parsed = urlsplit(url)
                valid_url = parsed.scheme in {'http', 'https'} and bool(parsed.hostname)
            except ValueError:
                valid_url = False
            if not valid_url:
                errors.append(f'{label}.url must be an HTTP(S) URL with a host')
            elif url in seen_urls:
                warnings.append(f'{label}: repeated URL also used in {seen_urls[url]}; inspect independence')
            else:
                seen_urls[url] = label
        for field, choices in ENUMS.items():
            value = record.get(field)
            if not isinstance(value, str) or value not in choices:
                errors.append(f'{label}.{field} is invalid')
        for field in ('excerpt', 'behavior'):
            if field not in record or (record[field] is not None and not nonempty(record[field])):
                errors.append(f'{label}.{field} must be a nonempty string or null')
        if 'published_at' not in record or (record['published_at'] is not None and not valid_date(record['published_at'])):
            errors.append(f'{label}.published_at must be YYYY-MM-DD or null')
        if not valid_date(record.get('retrieved_at')):
            errors.append(f'{label}.retrieved_at must be YYYY-MM-DD')
        else:
            if valid_date(record.get('published_at')) and record['published_at'] > record['retrieved_at']:
                errors.append(f'{label}: publication date is after retrieval')
            if valid_date(data.get('research_date')) and record['retrieved_at'] > data['research_date']:
                errors.append(f'{label}: retrieval date is after research_date')
        if not string_list(record.get('limitations')):
            errors.append(f'{label}.limitations must be an array of nonempty strings')
        refs = record.get('hypothesis_ids')
        if not string_list(refs) or not refs:
            errors.append(f'{label}.hypothesis_ids must be a nonempty string array')
        else:
            for ref in refs:
                if ref not in hypothesis_ids:
                    errors.append(f'{label}: unknown hypothesis {ref}')
        if record.get('access') in ('snippet', 'unavailable'):
            if record.get('excerpt') is not None:
                errors.append(f'{label}: unverified lead cannot contain an original-source excerpt')
            if record.get('stance') != 'context':
                errors.append(f'{label}: unverified lead must use stance=context')
        elif record.get('access') in ('full', 'partial'):
            verified += 1
        if record.get('payment_signal') == 'reported_spend' and not nonempty(record.get('behavior')):
            errors.append(f'{label}: reported_spend requires a described behavior')
        if record.get('source_type') in ('promotion', 'vendor_documentation') and record.get('stance') == 'supports':
            warnings.append(f'{label}: interested source; do not treat it as independent customer validation')
    if not verified:
        warnings.append('no inspected original sources; do not claim completed demand validation')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'ERROR: cannot read ledger: {exc}', file=sys.stderr)
        return 2
    errors, warnings = validate(data)
    for warning in warnings:
        print(f'WARNING: {warning}')
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    if errors:
        return 1
    print(f'OK: {len(data["evidence"])} records structurally valid. Source truth and conclusions require review.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
