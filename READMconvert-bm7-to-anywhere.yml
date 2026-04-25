name: Convert BM7 rules to Anywhere

on:
  workflow_dispatch:
  schedule:
    - cron: '23 3 * * *'

permissions:
  contents: write

jobs:
  convert:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout current repo
        uses: actions/checkout@v4

      - name: Checkout upstream ios_rule_script
        uses: actions/checkout@v4
        with:
          repository: blackmatrix7/ios_rule_script
          ref: master
          path: upstream

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Convert rules
        run: |
          python scripts/convert_bm7_to_anywhere.py \
            --input-root upstream/rule \
            --output-root anywhere-rules

      - name: Commit converted files
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add anywhere-rules
          if git diff --cached --quiet; then
            echo "No changes"
            exit 0
          fi
          git commit -m "chore: update Anywhere rules from blackmatrix7"
          git push
