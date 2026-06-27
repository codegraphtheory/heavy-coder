Output demos/vhs/out/02-council-plan.mp4
Set Shell "bash"
Set FontSize 22
Set Width 1920
Set Height 1080
Set Theme "Catppuccin Mocha"
Set TypingSpeed 40ms

Type "# Council plan JSON (team_coordinator.py)" Enter
Sleep 600ms

Hide
Type "source demos/vhs/sanitize-recording-env.sh" Enter
Sleep 300ms
Type "bash demos/vhs/bin/show-team-plan.sh" Enter
Sleep 4s
Show

Type "# Hooks inject DELEGATE_TASKS_JSON · coordinator dispatches one batch" Enter
Sleep 1.2s
