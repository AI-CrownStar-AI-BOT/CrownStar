# CrownStar Cognitive Model – Formal Description

Let $Q$ be a query. The engine performs:

$$
\text{Harvest}(Q) = \bigcup_{d \in \text{extractDomains}(Q)} \text{crawl}(d)
$$

Let $T$ be the multiset of tokenised texts. The **Gamma Burst** filter selects top $k$ sentences:

$$
\Gamma(T, Q) = \underset{s \in T}{\mathrm{top\_k}}\; \mathrm{relevance}(s, Q)
$$

A **second‑order Markov chain** $M$ with transition probabilities $P(w_{i+2} | w_i, w_{i+1})$ generates output $\hat{Y}$:

$$
\hat{Y} = \arg\max_{y} \prod_{t} P(y_{t+2} | y_t, y_{t+1})
$$
