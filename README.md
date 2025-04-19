# Sync music playlists between Rhythmbox (computer) and Phocid (mobile phone)

Fully synchronise your music playlists between Rhythmbox, on your computer, and Phocid (or Vanilla Music), on your mobile phone.

0. Run the following commands:

```
git clone https://github.com/neuralXray/sync-music-playlists.git
cd sync-music-playlists
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
chmod u+x sync.sh
touch sync.log
```

Note: With Phocid synchronisation is fully bidirectional: changes made to playlists on the phone are reflected on the computer and vice versa. However, with Vanilla Music changes made on the computer are not automatically imported on the phone. Although Vanilla Music has a playlist `Full synchronization` option, it doesn't work reliably, playlist files are not automatically imported on startup. One can manually delete and reimport playlists, or use the `Force M3U reimport` option, but its behaviour is inconsistent: sometimes it works, sometimes it doesn't. For fully automated synchronisation (with no user intervention) [Phocid](https://f-droid.org/en/packages/org.sunsetware.phocid/) is strongly recommended.

## Phocid

1. In Phocid, in the `Playlists` tab, open the `three-dot menu` and select the `Playlists sync` option. There you can choose which playlists to sync, their target file names and the parent directory location where they are stored.

2. Use Syncthing to synchronise `/home/<username>/.local/share/rhythmbox/` on your computer with the selected parent directory location of your Phocid playlists on your phone.


## Vanilla Music

1. In Vanilla Music: `Settings > Playlists > Playlists Synchronization`, select `Full synchronization`.

2. Use Syncthing to synchronise `/home/<username>/.local/share/rhythmbox/` on your computer with `storage/emulated/0/Android/media/ch.blinkenlights.android.vanilla/Playlists` on your phone.


## Computer

3. Edit the `sync_music_playlists.py` script parameters following the inline instructions.

4. Add `sync.sh` to `Session and Startup > Application Autostart` to trigger it on login.

Deployed on Linux Mint 21.3 with Python 3.10.12 (watchdog 4.0.1), for Rhythmbox 3.4.4 and Phocid 20250409 (Vanilla Music 1.3.2).


## Support the developer

* Bitcoin: 1GDDJ7sLcBwFXg978qzCdsxrC8Ci9Dbgfa
* Monero: 4BGpHVqEWBtNwhwE2FECSt6vpuDMbLzrCFSUJHX5sPG44bZQYK1vN8MM97CbyC9ejSHpJANpJSLpxVrLQ2XT6xEXR8pzdCT
* Litecoin: LdaMXYuayfQmEQ4wsgR2Tp6om78caG3TEG
* Ethereum: 0x7862D03Dd9Dd5F1ebc020B2AaBd107d872ebA58E
* PayPal: paypal.me/neuralXray

