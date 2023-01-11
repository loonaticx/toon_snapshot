## User editable portion of the snapshot config ##
snapshot-debug 0

# Server
snapshot-host localhost
snapshot-port 20151
# Sets window-type to offscreen
snapshot-headless 1

# Process
snapshot-res 1024
snapshot-extension .png
snapshot-dir out
snapshot-prefix render_

# Post-process
snapshot-trim-whitespace 1

# If false, renders will be deleted from the disk after a certain amount of time.
snapshot-keep-renders 0
# if we're not keeping renders, images after this amount of seconds will be deleted.
snapshot-cleanup-time 60

# Discord
snapshot-discord-token unknown

# Change this if you want the bot to only work in a particular guild.
# none means it'll run on any guild it's in.
snapshot-discord-guild none
