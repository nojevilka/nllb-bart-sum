ps -A | grep "translator_anvil run --port=5400" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
