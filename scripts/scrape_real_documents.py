"""Scrape real public documents for the Bayer-Monsanto M&A case study.

Fetches content from verified public URLs using per-source strategies,
and caches results for use by generate_sample_documents.py.

Usage:
    uv run python scripts/scrape_real_documents.py [--force] [--doc-id LEX-XXX-NNN]
"""

import argparse
import io
import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent
CACHE_DIR = ROOT_DIR / "data" / "scraped_cache"

# SEC requires a company name + email in User-Agent
SEC_USER_AGENT = "LexBridge/1.0 pankymathur@gmail.com"
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_DELAY = 1.5  # seconds between requests
MAX_CONTENT_CHARS = 10_000  # max chars per document


# ---------------------------------------------------------------------------
# Scrape target definitions
# ---------------------------------------------------------------------------

@dataclass
class ScrapeTarget:
    doc_id: str
    url: str
    strategy: str  # wikipedia, sec_edgar, pubmed, html, pdf, browser
    section_filter: str | None = None
    max_pdf_pages: int = 20


SCRAPE_TARGETS: list[ScrapeTarget] = [
    # --- Court cases ---
    ScrapeTarget("LEX-LIT-001",
                 "https://en.wikipedia.org/wiki/Johnson_v._Monsanto_Co.",
                 "wikipedia"),
    ScrapeTarget("LEX-LIT-002",
                 "https://law.justia.com/cases/california/court-of-appeal/2021/a158228.html",
                 "browser"),
    ScrapeTarget("LEX-LIT-003",
                 "https://cdn.ca9.uscourts.gov/datastore/opinions/2021/05/14/19-16636.pdf",
                 "pdf", max_pdf_pages=30),
    ScrapeTarget("LEX-LIT-004",
                 "https://www.courtlistener.com/docket/4579168/in-re-roundup-products-liability-litigation/",
                 "html"),
    ScrapeTarget("LEX-LIT-005",
                 "https://en.wikipedia.org/wiki/Monsanto_legal_cases",
                 "wikipedia"),

    # --- Regulatory ---
    ScrapeTarget("LEX-REG-001",
                 "https://www.epa.gov/ingredients-used-pesticide-products/glyphosate",
                 "html"),
    ScrapeTarget("LEX-REG-002",
                 "https://www.iarc.who.int/wp-content/uploads/2018/07/MonographVolume112-1.pdf",
                 "pdf", max_pdf_pages=15),
    ScrapeTarget("LEX-REG-003",
                 "https://www.epa.gov/pesticides/epa-withdraws-glyphosate-interim-decision",
                 "html"),

    # --- Scientific studies ---
    ScrapeTarget("LEX-SCI-001",
                 "https://publications.iarc.who.int/549",
                 "html"),
    ScrapeTarget("LEX-SCI-002",
                 "https://www.epa.gov/sites/default/files/2020-01/documents/glyphosate-interim-reg-review-decision-case-num-0178.pdf",
                 "pdf", max_pdf_pages=20),
    ScrapeTarget("LEX-SCI-003", "31342895", "pubmed"),
    ScrapeTarget("LEX-SCI-004", "10854122", "pubmed"),

    # --- SEC filings ---
    ScrapeTarget("LEX-SEC-001",
                 "https://www.sec.gov/Archives/edgar/data/1110783/000111078317000187/mon-20170831x10k.htm",
                 "sec_edgar", section_filter="Item 1A"),
    ScrapeTarget("LEX-SEC-002",
                 "https://www.sec.gov/Archives/edgar/data/1110783/000119312516714915/d234658d8k.htm",
                 "sec_edgar", section_filter="Item 1.01"),

    # --- Merger agreement ---
    ScrapeTarget("LEX-MRG-001",
                 "https://www.sec.gov/Archives/edgar/data/1110783/000119312516714915/d234658dex21.htm",
                 "sec_edgar", section_filter="ARTICLE III"),
    ScrapeTarget("LEX-MRG-002",
                 "https://www.sec.gov/Archives/edgar/data/1110783/000119312516765991/d252304ddefm14a.htm",
                 "sec_edgar", section_filter="RISK FACTORS"),

    # --- Settlements ---
    ScrapeTarget("LEX-SET-001",
                 "https://en.wikipedia.org/wiki/Johnson_v._Monsanto_Co.",
                 "wikipedia"),
    ScrapeTarget("LEX-SET-002",
                 "https://www.bayer.com/media/en-us/bayer-announces-agreements-to-resolve-major-legacy-monsanto-litigation/",
                 "html"),

    # --- Competition / regulatory clearance ---
    ScrapeTarget("LEX-CRB-001",
                 "https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_18_2282/IP_18_2282_EN.pdf",
                 "pdf", max_pdf_pages=5),
    ScrapeTarget("LEX-CRB-002",
                 "https://en.wikipedia.org/wiki/Monsanto",
                 "wikipedia"),
    ScrapeTarget("LEX-CRB-003",
                 "https://www.justice.gov/atr/case/us-v-bayer-ag-and-monsanto-company",
                 "html"),
    ScrapeTarget("LEX-CRB-004",
                 "https://www.justice.gov/atr/case/us-v-bayer-ag-and-monsanto-company",
                 "html"),

    # --- BaFin filings (use Bayer Wikipedia for context) ---
    ScrapeTarget("LEX-BAF-001",
                 "https://en.wikipedia.org/wiki/Bayer",
                 "wikipedia"),
    # LEX-BAF-002 shares same source as BAF-001, skip (will use synthetic)

    # --- Shareholder comms (from Bayer annual reports) ---
    ScrapeTarget("LEX-SH-001",
                 "https://www.annualreports.com/HostedData/AnnualReportArchive/b/OTC_BAYZF_2017.pdf",
                 "pdf", max_pdf_pages=15),
    ScrapeTarget("LEX-SH-002",
                 "https://www.annualreports.com/HostedData/AnnualReportArchive/b/OTC_BAYZF_2018.pdf",
                 "pdf", max_pdf_pages=15),
]


