ps -A | grep "translator_worker_anvil" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
