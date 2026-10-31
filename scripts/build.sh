#!/usr/bin/env bash
# Stage the dependency-free Paploo project site for GitHub Pages.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
out="$root/dist"

case "$out" in
  "$root/dist") ;;
  *) printf 'build: unsafe output path: %s\n' "$out" >&2; exit 1 ;;
esac

rm -rf -- "$out"
install -d "$out/assets/fonts"
install -m 0644 "$root/index.html" "$out/index.html"
install -m 0644 "$root/styles.css" "$out/styles.css"
install -m 0644 "$root/landing.mjs" "$out/landing.mjs"
install -m 0644 "$root/assets/paploo-mark.svg" "$out/assets/paploo-mark.svg"
install -m 0644 "$root/assets/favicon.svg" "$out/assets/favicon.svg"
install -m 0644 "$root/assets/tokens.css" "$out/assets/tokens.css"
for file in Geist-Variable.woff2 GeistMono-Variable.woff2 OFL.txt fonts.css; do
  install -m 0644 "$root/assets/fonts/$file" "$out/assets/fonts/$file"
done
: >"$out/.nojekyll"

printf 'build: wrote %s\n' "$out"
