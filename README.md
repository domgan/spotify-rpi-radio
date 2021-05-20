# Embedded Systems Project

## How to run

1. Install spotify client for Raspberry Pi **raspotify** with:
```bash
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```
2. Create new app at [Spotify Dashboard](https://developer.spotify.com/dashboard/).
3. Provide your **Client ID**, **Client Secret** and **Redirect URI** to `auth` file.
4. Run `./run_radio.sh terminal` or `./run_radio.sh gui`.
5. If prompted, open login url in browser and paste to the terminal url you've been redirected to.
