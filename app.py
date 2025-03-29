"""
Local deployment: Run the app locally using Flask.
"""

import os
import yt_dlp
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path to save downloaded files
UPLOAD_FOLDER = "downloads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the download folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Route to display the HTML page
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle the YouTube video download
@app.route("/download", methods=["POST"])
def download_video():
    if request.method == "POST":
        # Get YouTube URL and save path
        video_url = request.form["url"]
        save_path = request.form["save_path"]

        # Ensure the save path is safe
        safe_save_path = secure_filename(save_path)

        # Set download options
        ydl_opts = {
            "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best",  # WebM preferred, fall back to best available
            "outtmpl": os.path.join(
                save_path, "%(title)s.%(ext)s"
            ),  # Save with original title and format extension
            ######## If you wish to get best video and audio, and wish to merge them and then convert to mp4, you can use below options.
            ######## Prerequisites: ffmpeg should be installed and added to PATH. ########
            # "format": "bestvideo+bestaudio/best",  # Best video + best audio
            # "postprocessors": [
            #     {
            #         "key": "FFmpegVideoConvertor",
            #         "preferedformat": "mp4",  # Convert to mp4 format
            #     }
            # ],
            # "ffmpeg_location": "D://ffmpeg",  # Ensure ffmpeg is in the PATH
        }

        # Download video
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return jsonify(
                {
                    "message": "Download complete!",
                    "file_path": os.path.join(UPLOAD_FOLDER, f"{safe_save_path}.mp4"),
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify({"error": "Invalid request"})


if __name__ == "__main__":

    # Run the app locally
    app.run(debug=True)


"""
Google Cloud Run Deployment:
Below are scripts for deploying the app on Google Cloud Run. 
This requires a cookie file that extracted from your browser for authentication, 
which is not implemented in the current version of the app. 
The scripts are provided for reference only.
"""

# from flask import Flask, request, render_template, jsonify
# import yt_dlp
# import requests
# import os

# app = Flask(__name__)

# # Set headers to mimic a real browser
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
# }

# # Download folder
# DOWNLOAD_FOLDER = "downloads"
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# @app.route("/", methods=["GET"])
# def index():
#     """Serve the front-end HTML page."""
#     return render_template("index.html")


# @app.route("/download", methods=["POST"])
# def download_video():
#     """
#     API Endpoint to download a video from a given URL.
#     """
#     if not request.is_json:
#         return jsonify({"error": "Content-Type must be application/json"}), 415

#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Invalid JSON"}), 400

#     video_url = data.get("url")
#     save_path = data.get("save_path")

#     if not video_url:
#         return jsonify({"error": "No URL provided"}), 400

#     # Check if authentication is required
#     needs_auth = needs_authentication(video_url)
#     cookies_path = "cookies.txt" if needs_auth else None

#     # Run the downloader
#     filename = download_youtube_video(video_url, cookies_path)

#     if filename:
#         return jsonify({"message": "Download started", "file": filename}), 200
#     else:
#         return jsonify({"error": "Failed to download video"}), 500


# def download_youtube_video(url, cookies_path=None):
#     """
#     Downloads a video using yt-dlp with authentication and best format selection.
#     """
#     ydl_opts = {
#         "format": "bestvideo+bestaudio/best",
#         "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
#         "noprogress": True,
#         "quiet": True,
#         "nocheckcertificate": True,
#         "headers": HEADERS,
#     }

#     # Attach cookies if required
#     if cookies_path:
#         ydl_opts["cookiefile"] = cookies_path

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         return "Download successful"
#     except Exception as e:
#         print(f"Download error: {e}")
#         return None


# def needs_authentication(url):
#     """
#     Checks if authentication is needed (e.g., login page, restricted content).
#     """
#     try:
#         response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
#         if "login" in response.url.lower() or response.status_code in [401, 403]:
#             return True
#     except requests.RequestException:
#         return False
#     return False


# if __name__ == "__main__":

#     app.run(host="0.0.0.0", port=8080)
