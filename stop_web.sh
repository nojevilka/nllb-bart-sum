ps -A | grep "main run --port=5100" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
