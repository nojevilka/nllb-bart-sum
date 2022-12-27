ps -A | grep "back_translator run --port=6000" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
