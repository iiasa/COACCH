![docs_pages_workflow](https://github.com/iiasa/COACCH/workflows/docs_pages_workflow/badge.svg?branch=master)

# Data Reposity content for COACCH

The `master` branch of this repository holds content and content generation scripts for the [COACCH Data Repository website](https://coacch.iiasa.ac.at). The content is defined in [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) markup format and converted using [Sphinx](https://www.sphinx-doc.org/) to HTML. The Sphinx conversion is automated using GitHub Actions. The HTML is stored in the `gh-pages` branch and thereafter automatically displayed via GitHub Pages on the website.

The content for the data sets reflects [COACCH](https://www.coacch.eu/) dataset uploads to [Zenodo](https://zenodo.org/). These data sets are collected by querying the [Zenodo REST API](https://developers.zenodo.org/).

For more information, see this article

 * https://tech.michaelaltfield.net/2020/07/18/sphinx-rtd-github-pages-1/

# License

The contents of this repo are dual-licensed. All code is GPLv3 and all other content is CC-BY-SA.
