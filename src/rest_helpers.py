# Helper functions for generating ReST (reStructuredText) content.
#
# These should be adapted to project-specifics.

import os

def rest_hit(hit, zenodo_type='dataset'):
    """
    Process a query hit and generate a ReST page.
    """
    if 'coacch' in hit and 'metadata_rows' in hit['coacch']:
        cm = hit['coacch']['metadata_rows'][0]
        if 'keywords' in hit['metadata']:
            # Compile a cleaned-up list of single index entries from the keywords
            index_list = []
            for keyword in hit['metadata']['keywords']:
                if keyword.lower() in ['coacch', 'climate change']:
                    # Exclude listed keywords
                    continue
                if keyword != keyword.upper():
                    # Not all uppercase, not an acronym
                    if len(keyword.split(" ")) > 3:
                        # It's a long story, don't index.
                        continue
                    # Lower leading caps and mixed case
                    keyword = keyword.lower()
                # Add to index
                index_list.append(f"   single: {keyword}")
            index_list = '\n'.join(index_list)
        else:
            index_list = ''
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
    else:
        raise Exception(f"Cannot generate ReST, no COACCH metadata for hit {hit['id']}!")
    # Make sure that the output directory for the pages exists
    output_dir = f"../docs/{zenodo_type}s"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Write ReST page, basing the filename on the Zenodo ID   
    with open(f"{output_dir}/{hit['id']}.rst", "w", encoding = 'utf-8', newline = '\n') as rst:
        rst.write(page)
    return hit['id']