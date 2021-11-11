# Helper functions for generating ReST (reStructuredText) content.
#
# These should be adapted to project-specifics.

import os

# Entries to exclude from index: too common, a-specific, or
# obvious.
_EXCLUDE_FROM_INDEX = [
    'COACCH',
    'coacch',
    'climate change',
]

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
    # Add COACCH metadata keywords to the entries
    entries += [keyword.strip() for keyword in hit['coacch']['metadata_rows'][0]['Keywords'].split(',')]
    # Normalize and retain unique non-excluded shortish entries
    keep = []
    for entry in entries:
        entry, words = _normalize_index_entry_case(entry)
        if words < 1 or words > 3 :
            # Don't want empty or wordy index entries
            continue
        if entry in keep:
            # Already have this entry
            continue
        if entry in _EXCLUDE_FROM_INDEX:
            # Blacklisted
            continue
        keep.append(entry)
    return keep

def rest_hit(hit, page_dir):
    """Process a query hit to a nicely formatted ReST page."""
    entries = _extract_index_entries(hit)
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
