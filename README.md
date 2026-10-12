# OBS Deck

Turns a Steam Deck into a Stream Deck for OBS. It's a web page that talks to OBS over obs-websocket, which is built into OBS 28 and later.

## What it can do

**Buttons**
- **Mute / unmute** an audio source. A live level meter runs along the bottom. If you talk while muted, the button pulses.
- **Push-to-talk:** the mic is unmuted only while you hold the button (on screen or a bound controller button).
- **Volume sliders** (wide tiles) with a level meter and a mute button. The slider moves like OBS's own faders.
- **Switch scenes.** Scene buttons show a live preview of the scene. In Studio Mode they pick the preview scene and a **Transition** button takes it live (you can turn that off in Settings).
- **Show / hide** a source in a scene.
- **Turn a filter on / off** (noise suppression, voice changer, colour correction…).
- **Media control:** play/pause, restart, stop, next and previous for media and playlist sources.
- **Streaming, recording, pause recording, virtual camera, Studio Mode.**
- **Save replay buffer**, **screenshot** (saved to your recording folder), and **any OBS hotkey**.
- **Multi-action:** one button runs several steps in order (with "Wait" steps in between). Turn on *Tap again to undo* and a second tap puts everything back. For example, "BRB" switches to the BRB scene and mutes the mic, and tapping it again returns to your old scene and unmutes.

**Extras**
- **Pages:** as many pages of buttons as you like. Swipe left/right or use L1/R1 to switch (you can rebind those in Settings).
- **Stats bar:** live time, bitrate, dropped frames, CPU, FPS and remaining disk space, coloured when something looks wrong.
- **Timers** on the Stream and Record buttons.
- **Custom look:** colour, built-in icon, emoji, or your own image on any button.
- **Controller and keyboard bindings** for any button.
- Stopping a stream or recording needs **two taps**, so you can't end one by accident.

## 1. Set up OBS (on the PC)

1. In OBS, open **Tools → WebSocket Server Settings**.
2. Tick **Enable WebSocket server**. Leave the port at **4455**.
3. Click **Show Connect Info** and note the **Server Password**.

## 2. Start the server on the PC (recommended)

Double-click **`start-server.bat`**. You need Python 3, which you can get from python.org. The window shows an address like:

```
On the Steam Deck, open:  http://192.168.1.50:8080
```

If Windows Firewall asks, allow Python on **Private networks**. Keep the window open while you stream.

With the server:
- Your layout is saved on the PC in `layout.json`, so it survives clearing the browser and is shared by every device you open it on.
- The Deck finds OBS automatically. You only enter the password once.
- Changes to `index.html` reach the Deck when you reload the page. You never copy files again.

The server only sends the page and your layout. It never sends your OBS password anywhere.

*No server?* `index.html` also works on its own. Copy it to the Deck and open it, then enter the PC's IP, port and password in Settings. The layout is then kept in that browser only.

## 3. Open it on the Steam Deck

In Desktop Mode, open the address in a browser, open Settings, enter the OBS password, and tap **Connect**.

### Run it in Game Mode, fullscreen

1. In Desktop Mode, install **Google Chrome** from Discover.
2. Open Steam → **Games → Add a Non-Steam Game** → pick Google Chrome.
3. In that shortcut's **Properties**, add this to the end of the launch options (use your PC's address):
   ```
   --kiosk http://192.168.1.50:8080
   ```
4. Rename the shortcut to "OBS Deck". It now opens fullscreen from Game Mode.

## Editing

- Tap **Edit**, then tap a button to change it, or tap **+** to add one. Tap **Done** when you're finished.
- In Edit mode, **+ Page** adds a page. Tap the current page's tab again to rename, reorder or delete it.
- While you're connected, names of sources, scenes, filters and hotkeys are suggested as you type.
- **Settings → Add a button for every scene** fills the current page with scene buttons.
- **Bind…** links a button to a Deck control (A/B/X/Y, D-pad, bumpers, triggers) or a key. Bindings work from any page. To use the back paddles (L4/R4/L5/R5), map them to keyboard keys in the shortcut's Steam Input layout, then bind those keys.
- **Settings → Backup** shows the whole layout as text you can copy, paste back, and Import.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Can't reach OBS, retrying…" | Check the PC's IP, make sure the Deck and PC are on the same network, and allow OBS through Windows Firewall (Private networks). |
| "Wrong password" | Copy the password again from OBS → Tools → WebSocket Server Settings → Show Connect Info. |
| The Deck can't open the server address | Allow Python through Windows Firewall on Private networks, and check the PC's network is set to Private. |
| A button says "not found" | The name doesn't match OBS exactly. Edit the button and pick the name from the suggestions. |
| Replay button gives an error | Turn on the Replay Buffer in OBS (Settings → Output) and start it. |
| Transition button is dimmed | It only works while Studio Mode is on. |
