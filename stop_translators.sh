# pkill -f translator_worker
ps -A | grep "translator_worker run" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
