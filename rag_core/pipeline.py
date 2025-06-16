from rag_core.genai import call_gemini_api
from rag_core.embeddings import embed_query
from rag_core.qdrant import search_qdrant
from rag_core.fmp_api import fetch_integrated_annual_report

def decompose_query(query: str):
    prompt = (
        "Decompose the following complex financial query into a list of simpler sub-questions. "
        "Provide a clear, step-by-step breakdown.\n\n"
        f"Query: {query}\n\nDecomposition:"
    )
    decomposition_text = call_gemini_api(prompt)
    subqueries = [line.strip() for line in decomposition_text.splitlines() if line.strip()]
    return subqueries, decomposition_text

def generate_answer(query: str, context: list, integrated_report: dict):
    context_text = ""
    for idx, doc in enumerate(context):
        comp = doc.get("company", {})
        header = doc.get("header", "")
        content = doc.get("content", "")
        company_name = comp.get("companyName", "Unknown")
        collection = doc.get("collection", "Unknown Collection")
        context_text += f"Document {idx + 1} [Collection: {collection}, Company: {company_name}, Section: {header}]:\n{content}\n\n"
    integrated_text = "Integrated Annual Report Data:\n"
    for section, data in integrated_report.items():
        integrated_text += f"{section.capitalize()}:\n{data}\n\n"
    system_prompt = (
        "You are a financial analysis assistant. Answer the following question based only on the provided context. "
        "If the context does not have enough details, give content related to the data given. "
        "Provide your answer as a well-structured paragraph that integrates all the key details in a coherent narrative, "
        "rather than as a table. Referencing to the content is not needed, respond as if you are responding on your own."
    )
    full_prompt = (
        f"{system_prompt}\n\nQuestion: {query}\n\n"
        f"Context from Qdrant:\n{context_text}\n\n"
        f"{integrated_text}"
    )
    return call_gemini_api(full_prompt, max_tokens=2048)

def rag_with_decomposition(query: str, company_filter: str = "") -> dict:
    subqueries, decomposition_text = decompose_query(query)
    filter_params = {}
    if company_filter:
        filter_params["company.companyName"] = company_filter
    query_vector = embed_query(query)
    qdrant_results = search_qdrant(query_vector, top_k=5, filter_params=filter_params)
    company_symbol = "AAPL"
    if qdrant_results and qdrant_results[0].get("company", {}).get("symbol"):
        company_symbol = qdrant_results[0]["company"]["symbol"]
    integrated_report = fetch_integrated_annual_report(company_symbol)
    final_answer = generate_answer(query, qdrant_results, integrated_report)
    return {
        "Query": query,
        "Query Decomposition": decomposition_text,
        "Sub-queries": subqueries,
        "Qdrant Results": qdrant_results,
        "Integrated Annual Report": integrated_report,
        "Final Answer": final_answer
    }
