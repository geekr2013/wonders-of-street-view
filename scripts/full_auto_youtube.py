#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily YouTube Shorts workflow using free Pexels footage.
- English-first metadata
- Reduced template repetition
- Series-based packaging
- Source attribution logging
"""

import base64
import json
import os
import pickle
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
AUDIO_DIR = BASE_DIR / "assets" / "audio"
DEFAULT_BGM_PATH = AUDIO_DIR / "background.mp3"
SOURCE_LOG_PATH = LOGS_DIR / "source_log.jsonl"

OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

COUNTRY_NAME_MAP = {
    "그리스": "Greece",
    "독일": "Germany",
    "몰디브": "Maldives",
    "미국": "USA",
    "베트남": "Vietnam",
    "브라질": "Brazil",
    "스페인": "Spain",
    "아르헨티나": "Argentina",
    "영국": "United Kingdom",
    "요르단": "Jordan",
    "이집트": "Egypt",
    "이탈리아": "Italy",
    "인도": "India",
    "인도네시아": "Indonesia",
    "일본": "Japan",
    "중국": "China",
    "캄보디아": "Cambodia",
    "캐나다": "Canada",
    "탄자니아": "Tanzania",
    "페루": "Peru",
    "프랑스": "France",
    "프랑스령 폴리네시아": "French Polynesia",
    "호주": "Australia",
}


COUNTRY_TO_ISO2 = {
    "Argentina": "AR",
    "Australia": "AU",
    "Austria": "AT",
    "Bolivia": "BO",
    "Brazil": "BR",
    "Cambodia": "KH",
    "Canada": "CA",
    "Chile": "CL",
    "China": "CN",
    "Croatia": "HR",
    "Czech Republic": "CZ",
    "Egypt": "EG",
    "France": "FR",
    "French Polynesia": "PF",
    "Germany": "DE",
    "Greece": "GR",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Italy": "IT",
    "Japan": "JP",
    "Jordan": "JO",
    "Maldives": "MV",
    "Mexico": "MX",
    "Myanmar": "MM",
    "New Zealand": "NZ",
    "Norway": "NO",
    "Peru": "PE",
    "South Africa": "ZA",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Tanzania": "TZ",
    "Turkey": "TR",
    "USA": "US",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "Venezuela": "VE",
    "Vietnam": "VN",
}

SERIES_RULES = {
    "City Walks": {
        "keywords": ["도시", "랜드마크", "건축물", "마을", "야경"],
        "title_templates": [
            "Walk Through {name} | {country}",
            "Street-Level Views: {name}, {city}",
            "Why Travelers Love {name} ({country})",
            "Inside {name}: City Walk Highlights",
        ],
        "hook_templates": [
            "Street-level views from a popular destination",
            "A city walk worth saving",
            "Quick highlights before your next trip",
            "Local vibes from one famous spot",
        ],
    },
    "History Trails": {
        "keywords": ["역사", "유적", "사원", "성당", "궁전", "성"],
        "title_templates": [
            "Historic Walk: {name} in {country}",
            "Inside {name} | History Trails",
            "Timeless Streets of {name} ({country})",
            "Why {name} Still Matters Today",
        ],
        "hook_templates": [
            "A place where history meets daily life",
            "Walk through living history",
            "A timeless landmark from street level",
            "Past and present in one destination",
        ],
    },
    "Nature Escapes": {
        "keywords": ["자연", "산", "폭포", "바다", "섬", "협곡", "사막", "호수", "빙하", "정글", "공원", "해안", "온천"],
        "title_templates": [
            "Nature Escape: {name}, {country}",
            "Scenic Streets Around {name}",
            "Why Everyone Visits {name}",
            "Pure Travel Vibes at {name} ({country})",
        ],
        "hook_templates": [
            "A calm view from a natural destination",
            "Scenic textures and travel vibes",
            "A place worth adding to your trip list",
            "Take a short visual break in nature",
        ],
    },
}

CTA_TEMPLATES = [
    "Follow for the next destination.",
    "More places are coming every day.",
    "Save this short for your future trip list.",
]

DESC_TEMPLATES = [
    "Today we explore {name} in {city}, {country}.",
    "A quick walk around {name}, right in the heart of {city}, {country}.",
    "Street-level moments from {name} ({country}).",
    "A short visual stop at {name} in {city}.",
]


def remove_emoji(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001FAFF"
        "\u2600-\u27BF"
        "\uFE0F"
        "]",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def clean_text(text: str) -> str:
    no_emoji = remove_emoji(text)
    lines = no_emoji.replace("\r\n", "\n").split("\n")
    cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in lines]
    return "\n".join(cleaned_lines).strip()


def clean_metadata_text(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in lines]
    return "\n".join(cleaned_lines).strip()


def load_locations() -> list[dict]:
    with open(CONFIG_DIR / "locations.json", "r", encoding="utf-8") as f:
        return json.load(f)


def select_random_location(locations: list[dict]) -> dict:
    return random.choice(locations)


def to_english_country(country_name: str) -> str:
    return COUNTRY_NAME_MAP.get(country_name, country_name)


def get_country_en(location: dict) -> str:
    return clean_text(location.get("country_en") or to_english_country(location.get("country", "")))


def get_city_en(location: dict) -> str:
    return clean_text(location.get("city_en") or location.get("city", ""))


def country_code_to_flag(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return ""
    code = country_code.upper()
    if not code.isalpha():
        return ""
    return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)


def get_country_flag_emoji(location: dict) -> str:
    country_en = get_country_en(location)
    iso2 = COUNTRY_TO_ISO2.get(country_en, "")
    return country_code_to_flag(iso2)


def get_description_en(location: dict) -> str:
    fallback = f"A short street-level look around {location['name_en']} in {get_city_en(location)}, {get_country_en(location)}."
    return clean_text(location.get("description_en") or fallback)


def choose_series(location: dict) -> str:
    tags = " ".join(location.get("tags", []))
    for series_name, series_meta in SERIES_RULES.items():
        for keyword in series_meta["keywords"]:
            if keyword in tags:
                return series_name
    return "City Walks"


def build_content_package(location: dict) -> dict:
    day = datetime.now(timezone.utc).strftime("%m%d")
    seed = int(datetime.now(timezone.utc).strftime("%Y%m%d")) + int(location.get("id", 0))
    rng = random.Random(seed)

    name = location["name_en"]
    city = get_city_en(location)
    country = get_country_en(location)
    series = choose_series(location)

    series_meta = SERIES_RULES[series]
    title = rng.choice(series_meta["title_templates"]).format(
        name=name,
        city=city,
        country=country,
        day=day,
    )
    intro = rng.choice(series_meta["hook_templates"])
    body = rng.choice(DESC_TEMPLATES).format(name=name, city=city, country=country)
    cta = rng.choice(CTA_TEMPLATES)

    hashtags = [
        f"#{name.replace(' ', '')}",
        f"#{country.replace(' ', '')}",
        "#Travel",
        "#StreetView",
        "#Shorts",
        f"#{series.replace(' ', '')}",
    ]

    description_lines = [
        f"Series: {series}",
        body,
        get_description_en(location),
        f"Location: {city}, {country}",
        cta,
        "",
        " ".join(hashtags),
    ]

    tags = [
        "travel",
        "street view",
        "shorts",
        "walking tour",
        series.lower(),
        name.lower(),
        country.lower(),
        city.lower(),
    ]

    flag = get_country_flag_emoji(location)
    title_text = clean_metadata_text(title)[:98]
    if flag:
        title_text = f"{flag} {title_text}"[:100]

    return {
        "series": series,
        "title": title_text,
        "description": clean_metadata_text("\n".join(description_lines)),
        "tags": sorted(set(clean_text(t) for t in tags if t)),
        "hook": clean_text(intro),
        "subtitle": clean_text(f"{name}, {country}"),
    }


def search_pexels_video(query: str, api_key: str) -> dict | None:
    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=portrait"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("videos"):
            video = random.choice(data["videos"][:5])
            video_files = video.get("video_files", [])
            portrait_videos = [v for v in video_files if v.get("width", 0) < v.get("height", 0)]

            if portrait_videos:
                best_video = max(portrait_videos, key=lambda x: x.get("width", 0))
                user = video.get("user", {})
                return {
                    "download_url": best_video["link"],
                    "pexels_video_id": video.get("id"),
                    "pexels_page_url": video.get("url"),
                    "creator_name": user.get("name"),
                    "creator_url": user.get("url"),
                    "search_query": query,
                }
        return None
    except Exception as e:
        print(f"Pexels API error: {e}")
        return None


def download_video(url: str, output_path: Path) -> bool:
    try:
        print("Downloading source video...")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Download complete")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def has_audio_stream(video_path: Path) -> bool:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "csv=p=0",
        str(video_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return bool(result.stdout.strip())
    except Exception:
        return False


def resolve_background_music_path() -> Path:
    env_path = os.getenv("BACKGROUND_MUSIC_FILE", "").strip()
    if env_path:
        candidate = Path(env_path)
        if not candidate.is_absolute():
            candidate = BASE_DIR / candidate
        return candidate

    candidates = [
        AUDIO_DIR / f"background_{i:02d}.mp3"
        for i in range(1, 7)
        if (AUDIO_DIR / f"background_{i:02d}.mp3").exists()
    ]

    if candidates:
        return random.choice(candidates)

    return DEFAULT_BGM_PATH


def compose_final_shorts(video_path: Path, hook_text: str, subtitle_text: str, output_path: Path) -> bool:
    font_paths = [
        str(BASE_DIR / "fonts" / "HakgyoansimYeohaengOTFR.otf"),
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    font_file = next((f for f in font_paths if Path(f).exists()), font_paths[-1])

    def escape_text_for_ffmpeg(text: str) -> str:
        text = text.replace("\\", "\\\\")
        text = text.replace(":", "\\:")
        text = text.replace("%", "\\%")
        text = text.replace("'", "'\\\\''")
        return text

    hook = escape_text_for_ffmpeg(hook_text)
    subtitle = escape_text_for_ffmpeg(subtitle_text)

    draw_hook = (
        f"drawtext=text='{hook}':fontfile={font_file}:fontsize=52:fontcolor=white:"
        "box=1:boxcolor=black@0.45:boxborderw=18:x=(w-text_w)/2:y=110"
    )
    draw_subtitle = (
        f"drawtext=text='{subtitle}':fontfile={font_file}:fontsize=62:fontcolor=white:"
        "borderw=4:bordercolor=black:x=(w-text_w)/2:y=210"
    )

    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,{draw_hook},{draw_subtitle}[vout]"
    )

    has_source_audio = has_audio_stream(video_path)
    bg_music_path = resolve_background_music_path()

    if has_source_audio:
        print("Source audio detected: using original track")
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-filter_complex", "".join(filter_complex),
            "-map", "[vout]",
            "-map", "0:a:0",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", "60",
            "-y",
            str(output_path),
        ]
    elif bg_music_path.exists():
        print(f"No source audio: using background music {bg_music_path.name}")
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-stream_loop", "-1",
            "-i", str(bg_music_path),
            "-filter_complex", "".join(filter_complex),
            "-map", "[vout]",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", "60",
            "-shortest",
            "-y",
            str(output_path),
        ]
    else:
        print("No source audio and no fallback music found; exporting without audio")
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-filter_complex", "".join(filter_complex),
            "-map", "[vout]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-t", "60",
            "-y",
            str(output_path),
        ]

    try:
        print("Composing final short...")
        subprocess.run(cmd, capture_output=True, check=True)
        print("Composition complete")
        return True
    except Exception as e:
        print(f"Composition failed: {e}")
        return False


def get_youtube_service():
    creds = None
    token_base64 = os.getenv("YOUTUBE_TOKEN_BASE64")

    if token_base64:
        try:
            token_data = base64.b64decode(token_base64)
            creds = pickle.loads(token_data)
            print("YouTube token loaded")
        except Exception as e:
            print(f"Token load failed: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("YouTube token refreshed")
            except Exception as e:
                print(f"Token refresh failed: {e}")
                return None
        else:
            print("YouTube authentication required")
            return None

    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(video_path: Path, content: dict):
    print("\nPreparing YouTube upload")
    print(f"Title: {content['title']}")
    print(f"File: {video_path.name}")

    try:
        youtube = get_youtube_service()
        if not youtube:
            print("YouTube API authentication failed")
            return None

        body = {
            "snippet": {
                "title": content["title"],
                "description": content["description"],
                "tags": content["tags"],
                "categoryId": "19",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
                "madeForKids": False,
            },
        }

        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,
            resumable=True,
            mimetype="video/mp4",
        )

        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")

        video_id = response["id"]
        video_url = f"https://youtube.com/shorts/{video_id}"
        print(f"Upload complete: {video_url}")
        return video_url

    except Exception as e:
        print(f"Upload failed: {e}")
        import traceback

        traceback.print_exc()
        return None


def append_source_log(location: dict, source_info: dict, content: dict, final_video: Path, youtube_url: str | None) -> None:
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "location_id": location.get("id"),
        "location_name_en": location.get("name_en"),
        "city_en": get_city_en(location),
        "country_en": get_country_en(location),
        "series": content.get("series"),
        "title": content.get("title"),
        "final_video": str(final_video),
        "youtube_url": youtube_url,
        "source": source_info,
    }
    with open(SOURCE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def save_output_metadata(location: dict, source_info: dict, content: dict, final_video: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = location["name_en"].replace(" ", "_")
    metadata_path = OUTPUT_DIR / f"{safe_name}_{timestamp}_metadata.json"
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "location": location,
        "content": content,
        "source": source_info,
        "final_video": str(final_video),
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return metadata_path


def main():
    print("\n" + "=" * 70)
    print("YouTube Shorts generation and upload")
    print("=" * 70)

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("PEXELS_API_KEY is required")
        sys.exit(1)

    locations = load_locations()
    location = select_random_location(locations)
    print(f"Selected: {location['name_en']} ({get_country_en(location)})")

    content = build_content_package(location)

    source_info = search_pexels_video(
        f"{location['name_en']} {get_country_en(location)} travel", api_key
    )
    if not source_info:
        source_info = search_pexels_video(f"{get_country_en(location)} landmark", api_key)

    if not source_info:
        print("No matching video found")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_video = OUTPUT_DIR / f"raw_{timestamp}.mp4"
    safe_name = location["name_en"].replace(" ", "_")
    final_video = OUTPUT_DIR / f"{safe_name}_short_{timestamp}.mp4"

    if not download_video(source_info["download_url"], raw_video):
        sys.exit(1)

    if not compose_final_shorts(raw_video, content["hook"], content["subtitle"], final_video):
        sys.exit(1)

    metadata_path = save_output_metadata(location, source_info, content, final_video)
    video_url = upload_to_youtube(final_video, content)

    append_source_log(location, source_info, content, final_video, video_url)

    raw_video.unlink(missing_ok=True)

    print("\n" + "=" * 70)
    print("Done")
    print("=" * 70)
    print(f"Series: {content['series']}")
    print(f"Location: {location['name_en']}")
    print(f"Video: {final_video}")
    print(f"Metadata: {metadata_path}")
    if video_url:
        print(f"YouTube: {video_url}")
    else:
        print("Upload failed")

    if video_url:
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a", encoding="utf-8") as f:
                f.write(f"video_url={video_url}\n")
                f.write(f"location={location['name_en']}\n")
                f.write(f"series={content['series']}\n")

    return 0 if video_url else 1


if __name__ == "__main__":
    sys.exit(main())
