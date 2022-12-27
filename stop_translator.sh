ps -A | grep "translator run --port=5000" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
