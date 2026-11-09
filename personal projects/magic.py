import argparse
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def resolve_link(short_url: str) -> str:
    """Follow regular HTTP redirects from a Speedy Links URL."""
    parsed_url = urlparse(short_url)
    hostname = parsed_url.hostname or ""

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Use a full URL beginning with http:// or https://.")
    if hostname != "speedy-links.com" and not hostname.endswith(".speedy-links.com"):
        raise ValueError("The URL must be hosted on speedy-links.com.")

    request = Request(short_url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=15) as response:
        return response.geturl()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find the destination of a Speedy Links URL that uses HTTP redirects."
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Speedy Links URL to resolve (you will be prompted if omitted)",
    )
    args = parser.parse_args()
    short_url = args.url or input("Paste a Speedy Links URL: ").strip()

    try:
        destination = resolve_link(short_url)
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        print(f"Could not resolve the link: {error}")
        return 1

    print(f"Destination: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())