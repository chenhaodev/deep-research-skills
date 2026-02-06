# Citation Standards

## Inline Citation Format

Use numbered citations in square brackets: `[N]` where N is the reference number.

### Examples

```markdown
Recent studies have shown significant improvements in outcomes [1, 2]. However, some researchers argue that methodological limitations persist [3].

A meta-analysis of 15 RCTs [4] found that...
```

### Multiple Citations
- Consecutive: `[1, 2, 3]` or `[1-3]`
- Non-consecutive: `[1, 5, 9]`

## Bibliography Format

### Standard Format

```
[N] Author(s). (Year). Title. Journal Name, Volume(Issue), pages. DOI: 10.xxxx/xxxxx
```

### Components

1. **[N]**: Reference number (matches inline citation)
2. **Author(s)**: 
   - Single author: `Smith J.`
   - Two authors: `Smith J, Jones A.`
   - Three or more: `Smith J, Jones A, Brown C.` or `Smith J, et al.` if >5 authors
3. **Year**: Publication year in parentheses
4. **Title**: Full paper title (no quotes)
5. **Journal**: Italicized or *marked* journal name
6. **Volume(Issue)**: Volume number, issue in parentheses if available
7. **Pages**: Page range (optional if DOI present)
8. **DOI**: Digital Object Identifier (preferred) or PubMed ID (PMID:)

### Examples

**Journal Article:**
```
[1] Johnson M, Smith R, Lee K. (2023). Deep learning approaches for medical image analysis. Nature Medicine, 29(4), 445-456. DOI: 10.1038/s41591-023-02345-6
```

**Meta-Analysis:**
```
[2] Chen H, et al. (2022). Effectiveness of telemedicine interventions: a systematic review and meta-analysis. JAMA Network Open, 5(8), e2226505. DOI: 10.1001/jamanetworkopen.2022.26505
```

**Systematic Review:**
```
[3] Williams A, Brown J. (2024). Home-based rehabilitation technologies: a systematic review. Cochrane Database of Systematic Reviews, 2024(1), CD013456. DOI: 10.1002/14651858.CD013456.pub2
```

**PubMed Only (no DOI):**
```
[4] Zhang Y, Liu X. (2021). Sensor-based fall detection in elderly care. Journal of Medical Systems, 45(6), 78. PMID: 33987654
```

**Semantic Scholar ID (no DOI/PMID):**
```
[5] Taylor R. (2020). Machine learning in healthcare: current applications. arXiv preprint. S2ID: 218487234
```

## Quality Badges

Add badges after the citation to indicate study quality:

- **[RCT]**: Randomized Controlled Trial
- **[Meta]**: Meta-Analysis
- **[SR]**: Systematic Review
- **[Highly Cited]**: >100 citations
- **[Rigorous Journal]**: Top-tier journal (>10k journal citations)

### Example with Badges

```
[1] Johnson M, et al. (2023). Deep learning for diagnostics. Nature Medicine, 29(4), 445-456. DOI: 10.1038/s41591-023-02345-6 [RCT] [Highly Cited] [Rigorous Journal]
```

## Citation Sorting

In the References section, citations should be ordered:
1. Numerically (as they appear in text)
2. OR alphabetically by first author (with renumbering)

**Prefer numerical order** for easier reader navigation.

## Extraction from API Responses

### Semantic Scholar Response Mapping

```python
citation = {
    "number": index + 1,
    "authors": [f"{a['name']}" for a in paper['authors']],
    "year": paper['year'],
    "title": paper['title'],
    "journal": paper['venue'] or "arXiv preprint",
    "doi": paper.get('externalIds', {}).get('DOI'),
    "s2id": paper['paperId'],
    "citations_count": paper['citationCount'],
}
```

### PubMed Response Mapping

```python
citation = {
    "number": index + 1,
    "authors": extract_authors_from_xml(xml),
    "year": extract_year_from_xml(xml),
    "title": extract_title_from_xml(xml),
    "journal": extract_journal_from_xml(xml),
    "volume": extract_volume_from_xml(xml),
    "issue": extract_issue_from_xml(xml),
    "pages": extract_pages_from_xml(xml),
    "pmid": paper['pmid'],
    "doi": extract_doi_from_xml(xml),
}
```

## Special Cases

### Preprints (arXiv, medRxiv, bioRxiv)

```
[N] Author(s). (Year). Title. Preprint posted on Platform. DOI or URL.
```

Example:
```
[6] Kumar S, et al. (2024). Novel approach to drug discovery. Preprint posted on bioRxiv. DOI: 10.1101/2024.01.15.575234
```

### Conference Papers

```
[N] Author(s). (Year). Title. In: Conference Name, Location. Pages. DOI.
```

### Missing Information

- **No DOI/PMID**: Use Semantic Scholar ID: `S2ID: xxxxxxx`
- **No year**: Use `(n.d.)` for "no date"
- **No journal**: Use `Unpublished manuscript` or `Preprint`
- **No authors**: Use `Anonymous` or `[Author names not available]`
