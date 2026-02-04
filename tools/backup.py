import os
import requests
import time
from datetime import datetime
from typing import List, Dict
import base64

UPDATE_PATH = "./update/"

PROTOCOL_PREFIXES = (
    "vless://",
    "vmess://",
    "trojan://",
    "ss://",
    "ssr://",
    "hysteria://",
    "hysteria2://",
    "tuic://",
    "wireguard://",
)


# ------------------ Helper Functions ------------------

def backup(text: str) -> None:
    """Save fetched text to a dated backup file."""
    date_dir = datetime.now().strftime("%y%m")
    date_file = datetime.now().strftime("%y%m%d_%H%M%S")

    os.makedirs(os.path.join(UPDATE_PATH, date_dir), exist_ok=True)
    file_path = os.path.join(UPDATE_PATH, date_dir, f"{date_file}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def clean_text(text: str) -> str:
    """Normalize response text."""
    return text.replace("&amp;", "&").strip()


def fetch_url(url: str, timeout: int = 10, retry_count: int = 1) -> Dict:
    """Fetch a single URL with retries."""
    max_attempts = retry_count + 1
    for attempt in range(max_attempts):
        try:
            print(f"Fetching ({attempt + 1}/{max_attempts}): {url}")
            response = requests.get(
                url,
                timeout=timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                        " AppleWebKit/537.36"
                    )
                },
            )
            response.raise_for_status()
            text = clean_text(response.text)
            return {
                "success": True,
                "status_code": response.status_code,
                "text": text,
                "lines": text.splitlines(),
                "headers": dict(response.headers),
                "elapsed": response.elapsed.total_seconds(),
                "attempts": attempt + 1,
            }
        except requests.exceptions.Timeout:
            print("⚠ Timeout, retrying...")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            if attempt == max_attempts - 1:
                return {
                    "success": False,
                    "status_code": None,
                    "error": str(e),
                    "attempts": attempt + 1,
                }
    return {"success": False, "status_code": None, "error": "Unknown", "attempts": max_attempts}


def fetch_urls(urls: List[str], timeout: int = 10, retry_count: int = 1) -> Dict[str, Dict]:
    """Fetch multiple URLs."""
    results = {}
    for url in urls:
        results[url] = fetch_url(url, timeout, retry_count)
    return results


def process_results(results: Dict[str, Dict]) -> List[str]:
    """Filter, deduplicate, and backup valid responses."""
    selected = []

    for url, data in results.items():
        if not data.get("success"):
            print(f"✗ Failed: {url} - {data.get('error')}")
            continue

        text = data["text"]

        if len(text.splitlines()) > 100 and text not in selected:
            selected.append(text)
            backup(text)
            print("-" * 60)
            print(f"{url}: {data['status_code']} - {len(text)} chars")
    return selected


def encode_line(line: str) -> str:
    """Encode raw config line to base64 if needed."""
    line = line.strip()
    if not line:
        return ""
    if line.startswith(PROTOCOL_PREFIXES):
        return base64.b64encode(line.encode()).decode()
    # Already base64? keep as is
    try:
        base64.b64decode(line, validate=True)
        return line
    except Exception:
        return ""


def merge_and_export(texts: list[str], output_dir: str = UPDATE_PATH) -> None:
    """Generate raw.txt, base64.txt, and protocol-specific files from multiple config texts."""
    raw_lines = []
    encoded_lines = []
    seen = set()
    protocol_dict = {p[:-3] if p.endswith("://") else p: [] for p in PROTOCOL_PREFIXES}  # store lines by protocol

    for text in texts:
        for line in text.splitlines():
            line = line.strip()
            if not line or line in seen:
                continue
            seen.add(line)
            if line.startswith(PROTOCOL_PREFIXES):
                raw_lines.append(line)
                encoded = encode_line(line)
                if encoded:
                    encoded_lines.append(encoded)
                # Assign line to protocol-specific list
                for proto in PROTOCOL_PREFIXES:
                    if line.startswith(proto):
                        protocol_dict[proto[:-3] if proto.endswith("://") else proto].append(line)
                        break

    os.makedirs(output_dir, exist_ok=True)

    # RAW output
    raw_file = os.path.join(output_dir, "raw.txt")
    with open(raw_file, "w", encoding="utf-8") as f:
        f.write("\n".join(raw_lines))
    print(f"\n✅ Raw merged file created: {raw_file} ({len(raw_lines)} links)")

    # BASE64 output
    base64_file = os.path.join(output_dir, "base64.txt")
    final_payload = "\n".join(encoded_lines)
    final_base64 = base64.b64encode(final_payload.encode()).decode()
    with open(base64_file, "w", encoding="utf-8") as f:
        f.write(final_base64)
    print(f"✅ Base64 subscription file created: {base64_file} ({len(encoded_lines)} links)")

    # Protocol-specific files
    for proto, lines in protocol_dict.items():
        if lines:
            proto_file = os.path.join(output_dir, f"{proto}.txt")
            with open(proto_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print(f"📄 {proto} file created: {proto_file} ({len(lines)} links)")



# ------------------ USAGE ------------------

urls = [
    "https://raw.githubusercontent.com/ShatakVPN/ConfigForge-V2Ray/main/configs/all.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/all_new.txt",
    "https://amirrezafarnamtaheri.github.io/ConfigStream/proxies.txt",
]

results = fetch_urls(urls, timeout=5, retry_count=2)
selected = process_results(results)
merge_and_export(selected)
