# Helper functions for generating ReST (reStructuredText) content.
#
# These should be adapted to project-specifics.

import os

# Lowercase versions of keywords/phrases to exclude from the index
_EXCLUDE_FROM_INDEX = [
    'coacch',
    'climate change',
]

def _extract_index_entries(hit):
    """Collect index and clean-up index entries given a hit."""
    entries = []
    # Add regular Zenodo keywords metadata to the entries
    entries += hit['metadata']['keywords']
    # Add COACCH metadata keywords to the entries
    entries += [keyword.strip() for keyword in hit['coacch']['metadata_rows'][0]['Keywords'].split(',')]
    # Retain unique non-exluded shortish entries case-independently
    low_keep = []
    keep = []
    for entry in entries:
        low_entry = entry.lower()
        if low_entry in low_keep:
            continue
        if low_entry in _EXCLUDE_FROM_INDEX:
            continue
        if len(entry.split(" ")) > 3:
            continue
        low_keep.append(low_entry)
        keep.append(entry)
    entries = keep
    # Lower the case of non-acronym or multi-word entries
    for i,entry in enumerate(entries):
        if entry != entry.upper() or len(entry.split(" ")) > 1:
            entries[i] = entry.lower()
    return entries

def rest_hit(hit, zenodo_type='dataset'):
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

.. image:: {hit['links']['badge']}
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

    # Make sure that the output directory for the pages exists
    output_dir = f"../docs/{zenodo_type}s"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write ReST page, basing the filename on the Zenodo ID   
    with open(f"{output_dir}/{hit['id']}.rst", "w", encoding = 'utf-8', newline = '\n') as rst:
        rst.write(page)
    return hit['id']
