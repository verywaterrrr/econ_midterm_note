# ECON2103 Midterm — Checklist Edition

A Traditional Chinese / English study website ordered exactly by the original midterm checklist.

- 117 individual lessons: 112 chapter items and five final MCQ checks.
- Every item has an explanation, one worked example, and one practice question with answer feedback.
- Chapters 1–8, 14 and 15 remain separate, with previous/next navigation through the entire checklist.
- 24 original SVG diagrams replace the previous text sketches.
- Review flags, answers and resume position are saved locally in the browser.

## Build and preview

Python 3 is the only build dependency:

    python3 generate_graphs.py
    python3 build.py
    python3 -m http.server 8765 --directory dist

Content files align one-to-one with the checkboxes in content/checklist.md. The build checks item counts; validate.py checks exact objective order, per-item content, graph files and links.

GitHub Pages publishes the dist folder using the included workflow.

The site contains independently written study material; instructor slide decks and problem-set PDFs are not redistributed. It is not an official course resource. A single practice answer does not establish mastery.
