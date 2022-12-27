ps -A | grep "summarizer_fb_bart run --port=5200" | grep -v "grep" | awk '{print $1;}' | xargs -I {} kill {}
