from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# ------------------ TEXTOS ------------------
def get_texts(lang="pt"):
    if lang == "pt":
        return {
            "site_name": "VideoDownloader",
            "tagline": "Baixe vídeos de qualquer rede social",
            "hero_cta": "Cole o link abaixo e faça o download!",
            "download_placeholder": "Cole o link do vídeo aqui...",
            "format_label": "Formato:",
            "download_button": "Baixar",
            "mp4_option": "MP4",
            "mp3_option": "MP3",
            "status_ready": "Pronto para baixar!",
            "tools_title": "Ferramentas Disponíveis",
            "tools": ["YouTube", "Instagram", "TikTok", "Facebook"],
            "features_title": "Principais recursos",
            "feature_easy": "Fácil de usar",
            "feature_quality": "Alta qualidade",
            "feature_unlimited": "Downloads ilimitados",
            "howto_title": "Como usar",
            "howto_steps": ["Cole o link", "Escolha o formato", "Clique em baixar"],
            "footer_nav": ["Sobre", "Privacidade", "Termos", "Contato", "Blog"],
            "lang_pt": "Português",
            "lang_en": "Inglês",
            "blog_title": "Blog",
            "adsense_note": "Este site pode conter anúncios.",
            "legal_disclaimer": "Use por sua conta e risco."
        }
    else:
        return {
            "site_name": "VideoDownloader",
            "tagline": "Download videos from any social network",
            "hero_cta": "Paste the link below to download!",
            "download_placeholder": "Paste the video link here...",
            "format_label": "Format:",
            "download_button": "Download",
            "mp4_option": "MP4",
            "mp3_option": "MP3",
            "status_ready": "Ready to download!",
            "tools_title": "Available Tools",
            "tools": ["YouTube", "Instagram", "TikTok", "Facebook"],
            "features_title": "Main features",
            "feature_easy": "Easy to use",
            "feature_quality": "High quality",
            "feature_unlimited": "Unlimited downloads",
            "howto_title": "How to use",
            "howto_steps": ["Paste the link", "Choose format", "Click download"],
            "footer_nav": ["About", "Privacy", "Terms", "Contact", "Blog"],
            "lang_pt": "Portuguese",
            "lang_en": "English",
            "blog_title": "Blog",
            "adsense_note": "This site may contain ads.",
            "legal_disclaimer": "Use at your own risk."
        }

# ------------------ ROTAS PÁGINAS ------------------
@app.route("/")
@app.route("/<lang>")
def home(lang="pt"):
    return render_template("index.html", t=get_texts(lang), lang=lang)

@app.route("/blog")
@app.route("/<lang>/blog")
def blog(lang="pt"):
    return render_template("blog.html", t=get_texts(lang), lang=lang)

@app.route("/about")
@app.route("/<lang>/about")
def page_about(lang="pt"):
    return render_template("about.html", t=get_texts(lang), lang=lang)

@app.route("/privacy")
@app.route("/<lang>/privacy")
def page_privacy(lang="pt"):
    return render_template("privacy.html", t=get_texts(lang), lang=lang)

@app.route("/terms")
@app.route("/<lang>/terms")
def page_terms(lang="pt"):
    return render_template("terms.html", t=get_texts(lang), lang=lang)

@app.route("/contact")
@app.route("/<lang>/contact")
def contact(lang="pt"):
    return render_template("contact.html", t=get_texts(lang), lang=lang)

# ------------------ DOWNLOAD ------------------
@app.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("url")
    file_format = request.form.get("format", "mp4")

    # Nome temporário do arquivo
    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOADS_DIR, f"{file_id}.%(ext)s")

    # Configurações do yt-dlp
    ydl_opts = {
        "outtmpl": output_template,
        "format": "bestaudio/best" if file_format == "mp3" else "bestvideo+bestaudio/best",
    }

    if file_format == "mp3":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    # Faz o download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info)
        if file_format == "mp3":
            file_path = os.path.splitext(file_path)[0] + ".mp3"

    # Envia o arquivo para o usuário
    return send_file(file_path, as_attachment=True)

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
