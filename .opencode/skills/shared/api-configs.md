# API Configuration Reference

## Qwen3 Max API

### Endpoints

**Primary (OpenRouter):**
```
Base URL: https://openrouter.ai/api/v1
Model: qwen/qwen3-max
```

**Alternative (Novita AI):**
```
Base URL: https://api.novita.ai/openai
Model: qwen/qwen3-max
```

### Authentication

```yaml
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json
```

### Rate Limits

- **Tokens per minute**: 500
- **Requests per minute**: 600,000
- **Context window**: 256,000 tokens
- **Max output**: 65,536 tokens

### Pricing (Tiered by Input Length)

| Input Tokens | Input Price ($/M) | Output Price ($/M) |
|--------------|------------------|-------------------|
| 0 - 32,768 | $0.845 | $3.38 |
| 32,769 - 131,072 | $1.40 | $5.64 |
| 131,073 - 258,048 | $2.11 | $8.45 |

### Request Format (OpenAI-Compatible)

```json
{
  "model": "qwen/qwen3-max",
  "messages": [
    {"role": "system", "content": "You are a helpful research assistant."},
    {"role": "user", "content": "Analyze this paper abstract..."}
  ],
  "max_tokens": 4096,
  "temperature": 0.7,
  "response_format": {"type": "json_object"}
}
```

### Error Codes

- **401**: Invalid API key
- **429**: Rate limit exceeded (implement exponential backoff)
- **503**: Service unavailable (retry after 60s)

### Recommended Settings

**For consensus analysis (deterministic):**
```yaml
temperature: 0.2
max_tokens: 512
```

**For synthesis (creative):**
```yaml
temperature: 0.7
max_tokens: 4096
```

---

## Semantic Scholar API

### Endpoints

**Base URL:** `https://api.semanticscholar.org/graph/v1`

**Key Endpoints:**
- Search: `/paper/search`
- Get paper: `/paper/{paperId}`
- Citations: `/paper/{paperId}/citations`
- References: `/paper/{paperId}/references`
- Batch: `/paper/batch`

### Authentication

```yaml
Headers:
  x-api-key: {API_KEY}  # Optional but recommended for higher rate limits
```

### Rate Limits

**Without API key:**
- 100 requests per 5 minutes

**With API key:**
- 1 request per second (sustained)
- Burst: up to 10 requests per second (short duration)

### Request Parameters

**Search:**
```
GET /paper/search?query={query}&offset={offset}&limit={limit}&fields={fields}
```

**Available Fields:**
```
paperId, title, abstract, year, authors, venue, citationCount, referenceCount, 
externalIds, url, publicationTypes, publicationDate, journal, fieldsOfStudy
```

**Recommended Fields:**
```
fields=paperId,title,abstract,year,authors,venue,citationCount,externalIds,url,publicationTypes
```

### Pagination

```
offset: Start from result N (default: 0)
limit: Return up to N results (max: 100, default: 10)
```

For 1000 results: 10 requests with `limit=100` and `offset=0,100,200,...,900`

### Example Response

```json
{
  "data": [
    {
      "paperId": "649def34f8be52c8b66281af98ae884c09aef38b",
      "title": "BERT: Pre-training of Deep Bidirectional Transformers",
      "abstract": "We introduce a new language representation model...",
      "year": 2019,
      "authors": [
        {"authorId": "40348915", "name": "Jacob Devlin"}
      ],
      "venue": "NAACL",
      "citationCount": 45234,
      "externalIds": {"DOI": "10.18653/v1/N19-1423", "ArXiv": "1810.04805"}
    }
  ],
  "total": 1234,
  "offset": 0
}
```

---

## PubMed E-utilities API

### Endpoints

**Base URL:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

**Key E-utilities:**
- **ESearch**: `esearch.fcgi` (search, returns PMIDs)
- **EFetch**: `efetch.fcgi` (fetch full records)
- **ESummary**: `esummary.fcgi` (fetch summaries)

### Authentication

```yaml
Query Parameters:
  api_key: {NCBI_API_KEY}  # Optional but recommended
  email: {YOUR_EMAIL}      # Required for courtesy
```

### Rate Limits

**Without API key:**
- 3 requests per second

**With API key:**
- 10 requests per second

### ESearch Request

```
GET /esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retstart={offset}&retmode=json
```

**Query Syntax:**
```
term=machine+learning+AND+healthcare[Title]
term=diabetes[MeSH]+AND+2020:2024[PDAT]
term=systematic+review[PT]+AND+cancer
```

**Response:**
```json
{
  "esearchresult": {
    "count": "1234",
    "idlist": ["34567890", "34567891", "34567892"],
    "querytranslation": "machine learning[All Fields] AND healthcare[Title]"
  }
}
```

### EFetch Request

```
GET /efetch.fcgi?db=pubmed&id={pmid_list}&retmode=xml&rettype=abstract
```

**Parameters:**
- `id`: Comma-separated PMIDs (max 200 per request)
- `retmode`: xml, json (xml has more complete data)
- `rettype`: abstract, full

**XML Structure:**
```xml
<PubmedArticle>
  <MedlineCitation>
    <PMID>34567890</PMID>
    <Article>
      <ArticleTitle>Paper Title Here</ArticleTitle>
      <Abstract>
        <AbstractText>Abstract text...</AbstractText>
      </Abstract>
      <AuthorList>
        <Author>
          <LastName>Smith</LastName>
          <ForeName>John</ForeName>
        </Author>
      </AuthorList>
      <Journal>
        <Title>Journal Name</Title>
      </Journal>
      <ArticleDate>
        <Year>2023</Year>
      </ArticleDate>
    </Article>
  </MedlineCitation>
</PubmedArticle>
```

### Recommended Settings

**For broad search:**
```yaml
retmax: 100
sort: relevance
```

**For recent papers:**
```yaml
retmax: 50
sort: date
filter: 2020:2024[PDAT]
```

---

## Default Configuration Template

**~/.deep-research/config.yaml**

```yaml
qwen:
  api_key: ${DEEP_RESEARCH_QWEN_API_KEY}
  base_url: "https://openrouter.ai/api/v1"
  model: "qwen/qwen3-max"
  timeout: 60
  max_retries: 3

semantic_scholar:
  api_key: ${DEEP_RESEARCH_S2_API_KEY}  # Optional
  timeout: 30
  max_retries: 3

pubmed:
  api_key: ${DEEP_RESEARCH_PUBMED_API_KEY}  # Optional
  email: ${DEEP_RESEARCH_EMAIL}  # Required
  timeout: 30
  max_retries: 3

cache:
  path: "~/.deep-research/cache.db"
  ttl_days: 30
  enabled: true

search:
  max_papers_per_query: 100
  max_searches_per_review: 25
  relevance_threshold: 0.6
  min_abstract_words: 50
  date_range_years: 3

logging:
  level: "INFO"
  file: "~/.deep-research/logs/deep-research.log"
  max_size_mb: 10
  backup_count: 3
```
