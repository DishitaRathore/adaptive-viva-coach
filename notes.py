import re
from io import BytesIO


STOP_WORDS = {
    "the", "and", "for", "are", "was", "were", "with", "that", "this",
    "from", "into", "what", "when", "where", "which", "who", "why",
    "how", "does", "did", "can", "could", "should", "would", "have",
    "has", "had", "not", "but", "about", "their", "there", "then",
}


def extract_pdf_pages(pdf_bytes):
    """Extract selectable text from each page of an uploaded PDF."""
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text,
            })

    return pages


def _terms(text):
    words = re.findall(r"\w+", text.casefold(), flags=re.UNICODE)
    return {
        word
        for word in words
        if len(word) > 2 and word not in STOP_WORDS
    }


def retrieve_relevant_pages(pages, query, top_k=3, chunk_size=1000):
    """Return the most relevant short text excerpts and their PDF page numbers."""
    query_terms = _terms(query)

    if not query_terms:
        return []

    matches = []

    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()

        # Split long pages into overlapping excerpts so relevant text later
        # in a page can still be found.
        step = max(1, chunk_size - 150)

        for start in range(0, len(text), step):
            excerpt = text[start:start + chunk_size]
            excerpt_terms = _terms(excerpt)
            overlap = len(query_terms & excerpt_terms)

            if overlap:
                matches.append({
                    "page": page["page"],
                    "score": overlap,
                    "text": excerpt,
                })

    matches.sort(key=lambda item: (-item["score"], item["page"]))
    return matches[:top_k]