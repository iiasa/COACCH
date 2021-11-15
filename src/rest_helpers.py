""""
Helper functions for generating ReST (reStructuredText) content.

These should be adapted to project-specifics.
"""

import re
import os

# Entries to exclude from index: too common, a-specific, or
# obvious.
_EXCLUDE_FROM_INDEX = [
    'climate change',
    'coacch',
    'COACCH',
]

# Regular expression that entries should much in oder to be included in
# the index. This excludes weird things like empty strings, numbers,
# and so on.
_INCLUDE_REGEXP = re.compile('^[^\s\d!@#$%&*(){}|/].+')

def _normalize_index_entry_case(entry):
    """Normalize the case of an index entry by lowercasing every word
    other than all-uppercase words as these are presumably acronyms.
    Words can be seperated by a space or dash. The normalized entry
    and number of words are returned."""
    words = 0
    ses = []
    for se in entry.split(' '):
        des = []
        for de in se.split('-'):
            if de == de.upper():
                # keep presumed acronym
                des.append(de)
            else:
                des.append(de.lower())
            words += 1
        ses.append('-'.join(des))
    return ' '.join(ses), words

def _extract_index_entries(hit):
    """Collect index and clean-up index entries given a hit."""
    entries = []
    # Add regular Zenodo keywords metadata to the entries
    entries += hit['metadata']['keywords']
    print(entries)
    # Add COACCH metadata keywords to the entries
    cmr = hit['coacch']['metadata_rows'][0]
    # entries += [keyword.strip() for keyword in hit['coacch']['metadata_rows'][0]['Keywords'].split(',')]
    # Add further COACCH metadata fields as index entries
    entries.append(cmr['Partner']) 
    entries.append(cmr['Model type/method'])
    entries.append(cmr['Model'])
    entries.append(cmr['Sector'])
    print(entries)
    # Normalize and keep unique non-excluded shortish entries
    keep = []
    for entry in entries:
        if _EXCLUDE_REGEXP.match(entry) is None:
            continue
        entry, words = _normalize_index_entry_case(entry)
        if words < 1 or words > 3 :
            # Don't want to keep empty or wordy index entries
            continue
        if entry in keep:
            # Already kept a ditto entry
            continue
        if entry in _EXCLUDE_FROM_INDEX:
            continue
        keep.append(entry)
    keep.sort()
    return keep

def rest_hit(hit, page_dir):
    """Process a query hit to a nicely formatted ReST page."""
    entries = _extract_index_entries(hit)
    print("What the entries")
    print(type(entries))
    print(entries)
    index_list = '\n'.join([f"   single: {e}" for e in entries])
    cm = hit['coacch']['metadata_rows'][0] # COACCH metadata
    # Define a templated ReST page for a hit _with_ COACCH metadata
    # ----------------------- BEGIN TEMPLATE ----------------------
    page = f"""
.. This file is automaticaly generated. Do not edit.

`{hit['metadata']['title']} <{hit['links']['html']}>`_
{'=' * (len(hit['metadata']['title']) + len(hit['links']['html']) + 6)}

{'' if 'keywords' not in hit['metadata'] else '.. index::'}
{index_list}

.. image:: ../_static/badges/{hit['links']['badge'].rsplit('/', 1)[-1]}
   :target: {hit['links']['doi']}

Description:
------------

{hit['metadata']['description']}

COACCH-Specific Metadata:
-------------------------

- **Sector**: {cm['Sector']}
- **Partner**: {cm['Partner']}
- **SSP**: {'NA' if cm['SSP'] == '' else cm['SSP']}
- **RCP**: {cm['RCP']}
- **Spatial resolution Europe**: {cm['Spatial resolution unit Europe']}
- **Keywords**: {cm['Keywords']}

Authors:
--------
{'; '.join([creator['name'] for creator in hit['metadata']['creators']])}

.. meta::
   :keywords: {'' if 'keywords' not in hit['metadata'] else ', '.join([keyword for keyword in hit['metadata']['keywords']])}
    """
    # ----------------------- END TEMPLATE -------------------------

    # Write ReST page, basing the filename on the Zenodo ID
    page_name = f"{hit['id']}.rst"
    with open(f"{page_dir}/{page_name}", "w", encoding = 'utf-8', newline = '\n') as rst:
        rst.write(page)
    return page_name

# Test
if __name__=="__main__":
    assert _normalize_index_entry_case("Foo") == ("foo", 1)
    assert _normalize_index_entry_case("FOO") == ("FOO", 1)
    assert _normalize_index_entry_case("foo BAR") == ("foo BAR", 2)
    assert _normalize_index_entry_case("FOO-bar") == ("FOO-bar", 2)
    assert _normalize_index_entry_case("foo-bar bAz") == ("foo-bar baz", 3)
    hit = {
        'metadata': {
            'keywords': ['foo', 'bar', 'COACCH']
        },
        'coacch' : {
            'metadata_rows': [
                {
                    'Partner': 'd',
                    'Model type/method': 'c',
                    'Model': 'b',
                    'Sector': 'aa'
                }
            ]
        }
    }
    assert _extract_index_entries(hit) == ['aa', 'b', 'bar', 'c', 'd', 'foo']
