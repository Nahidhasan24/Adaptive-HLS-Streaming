import os
import subprocess
import sys

# Define the different resolutions and bitrates
streams = [
    {"name": "240p", "resolution": "426x240", "bitrate": "300k"},
    {"name": "360p", "resolution": "640x360", "bitrate": "700k"},
    {"name": "720p", "resolution": "1280x720", "bitrate": "1500k"},
]

def run_ffmpeg(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    playlists = []

    # Generate HLS for each stream
    for stream in streams:
        stream_name = stream["name"]
        playlist_path = os.path.join(output_dir, f"{stream_name}.m3u8")
        playlists.append({
            "name": stream_name,
            "playlist": f"{stream_name}.m3u8",
            "bandwidth": int(stream["bitrate"].replace("k", "000")),  # BANDWIDTH in bits/sec
            "resolution": stream["resolution"]
        })

        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:v", stream["bitrate"],
            "-s", stream["resolution"],
            "-hls_time", "6",
            "-hls_playlist_type", "vod",
            playlist_path
        ]

        print(f"Generating {stream_name} stream...")
        subprocess.run(cmd, check=True)

    # Create master playlist
    master_path = os.path.join(output_dir, "master.m3u8")
    with open(master_path, "w") as f:
        f.write("#EXTM3U\n")
        for p in playlists:
            f.write(f'#EXT-X-STREAM-INF:BANDWIDTH={p["bandwidth"]},RESOLUTION={p["resolution"]}\n')
            f.write(f'{p["playlist"]}\n')

    print(f"Master playlist created at {master_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python adaptive_hls_windows_fixed.py <input_video> <output_folder>")
        sys.exit(1)

    input_video = sys.argv[1]
    output_folder = sys.argv[2]
    run_ffmpeg(input_video, output_folder)