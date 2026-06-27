Output demos/demo.gif
Set Shell "bash"
Set FontSize 18
Set Width 1280
Set Height 720
Set Theme "Catppuccin Mocha"
Set TypingSpeed 48ms

Type "# Heavy Coder · council + swarm_watch" Enter
Sleep 500ms
Type "cat demos/vhs/assets/install-transcript.txt" Enter
Sleep 2s

Hide
Type "bash -lc 'source demos/vhs/env.sh && ./demos/vhs/bin/show-team-plan.sh'" Enter
Sleep 4s
Show

Hide
Type "bash demos/vhs/bin/animate-swarm.sh" Enter
Sleep 14s
Show

Type "cat demos/vhs/assets/coordinator-excerpt.txt" Enter
Sleep 3s

Hide
Type "bash -lc 'source demos/vhs/env.sh && python3 -m pytest tests/test_swarm_progress.py -q'" Enter
Sleep 4s
Show