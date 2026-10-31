#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
out="$root/dist"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

fail() {
  printf 'build_test: %s\n' "$*" >&2
  exit 1
}

"$root/scripts/build.sh"

find "$out" -type f -printf '%P\n' | sort >"$work/actual"
cat >"$work/expected" <<'EOF'
.nojekyll
assets/favicon.svg
assets/fonts/Geist-Variable.woff2
assets/fonts/GeistMono-Variable.woff2
assets/fonts/OFL.txt
assets/fonts/fonts.css
assets/paploo-mark.svg
assets/tokens.css
index.html
landing.mjs
styles.css
EOF
cmp -s "$work/expected" "$work/actual" || {
  diff -u "$work/expected" "$work/actual" >&2 || true
  fail "artifact file list drifted"
}

for file in index.html styles.css landing.mjs; do
  cmp -s "$root/$file" "$out/$file" || fail "$file drifted"
done
for file in favicon.svg paploo-mark.svg tokens.css; do
  cmp -s "$root/assets/$file" "$out/assets/$file" || fail "$file drifted"
done
for file in Geist-Variable.woff2 GeistMono-Variable.woff2 OFL.txt fonts.css; do
  cmp -s "$root/assets/fonts/$file" "$out/assets/fonts/$file" || fail "$file drifted"
done

if grep -Eq '(href|src)="/' "$out/index.html"; then
  fail "artifact contains a root-absolute resource or navigation path"
fi

(cd "$out" && find . -type f -print0 | sort -z | xargs -0 sha256sum) >"$work/first"
"$root/scripts/build.sh"
(cd "$out" && find . -type f -print0 | sort -z | xargs -0 sha256sum) >"$work/second"
cmp -s "$work/first" "$work/second" || fail "two builds produced different file hashes"

printf 'build_test: ok\n'
