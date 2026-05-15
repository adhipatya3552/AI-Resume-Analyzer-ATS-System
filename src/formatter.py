"""
formatter.py
~~~~~~~~~~~~
Parses a raw, unformatted job-description string into titled sections and
renders them as structured HTML inside a Streamlit app.
"""

import re
import streamlit as st


# Ordered list of section keywords to detect (more-specific first).
_SECTION_KEYWORDS = [
    "key responsibilities",
    "responsibilities",
    "preferred qualifications",
    "qualifications",
    "requirements",
    "nice to have",
    "bonus",
    "benefits",
    "about us",
    "about the role",
    "job overview",
    "overview",
    "what you will do",
    "what we offer",
]

# Pre-compile a single pattern that matches any keyword at a word boundary.
_SECTION_RE = re.compile(
    "|".join(r"(?<!\w)" + re.escape(kw) + r"(?!\w)" for kw in _SECTION_KEYWORDS),
    re.IGNORECASE,
)


def _split_into_bullets(body: str) -> list[str]:
    """Split a section body into individual bullet items."""
    # Split on period followed by space or end-of-string.
    clauses = re.split(r"\.\s+|\.\s*$", body)
    results = []
    for c in clauses:
        c = c.strip().strip(",").strip()
        if c:
            results.append(c[0].upper() + c[1:])
    return results


def format_job_description(text: str) -> None:
    """
    Render *text* as a structured job-description card inside Streamlit.

    Detects well-known section headers (e.g. "Key Responsibilities",
    "Requirements", "Benefits") and renders each section with a coloured
    heading and bullet points.  Falls back to wrapped plain text when no
    sections are found.
    """
    text = (text or "").strip()
    if not text:
        st.info("No job description available.")
        return

    matches = list(_SECTION_RE.finditer(text))

    # ── Card wrapper ─────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
        .jd-section-title {
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #4A90D9;
            margin: 1.2rem 0 0.35rem 0;
            padding-bottom: 4px;
            border-bottom: 1px solid rgba(74, 144, 217, 0.25);
        }
        .jd-intro {
            line-height: 1.75;
            margin-bottom: 0.8rem;
            color: var(--text-color);
        }
        .jd-bullets {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .jd-bullets li {
            position: relative;
            padding-left: 1.4rem;
            margin-bottom: 5px;
            line-height: 1.65;
            color: var(--text-color);
        }
        .jd-bullets li::before {
            content: "▸";
            position: absolute;
            left: 0;
            color: #4A90D9;
        }
        .jd-plain {
            line-height: 1.75;
            color: var(--text-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if not matches:
        # No recognisable sections – render as a readable paragraph.
        st.markdown(
            f'<p class="jd-plain">{text}</p>',
            unsafe_allow_html=True,
        )
        return

    # ── Intro text (before first section heading) ─────────────────────
    intro = text[: matches[0].start()].strip()
    if intro:
        st.markdown(
            f'<p class="jd-intro">{intro.capitalize()}</p>',
            unsafe_allow_html=True,
        )

    # ── Sections ──────────────────────────────────────────────────────
    for i, m in enumerate(matches):
        title = m.group(0).title()
        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end].strip().strip(":")

        st.markdown(
            f'<p class="jd-section-title">{title}</p>',
            unsafe_allow_html=True,
        )

        bullets = _split_into_bullets(body)
        if len(bullets) > 1:
            items_html = "".join(f"<li>{b}</li>" for b in bullets)
            st.markdown(
                f'<ul class="jd-bullets">{items_html}</ul>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<p class="jd-plain">{body.capitalize()}</p>',
                unsafe_allow_html=True,
            )