# ---------------------------------------------------------------------------
# Scraper class
# ---------------------------------------------------------------------------

class Scraper:
    def __init__(self, cache_dir: Path = CACHE_DIR, force: bool = False):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.force = force
        self.session = requests.Session()

    # --- Public API ---

    def scrape_all(self, targets: list[ScrapeTarget]) -> dict[str, str]:
        results: dict[str, str] = {}
        for i, target in enumerate(targets):
            cached = self._load_cache(target.doc_id)
            if cached and not self.force:
                log.info(f"[{i+1}/{len(targets)}] {target.doc_id}: cached ({len(cached)} chars)")
                results[target.doc_id] = cached
                continue

            log.info(f"[{i+1}/{len(targets)}] {target.doc_id}: scraping ({target.strategy}) ...")
            text = self._scrape_one(target)
            text = _postprocess(text)

            if text:
                self._save_cache(target.doc_id, target.url, text, target.strategy)
                log.info(f"  -> {len(text)} chars")
            else:
                log.warning(f"  -> EMPTY (will keep synthetic content)")

            results[target.doc_id] = text
            if i < len(targets) - 1:
                time.sleep(REQUEST_DELAY)

        return results

    # --- Strategy dispatch ---

    def _scrape_one(self, target: ScrapeTarget) -> str:
        try:
            match target.strategy:
                case "wikipedia":
                    return self._fetch_wikipedia(target.url)
                case "sec_edgar":
                    return self._fetch_sec_edgar(target.url, target.section_filter)
                case "pubmed":
                    return self._fetch_pubmed(target.url)
                case "html":
                    return self._fetch_html(target.url)
                case "pdf":
                    return self._fetch_pdf(target.url, target.max_pdf_pages)
                case "browser":
                    return self._fetch_browser(target.url)
                case _:
                    log.warning(f"Unknown strategy: {target.strategy}")
                    return ""
        except requests.RequestException as e:
            log.warning(f"Network error for {target.doc_id}: {e}")
            return ""
        except Exception as e:
            log.error(f"Error for {target.doc_id}: {e}")
            return ""

    # --- Wikipedia ---

    def _fetch_wikipedia(self, url: str) -> str:
        # Extract page title from URL
        title = url.rstrip("/").split("/wiki/")[-1]
        api_url = (
            f"https://en.wikipedia.org/w/api.php"
            f"?action=query&prop=extracts&explaintext=true"
            f"&titles={title}&format=json&redirects=1"
        )
        headers = {"User-Agent": "LexBridge/1.0 (pankymathur@gmail.com)"}
        resp = self.session.get(api_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            text = page.get("extract", "")
            if text:
                # Remove "See also", "References", "External links" etc
                for section in ["== See also ==", "== References ==",
                                "== External links ==", "== Further reading =="]:
                    idx = text.find(section)
                    if idx > 0:
                        text = text[:idx]
                return text.strip()
        return ""

    # --- SEC EDGAR ---

    def _fetch_sec_edgar(self, url: str, section_filter: str | None) -> str:
        headers = {
            "User-Agent": SEC_USER_AGENT,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = self.session.get(url, headers=headers, timeout=60)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        # Remove scripts/styles
        for tag in soup(["script", "style", "meta", "link"]):
            tag.decompose()

        full_text = soup.get_text(separator="\n", strip=True)

        if not section_filter:
            return full_text[:MAX_CONTENT_CHARS]

        # Extract specific section(s)
        extracted_sections = []

        for section_name in section_filter.split(","):
            section_name = section_name.strip()
            extracted = _extract_section(full_text, section_name)
            if extracted and len(extracted) > 500:
                extracted_sections.append(extracted)

        if extracted_sections:
            return "\n\n".join(extracted_sections)

        # Fallback: return full text (section headings may be in different format)
        log.warning(f"Section '{section_filter}' too short or missing, using full text")
        return full_text[:MAX_CONTENT_CHARS]

    # --- PubMed E-utilities ---

    def _fetch_pubmed(self, pmid: str) -> str:
        # Fetch abstract via E-utilities
        efetch_url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            f"?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
        )
        resp = self.session.get(efetch_url, timeout=30)
        resp.raise_for_status()
        text = resp.text.strip()
        if text:
            return text
        # Fallback: fetch summary
        esummary_url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=pubmed&id={pmid}&retmode=json"
        )
        resp = self.session.get(esummary_url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        result = data.get("result", {}).get(pmid, {})
        title = result.get("title", "")
        return title

    # --- Generic HTML ---

    def _fetch_html(self, url: str) -> str:
        headers = {"User-Agent": BROWSER_UA}
        resp = self.session.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        # Remove navigation, footer, scripts, styles
        for tag in soup(["script", "style", "nav", "footer", "header",
                         "meta", "link", "aside"]):
            tag.decompose()

        # Try to find main content area
        main = (soup.find("main") or soup.find("article")
                or soup.find("div", class_=re.compile(r"content|article|body", re.I))
                or soup.find("body"))
        if main:
            text = main.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        return text

    # --- PDF ---

    def _fetch_pdf(self, url: str, max_pages: int = 20) -> str:
        from pypdf import PdfReader

        headers = {"User-Agent": BROWSER_UA}
        resp = self.session.get(url, headers=headers, timeout=60)
        resp.raise_for_status()

        reader = PdfReader(io.BytesIO(resp.content))
        pages_to_read = min(len(reader.pages), max_pages)
        text_parts = []
        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n\n".join(text_parts)

    # --- Browser-like headers (for sites that block simple bots) ---

    def _fetch_browser(self, url: str) -> str:
        headers = {
            "User-Agent": BROWSER_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        resp = self.session.get(url, headers=headers, timeout=30, allow_redirects=True)
        if resp.status_code == 403:
            log.warning(f"  403 Forbidden (bot-blocked): {url}")
            return ""
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        main = (soup.find("main") or soup.find("article")
                or soup.find("div", class_=re.compile(r"content|article", re.I))
                or soup.find("body"))
        if main:
            return main.get_text(separator="\n", strip=True)
        return soup.get_text(separator="\n", strip=True)

    # --- Cache management ---

    def _load_cache(self, doc_id: str) -> str | None:
        path = self.cache_dir / f"{doc_id}.json"
        if not path.exists():
            return None
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get("raw_text", "").strip() or None
        except Exception:
            return None

    def _save_cache(self, doc_id: str, url: str, text: str, method: str):
        path = self.cache_dir / f"{doc_id}.json"
        data = {
            "doc_id": doc_id,
            "url": url,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "extraction_method": method,
            "content_length": len(text),
            "raw_text": text,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_section(text: str, section_name: str, max_chars: int = MAX_CONTENT_CHARS) -> str:
    """Extract a named section from text (e.g., 'Item 1A' from a 10-K)."""
    sn = section_name.strip()

    # Try various heading patterns, case-insensitive
    patterns = [
        # "Item 1A" or "ITEM 1A" with various separators
        rf"(?i)(?:^|\n)\s*{re.escape(sn)}[\.\s\-\—\:\u2014]*(?:Risk Factors|[A-Z])",
        rf"(?i)(?:^|\n)\s*{re.escape(sn)}\b",
        # Handle "Item\xa01A" (non-breaking spaces in SEC filings)
        rf"(?i){sn.replace(' ', '.?')}",
    ]

    start = -1
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            start = match.start()
            break

    if start < 0:
        return ""

    section_text = text[start:]

    # Find the end: next section heading of same level
    if sn.lower().startswith("item"):
        end_match = re.search(r"(?i)\n\s*Item\s+\d", section_text[200:])
    elif sn.lower().startswith("article"):
        end_match = re.search(r"(?i)\n\s*ARTICLE\s+[IVX]+", section_text[200:])
    elif sn.lower().startswith("risk"):
        end_match = re.search(r"\n\s*[A-Z][A-Z\s]{10,}\n", section_text[500:])
    else:
        end_match = None

    if end_match:
        offset = 200 if sn.lower().startswith("item") or sn.lower().startswith("article") else 500
        section_text = section_text[:end_match.start() + offset]

    return section_text[:max_chars].strip()


def _postprocess(text: str) -> str:
    """Clean scraped text: remove boilerplate, normalize whitespace, truncate."""
    if not text:
        return ""

    # Remove common boilerplate
    boilerplate = [
        r"Skip to (?:main )?content",
        r"Cookie(?:s)? (?:Policy|Notice|Settings|Consent)",
        r"Accept (?:all )?cookies?",
        r"We use cookies.*?\.",
        r"JavaScript is (?:required|disabled)",
        r"Please enable JavaScript",
    ]
    for pattern in boilerplate:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\t+", " ", text)

    # Remove lines that are just short navigation-like fragments
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip very short lines that look like nav items
        if len(stripped) < 3 and stripped not in ("", "-", "*"):
            continue
        cleaned.append(line)
    text = "\n".join(cleaned)

    # Truncate at sentence boundary
    if len(text) > MAX_CONTENT_CHARS:
        text = text[:MAX_CONTENT_CHARS]
        last_period = text.rfind(".")
        if last_period > MAX_CONTENT_CHARS * 0.7:
            text = text[: last_period + 1]

    return text.strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Scrape real documents for LexBridge")
    parser.add_argument("--force", action="store_true", help="Re-scrape even if cached")
    parser.add_argument("--doc-id", type=str, help="Scrape only this document ID")
    args = parser.parse_args()

    targets = SCRAPE_TARGETS
    if args.doc_id:
        targets = [t for t in targets if t.doc_id == args.doc_id]
        if not targets:
            log.error(f"Unknown doc-id: {args.doc_id}")
            return

    log.info(f"Scraping {len(targets)} documents...")
    scraper = Scraper(force=args.force)
    results = scraper.scrape_all(targets)

    succeeded = sum(1 for v in results.values() if v)
    failed = [doc_id for doc_id, text in results.items() if not text]

    print(f"\nResults: {succeeded}/{len(targets)} documents scraped successfully.")
    if failed:
        print(f"Failed/empty (will keep synthetic): {failed}")
    print(f"Cache: {CACHE_DIR}")


if __name__ == "__main__":
    main()
