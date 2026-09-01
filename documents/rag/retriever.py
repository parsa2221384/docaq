from .vector_store import vector_store


# MMR (Maximal Marginal Relevance) fetches a wider candidate pool and then
# picks results that are relevant *and* different from each other. Plain
# similarity search often returns five near-identical chunks, which wastes
# the context window without adding information.
#
#   fetch_k       — candidates pulled from Chroma before re-ranking
#   k             — passages actually sent to the LLM
#   lambda_mult   — 1.0 = pure relevance, 0.0 = pure diversity
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.6,
    },
)