# Sync music playlists between Rhythmbox (pc) and Vanilla Music (mobile phone)

Fully synchronize your music playlists between Rhythmbox, in your computer, and Vanilla Music, in your mobile phone.

0. Execute:

```
git clone https://github.com/neuralXray/sync-music-playlists.git
cd sync-music-playlists
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
chmod u+x sync.sh
touch sync.log
```

1. In Vanilla Music: `Settings > Playlists > Playlists Synchronization`, select `Full synchronization`.

2. Synchronize `/home/username/.local/share/rhythmbox/` in your computer with `storage/emulated/0/Android/media/ch.blinkenlights.android.vanilla/Playlists` in your phone with Syncthing.

3. Modify `sync_music_playlists.py` script parameters following inplace instructions.

4. Add `sync.sh` to Session and Startup > Application Autostart to trigger it on logging.

Deployed in Linux Mint 21.3 with Python 3.10.12 (watchdog 4.0.1). For Rhythmbox 3.4.4 and Vanilla Music 1.3.2.


## Support the developer

* Bitcoin: 1GDDJ7sLcBwFXg978qzCdsxrC8Ci9Dbgfa
* Monero: 4BGpHVqEWBtNwhwE2FECSt6vpuDMbLzrCFSUJHX5sPG44bZQYK1vN8MM97CbyC9ejSHpJANpJSLpxVrLQ2XT6xEXR8pzdCT
* Litecoin: LdaMXYuayfQmEQ4wsgR2Tp6om78caG3TEG
* Ethereum: 0x7862D03Dd9Dd5F1ebc020B2AaBd107d872ebA58E
* PayPal: paypal.me/neuralXray

