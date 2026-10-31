# Paploo project site

Static landing page for [Paploo](https://github.com/dagi377/paploo), built with dependency-free
HTML, CSS, and JavaScript. The published site is designed for GitHub Pages at
`https://dagi377.github.io/paploopage/`.

## Develop

```sh
make check
make preview
```

`make preview` builds the self-contained artifact in `dist/` and serves it at
`http://localhost:4173`.

## Structure

- `index.html`, `styles.css`, `landing.mjs`: page source and progressive enhancement
- `assets/`: Paploo's canonical mark, design tokens, and Geist font files
- `tests/`: document, interaction, and deterministic-artifact checks
- `scripts/build.sh`: stages the GitHub Pages artifact in `dist/`
- `.github/workflows/pages.yml`: SHA-pinned Pages deployment from `main`
