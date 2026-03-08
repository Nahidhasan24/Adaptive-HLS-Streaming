# Adaptive HLS Streaming with Modern Video.js Player

This project demonstrates a **local adaptive video streaming setup** using FFmpeg-generated HLS files and a modern Video.js player with quality selector controls. Perfect for short-video platforms like TikTok or Instagram Reels.

---

## **Project Structure**

```
Project/
├─ index.html             # Main HTML player page
├─ videos/                # Folder containing HLS playlists and segments
│   ├─ master.m3u8        # Master playlist for adaptive streaming
│   ├─ 240p.m3u8
│   ├─ 360p.m3u8
│   ├─ 720p.m3u8
│   ├─ 240p0.ts
│   ├─ 240p1.ts
│   ├─ ...
│   ├─ 720p5.ts
```

---

## **Requirements**

- **Python 3.x** (for serving local files via HTTP)
- **FFmpeg** (for generating HLS playlists and segments)
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for Video.js CDN, or use local Video.js files)

---

## **Setup**

### 1. Generate HLS from video

Use FFmpeg (or the provided Python script) to create HLS playlists with multiple resolutions:

```bash
python adaptive_hls_windows_fixed.py input.mp4 ./videos
```

This generates:

- `master.m3u8` — master playlist pointing to different resolutions
- `240p.m3u8`, `360p.m3u8`, `720p.m3u8` — variant playlists
- `.ts` segment files for each resolution

---

### 2. Serve files via HTTP

Browsers **cannot play HLS from local file paths**. Start a local server in the project root:

```bash
python -m http.server 8000
```

Access your player at:

```
http://localhost:8000/index.html
```

---

### 3. Modern Video.js Player

- Uses Video.js v8.x from CDN
- Includes **quality selector plugin** for switching resolutions
- Responsive and modern UI
- Big centered play button, rounded container, shadow effects

#### Key HTML Example

```html
<video
  id="my-video"
  class="video-js vjs-big-play-centered vjs-theme-city"
  controls
>
  <source src="videos/master.m3u8" type="application/x-mpegURL" />
</video>
<script src="https://vjs.zencdn.net/8.23.4/video.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/videojs-http-source-selector@1.1.12/dist/videojs-http-source-selector.min.js"></script>
<script>
  const player = videojs("my-video");
  player.ready(function () {
    player.httpSourceSelector();
    player.play().catch(() => console.log("Autoplay blocked"));
  });
</script>
```

---

## **Notes**

- Ensure **master.m3u8** points to the correct variant playlists
- Variant playlists must reference the correct `.ts` segment files
- Keep all HLS files in the same folder (`videos/`) or adjust paths accordingly
- For multiple short videos, you can create separate folders and generate playlists per video

---

## **References**

- [Video.js Documentation](https://videojs.com/)
- [Video.js HTTP Source Selector Plugin](https://github.com/videojs/videojs-http-source-selector)
- [FFmpeg HLS Streaming Guide](https://trac.ffmpeg.org/wiki/StreamingGuide)

---
