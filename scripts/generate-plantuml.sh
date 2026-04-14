#!/usr/bin/env bash
set -e

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.puml$' || true); do
  echo "Generating SVG for $file"
  java -Dplantuml.allowincludeurl=true -jar "$HOME/.local/share/plantuml/plantuml.jar" -tsvg "$file"
  svg_file="${file%.puml}.svg"
  git add "$svg_file"
done
