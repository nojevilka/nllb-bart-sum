ps -A | grep "back_translator_worker" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
