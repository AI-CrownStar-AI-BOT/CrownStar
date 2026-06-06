# CrownStar v5.0.5 – Model Documentation

This document provides a complete mathematical description of the CrownStar cognitive engine.

---

## 1. Live Harvesting

Given a query `Q`, CrownStar extracts all domain names using the regular expression `\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b`. For each domain `d`, it performs:

- DNS `TXT` record lookup
- HTTP GET to `https://{d}` (extracts visible text)
- Wikipedia API summary for the main term in `d`

The harvested text is the union:

$$
\text{Harvest}(Q) = \bigcup_{d \in \text{extractDomains}(Q)} \text{crawl}(d)
$$

---

## 2. Relevance Filter (Semantic Intensity)

Harvested sentences are embedded into a sparse TF‑IDF vector space of dimension 4096. Each sentence is assigned to one of **7 attention zones** by:

$$
\text{zone}(s) = \text{hash}(\arg\max_{t \in s} \text{tfidf}(t)) \bmod 7
$$

The angular position of each zone evolves via Wolfram’s Rule 30:

$$
\theta_z(t+1) = \theta_z(t) + (\text{Rule30}(ca\_state) \bmod 360) \quad [\text{radians}]
$$

When a zone’s angle aligns with one of its 5 directional paths, a relevance spike occurs. The intensity is:

$$
I = \sigma(r) \cdot \left(1 - \frac{|\theta - \pi|}{\pi}\right)
$$

where:

$$
\sigma(r) = \frac{1}{1 + e^{-\alpha (r - R_{\text{shoulder}})}}
$$

with hyperparameters:

- \( \alpha = 2.3 \) (steepness)
- \( R_{\text{shoulder}} = 0.65 \) (midpoint)

Only sentences with \( I > 0.33 \) survive.

---

## 3. Third‑Order Markov Chain

The filtered text trains a trigram model. The conditional probability of the next word is:

$$
P(w_{t+3} \mid w_t, w_{t+1}, w_{t+2}) =
\frac{\text{count}(w_t, w_{t+1}, w_{t+2}, w_{t+3})}
{\text{count}(w_t, w_{t+1}, w_{t+2})}
$$

Generation is temperature‑controlled (temperature = 0.85). The final answer maximises the product:

$$
\hat{Y} = \arg\max_y \prod_{t} P(y_{t+3} \mid y_t, y_{t+1}, y_{t+2})
$$

Maximum output length: 60 words (trimmed to tier limits).

---

## 4. Persistent Memory

All conversations are stored in a local SQLite database. When answering, CrownStar performs a similarity search (cosine similarity threshold 0.7) over past embeddings and boosts relevant memories by:

$$
M = \sum_{\text{conversations}} e^{-\lambda \Delta t}
$$

with \( \lambda = 0.05 \) per hour. This recency weighting ensures recent interactions have higher influence.

---

## 5. Tier Limits

| Tier | Input (chars) | Output (chars) | File Upload |
|------|---------------|----------------|--------------|
| Free | 500,000 | 100,000,000 | 500 MB |
| Basic | 1,000,000 | 200,000,000 | 1 GB |
| Pro | 2,000,000 | 500,000,000 | 2 GB |
| Enterprise | 5,000,000 | 1,000,000,000 | 5 GB |

---

## 6. Amenities (Enterprise Tier)

55+ amenities are implemented as local JavaScript modules or free API calls with robust fallbacks. They do not require external accounts.

---

*For implementation details, see the source code in `src/`.*