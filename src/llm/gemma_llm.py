"""Gemma LLM wrapper using OpenAI-compatible API (llama-server).

Connects to a local llama-server running Gemma 4 (or any compatible model)
via the OpenAI chat completions API at http://localhost:8080/v1.

Start the server with:
    llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q4_K_M

Falls back to a keyword-based mock when the server is not running.
"""

from src.config import LLM_API_BASE, LLM_MODEL_NAME, LLM_TEMPERATURE

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class GemmaLLM:
    """Wrapper for Gemma via llama-server OpenAI-compatible API."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = base_url or LLM_API_BASE
        self.model = model or LLM_MODEL_NAME
        self.client = None

        if HAS_OPENAI:
            try:
                self.client = OpenAI(base_url=self.base_url, api_key="not-needed")
                self.client.models.list()
                print(f"Connected to LLM server at {self.base_url}")
            except Exception as e:
                print(f"[MockLLM] Could not connect to LLM server at {self.base_url}: {e}")
                print("[MockLLM] Start the server with: llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q4_K_M")
                self.client = None
        else:
            print("[MockLLM] openai package not installed. Using mock.")

    def generate(
        self,
        prompt: str,
        system_prompt: str = "You are a senior M&A due diligence analyst.",
        max_tokens: int = 1024,
        temperature: float | None = None,
    ) -> str:
        """Generate a response from the model."""
        if self.client is None:
            return self._mock_generate(prompt, system_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature if temperature is not None else LLM_TEMPERATURE,
            )
            return response.choices[0].message.content
        except Exception:
            return self._mock_generate(prompt, system_prompt)

    def generate_with_tools(
        self,
        prompt: str,
        tools: list[dict],
        system_prompt: str = "You are a senior M&A due diligence analyst.",
        max_tokens: int = 1024,
    ) -> dict:
        """Generate a response with tool/function calling support."""
        if self.client is None:
            return {"content": self._mock_generate(prompt, system_prompt)}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                tools=tools,
                max_tokens=max_tokens,
                temperature=LLM_TEMPERATURE,
            )
            msg = response.choices[0].message
            return {"content": msg.content, "tool_calls": getattr(msg, "tool_calls", None)}
        except Exception:
            return {"content": self._mock_generate(prompt, system_prompt)}

    def classify_intent(self, query: str) -> str:
        """Classify a user query into a legal due diligence query type."""
        if self.client is None:
            return self._mock_classify(query)

        system = """Classify the user's legal due diligence query into exactly one category.
Reply with ONLY the category name, nothing else.

Categories:
- document_search: Finding specific M&A documents, filings, or correspondence
- risk_assessment: Questions about litigation exposure, financial risk, or regulatory risk
- entity_lookup: Questions about specific companies, products, people, or their relationships
- clause_comparison: Comparing contract terms, indemnification clauses, or liability provisions
- gap_analysis: Identifying what's missing from due diligence, coverage gaps, or blind spots"""

        result = self.generate(query, system_prompt=system, max_tokens=512, temperature=0.1)
        result = result.strip().lower().replace(" ", "_")
        valid = {"document_search", "risk_assessment", "entity_lookup",
                 "clause_comparison", "gap_analysis"}
        return result if result in valid else "document_search"

    def extract_entities(self, text: str, language: str = "en") -> dict:
        """Extract legal entities from M&A due diligence text."""
        if self.client is None:
            return {"companies": [], "products": [], "risk_factors": [],
                    "regulatory_bodies": [], "monetary_values": []}

        system = """Extract legal entities from the M&A due diligence text.
Return a JSON object with these keys:
- companies: list of company names mentioned
- products: list of product names
- risk_factors: list of risk factors or legal issues
- regulatory_bodies: list of regulatory agencies
- monetary_values: list of monetary amounts mentioned

Return ONLY valid JSON, no explanation."""

        result = self.generate(
            f"Language: {language}\n\nText: {text}",
            system_prompt=system,
            max_tokens=2048,
            temperature=0.1,
        )
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"companies": [], "products": [], "risk_factors": [],
                    "regulatory_bodies": [], "monetary_values": []}

    def generate_cypher(self, question: str, schema: str) -> str:
        """Generate a Cypher query from natural language."""
        if self.client is None:
            return self._mock_cypher(question)

        system = f"""You are a graph database expert. Generate a Cypher query for FalkorDB
to answer the user's question about M&A due diligence documents.

Graph schema:
{schema}

Return ONLY the Cypher query, no explanation. Use MATCH, WHERE, RETURN clauses."""

        result = self.generate(question, system_prompt=system, max_tokens=1024, temperature=0.1)
        result = result.strip()
        if result.startswith("```"):
            lines = result.split("\n")
            result = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        return result.strip()

    # --- Mock methods for testing without LLM ---

    def _mock_classify(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["risk", "exposure", "liability", "litigation", "lawsuit", "haftung"]):
            return "risk_assessment"
        if any(w in q for w in ["entity", "company", "monsanto", "bayer", "roundup", "glyphosate", "glyphosat"]):
            return "entity_lookup"
        if any(w in q for w in ["clause", "indemnif", "contract", "provision", "compare", "vergleich", "klausel"]):
            return "clause_comparison"
        if any(w in q for w in ["gap", "missing", "blind spot", "coverage", "fehlt", "luecke"]):
            return "gap_analysis"
        return "document_search"

    def _mock_generate(self, prompt: str, system_prompt: str) -> str:
        return (
            "[MockLLM Response] Based on the available M&A due diligence data, "
            "the analysis shows cross-lingual results from US and German jurisdictions. "
            "The Harrier embedding model successfully retrieved relevant documents "
            "across languages without translation. Start llama-server for full "
            "LLM-powered analysis: llama-server -hf ggml-org/gemma-4-E2B-it-GGUF:Q4_K_M"
        )

    def _mock_cypher(self, question: str) -> str:
        q = question.lower()
        if "claim" in q or "lawsuit" in q or "litigation" in q:
            return (
                "MATCH (l:LegalClaim)-[:FILED_AGAINST]->(c:Company) "
                "RETURN l.case_name AS claim, c.name AS defendant, "
                "l.monetary_value AS value, l.status AS status "
                "ORDER BY l.monetary_value DESC LIMIT 20"
            )
        if "risk" in q or "risiko" in q:
            return (
                "MATCH (d:Document)-[:DISCLOSES]->(rf:RiskFactor) "
                "RETURN rf.name AS risk, rf.category AS category, "
                "rf.severity AS severity, count(d) AS documents "
                "ORDER BY documents DESC"
            )
        if "roundup" in q or "glyphosate" in q or "glyphosat" in q:
            return (
                "MATCH (p:Product {name: 'Roundup'})<-[:TARGETS]-(l:LegalClaim) "
                "RETURN l.case_name AS claim, l.claim_type AS type, "
                "l.monetary_value AS value, l.status AS status "
                "ORDER BY l.monetary_value DESC"
            )
        return (
            "MATCH (d:Document) "
            "RETURN d.id AS id, d.title AS title, d.language AS language, "
            "d.jurisdiction AS jurisdiction "
            "LIMIT 20"
        )
