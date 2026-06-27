Output demos/vhs/out/04-ship-gate.mp4
Set Shell "bash"
Set FontSize 22
Set Width 1920
Set Height 1080
Set Theme "Catppuccin Mocha"
Set TypingSpeed 45ms

Type "# Coordinator after batch (staged excerpt)" Enter
Sleep 500ms
Type "cat demos/vhs/assets/coordinator-excerpt.txt" Enter
Sleep 2.5s

Hide
Type "bash -lc 'source demos/vhs/env.sh && python3 -m pytest tests/test_swarm_progress.py -q'" Enter
Sleep 5s
Show

Type "# Launch edit: cut 01-04 in your NLE · add music and titles" Enter
Sleep 1.5s