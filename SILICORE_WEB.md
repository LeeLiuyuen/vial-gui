# Silicore Vial Web

This public fork keeps Vial's GPL-2.0-or-later licensing and upstream history. The
`codex/silicore-web` branch adds a Silicore web theme, IBM Plex Sans typography,
and English, Spanish, French, German, Korean, Japanese, Simplified Chinese, and
Traditional Chinese user-interface translations.

The `Silicore Vial Web` GitHub Actions workflow builds the web runtime from:

- Vial GUI: this repository at the workflow commit
- Vial Web: `3749f8dabc6d186f9b17cb75eed64e6bf0e23e16`
- VIA support data: `3bcf423c970300722a04113de1d20c901b177e42`

The artifact includes the hashed JavaScript, data, WebAssembly, worker files, and
a SHA-256 manifest. No pull request or other write is made to the upstream Vial
repository.

## Fonts

IBM Plex Sans is distributed under the SIL Open Font License. Locale-specific
Japanese, Korean, Simplified Chinese, and Traditional Chinese subsets come from
IBM Plex Sans JP/KR/SC/TC. The original license text is in
`src/main/python/assets/fonts/`.

Font source revisions used to generate the committed subsets:

- IBM Plex: `bf260093582f04622aacc1e9f9ca604d7ccd0c42`
Regenerate them with `util/subset_silicore_fonts.py` and FontTools 4.62.1.

## License and source

Vial and the Silicore modifications are licensed under GPL-2.0-or-later; see
`COPYING`. The font files remain under their included SIL Open Font License.
Corresponding source is this public repository, including the exact build
workflow and pinned dependency revisions.
