"""FalkorDBLite embedded graph store for M&A due diligence knowledge graph."""

from redislite import FalkorDB

from src.config import FALKORDB_PATH


GRAPH_SCHEMA = """
Node types:
- Company: name, jurisdiction, role (acquirer|target|subsidiary)
- Document: id, title, summary, language, doc_type, jurisdiction, date, monetary_value, confidentiality
- LegalClaim: case_name, claim_type, status, jurisdiction, filing_date, monetary_value
- Product: name, category, active_ingredient
- Chemical: name, cas_number, classification
- RegulatoryBody: name, jurisdiction, authority_type
- RiskFactor: name, category (litigation|regulatory|financial|reputational|environmental), severity (low|medium|high|critical)
- ContractClause: clause_type, summary, language

Relationships:
- (Document)-[:MENTIONS]->(Company)
- (Document)-[:CONTAINS]->(ContractClause)
- (Document)-[:DISCLOSES]->(RiskFactor)
- (LegalClaim)-[:TARGETS]->(Product)
- (LegalClaim)-[:FILED_AGAINST]->(Company)
- (Company)-[:ACQUIRED {date, value}]->(Company)
- (Document)-[:SIMILAR_TO {score, cross_lingual}]->(Document)
- (RegulatoryBody)-[:INVESTIGATES {status}]->(Product)
- (Document)-[:REFERENCES]->(Document)
- (Product)-[:CONTAINS_CHEMICAL]->(Chemical)
- (Chemical)-[:LINKED_TO]->(RiskFactor)
- (LegalClaim)-[:ALLEGES]->(RiskFactor)
- (Company)-[:MANUFACTURES]->(Product)
- (Entity)-[:ALSO_KNOWN_AS]->(Entity)
"""


class GraphStore:
    """FalkorDBLite embedded graph store — no server needed."""

    def __init__(self, path: str | None = None):
        import os
        db_dir = path or FALKORDB_PATH
        os.makedirs(db_dir, exist_ok=True)
        db_file = os.path.join(db_dir, "lexbridge.db")
        self.db = FalkorDB(db_file)
        self.graph = self.db.select_graph("lexbridge")
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Create indexes for fast lookups."""
        try:
            self.graph.query("CREATE INDEX FOR (c:Company) ON (c.name)")
            self.graph.query("CREATE INDEX FOR (d:Document) ON (d.id)")
            self.graph.query("CREATE INDEX FOR (l:LegalClaim) ON (l.case_name)")
            self.graph.query("CREATE INDEX FOR (p:Product) ON (p.name)")
            self.graph.query("CREATE INDEX FOR (ch:Chemical) ON (ch.name)")
            self.graph.query("CREATE INDEX FOR (r:RegulatoryBody) ON (r.name)")
            self.graph.query("CREATE INDEX FOR (rf:RiskFactor) ON (rf.name)")
            self.graph.query("CREATE INDEX FOR (cc:ContractClause) ON (cc.clause_type)")
        except Exception:
            pass  # Indexes may already exist

    # --- Node creation methods ---

    def add_company(self, name: str, jurisdiction: str = "", role: str = ""):
        """Add a company node (skip if exists)."""
        self.graph.query(
            """MERGE (c:Company {name: $name})
            ON CREATE SET c.jurisdiction = $jur, c.role = $role""",
            params={"name": name, "jur": jurisdiction, "role": role},
        )

    def add_document(self, doc: dict):
        """Add a document node."""
        self.graph.query(
            """CREATE (d:Document {
                id: $id, title: $title, summary: $summary,
                language: $language, doc_type: $doc_type,
                jurisdiction: $jurisdiction, date: $date,
                monetary_value: $monetary_value,
                confidentiality: $confidentiality
            })""",
            params={
                "id": doc["id"],
                "title": doc["title"],
                "summary": doc.get("summary", ""),
                "language": doc["language"],
                "doc_type": doc["doc_type"],
                "jurisdiction": doc["jurisdiction"],
                "date": doc.get("date", ""),
                "monetary_value": doc.get("monetary_value", 0),
                "confidentiality": doc.get("confidentiality", ""),
            },
        )

    def add_legal_claim(self, case_name: str, claim_type: str = "", status: str = "",
                        jurisdiction: str = "", filing_date: str = "", monetary_value: float = 0):
        """Add a legal claim node."""
        self.graph.query(
            """MERGE (l:LegalClaim {case_name: $name})
            ON CREATE SET l.claim_type = $type, l.status = $status,
                          l.jurisdiction = $jur, l.filing_date = $date,
                          l.monetary_value = $value""",
            params={"name": case_name, "type": claim_type, "status": status,
                    "jur": jurisdiction, "date": filing_date, "value": monetary_value},
        )

    def add_product(self, name: str, category: str = "", active_ingredient: str = ""):
        """Add a product node (skip if exists)."""
        self.graph.query(
            """MERGE (p:Product {name: $name})
            ON CREATE SET p.category = $cat, p.active_ingredient = $ai""",
            params={"name": name, "cat": category, "ai": active_ingredient},
        )

    def add_chemical(self, name: str, cas_number: str = "", classification: str = ""):
        """Add a chemical node (skip if exists)."""
        self.graph.query(
            """MERGE (ch:Chemical {name: $name})
            ON CREATE SET ch.cas_number = $cas, ch.classification = $cls""",
            params={"name": name, "cas": cas_number, "cls": classification},
        )

    def add_regulatory_body(self, name: str, jurisdiction: str = "", authority_type: str = ""):
        """Add a regulatory body node (skip if exists)."""
        self.graph.query(
            """MERGE (r:RegulatoryBody {name: $name})
            ON CREATE SET r.jurisdiction = $jur, r.authority_type = $type""",
            params={"name": name, "jur": jurisdiction, "type": authority_type},
        )

    def add_risk_factor(self, name: str, category: str = "", severity: str = ""):
        """Add a risk factor node (skip if exists)."""
        self.graph.query(
            """MERGE (rf:RiskFactor {name: $name})
            ON CREATE SET rf.category = $cat, rf.severity = $sev""",
            params={"name": name, "cat": category, "sev": severity},
        )

    def add_contract_clause(self, clause: dict):
        """Add a contract clause node."""
        self.graph.query(
            """MERGE (cc:ContractClause {clause_type: $type})
            ON CREATE SET cc.summary = $summary, cc.language = $lang""",
            params={
                "type": clause.get("clause_type", ""),
                "summary": clause.get("summary", ""),
                "lang": clause.get("language", ""),
            },
        )

    # --- Relationship creation methods ---

    def link_document_company(self, doc_id: str, company_name: str):
        """Create MENTIONS relationship."""
        self.graph.query(
            """MATCH (d:Document {id: $did}), (c:Company {name: $cname})
            MERGE (d)-[:MENTIONS]->(c)""",
            params={"did": doc_id, "cname": company_name},
        )

    def link_document_clause(self, doc_id: str, clause_type: str):
        """Create CONTAINS relationship."""
        self.graph.query(
            """MATCH (d:Document {id: $did}), (cc:ContractClause {clause_type: $ct})
            MERGE (d)-[:CONTAINS]->(cc)""",
            params={"did": doc_id, "ct": clause_type},
        )

    def link_document_risk(self, doc_id: str, risk_name: str):
        """Create DISCLOSES relationship."""
        self.graph.query(
            """MATCH (d:Document {id: $did}), (rf:RiskFactor {name: $rname})
            MERGE (d)-[:DISCLOSES]->(rf)""",
            params={"did": doc_id, "rname": risk_name},
        )

    def link_claim_product(self, case_name: str, product_name: str):
        """Create TARGETS relationship."""
        self.graph.query(
            """MATCH (l:LegalClaim {case_name: $cname}), (p:Product {name: $pname})
            MERGE (l)-[:TARGETS]->(p)""",
            params={"cname": case_name, "pname": product_name},
        )

    def link_claim_company(self, case_name: str, company_name: str):
        """Create FILED_AGAINST relationship."""
        self.graph.query(
            """MATCH (l:LegalClaim {case_name: $cname}), (c:Company {name: $comp})
            MERGE (l)-[:FILED_AGAINST]->(c)""",
            params={"cname": case_name, "comp": company_name},
        )

    def link_claim_risk(self, case_name: str, risk_name: str):
        """Create ALLEGES relationship."""
        self.graph.query(
            """MATCH (l:LegalClaim {case_name: $cname}), (rf:RiskFactor {name: $rname})
            MERGE (l)-[:ALLEGES]->(rf)""",
            params={"cname": case_name, "rname": risk_name},
        )

    def link_acquisition(self, acquirer: str, target: str, date: str = "", value: float = 0):
        """Create ACQUIRED relationship."""
        self.graph.query(
            """MATCH (a:Company {name: $acq}), (t:Company {name: $tgt})
            MERGE (a)-[:ACQUIRED {date: $date, value: $value}]->(t)""",
            params={"acq": acquirer, "tgt": target, "date": date, "value": value},
        )

    def link_similar_documents(self, doc1_id: str, doc2_id: str, score: float, cross_lingual: bool = False):
        """Create SIMILAR_TO relationship between documents."""
        self.graph.query(
            """MATCH (d1:Document {id: $d1}), (d2:Document {id: $d2})
            MERGE (d1)-[:SIMILAR_TO {score: $score, cross_lingual: $xl}]->(d2)""",
            params={"d1": doc1_id, "d2": doc2_id, "score": score, "xl": cross_lingual},
        )

    def link_regulatory_investigation(self, body_name: str, product_name: str, status: str = ""):
        """Create INVESTIGATES relationship."""
        self.graph.query(
            """MATCH (r:RegulatoryBody {name: $rname}), (p:Product {name: $pname})
            MERGE (r)-[:INVESTIGATES {status: $status}]->(p)""",
            params={"rname": body_name, "pname": product_name, "status": status},
        )

    def link_document_reference(self, doc1_id: str, doc2_id: str):
        """Create REFERENCES relationship between documents."""
        self.graph.query(
            """MATCH (d1:Document {id: $d1}), (d2:Document {id: $d2})
            MERGE (d1)-[:REFERENCES]->(d2)""",
            params={"d1": doc1_id, "d2": doc2_id},
        )

    def link_product_chemical(self, product_name: str, chemical_name: str):
        """Create CONTAINS_CHEMICAL relationship."""
        self.graph.query(
            """MATCH (p:Product {name: $pname}), (ch:Chemical {name: $cname})
            MERGE (p)-[:CONTAINS_CHEMICAL]->(ch)""",
            params={"pname": product_name, "cname": chemical_name},
        )

    def link_chemical_risk(self, chemical_name: str, risk_name: str):
        """Create LINKED_TO relationship."""
        self.graph.query(
            """MATCH (ch:Chemical {name: $cname}), (rf:RiskFactor {name: $rname})
            MERGE (ch)-[:LINKED_TO]->(rf)""",
            params={"cname": chemical_name, "rname": risk_name},
        )

    def link_company_product(self, company_name: str, product_name: str):
        """Create MANUFACTURES relationship."""
        self.graph.query(
            """MATCH (c:Company {name: $cname}), (p:Product {name: $pname})
            MERGE (c)-[:MANUFACTURES]->(p)""",
            params={"cname": company_name, "pname": product_name},
        )

    def link_entity_alias(self, canonical: str, local_name: str):
        """Create ALSO_KNOWN_AS for cross-lingual entity resolution.

        Works across node types by matching on name property.
        """
        self.graph.query(
            """MATCH (a {name: $canonical}), (b {name: $local})
            MERGE (a)-[:ALSO_KNOWN_AS]->(b)""",
            params={"canonical": canonical, "local": local_name},
        )

    # --- Query methods ---

    def query(self, cypher: str, params: dict | None = None) -> list[dict]:
        """Execute a Cypher query and return results as list of dicts."""
        result = self.graph.query(cypher, params=params or {})
        if not result.result_set:
            return []
        headers = result.header
        return [
            {h[1]: row[i] for i, h in enumerate(headers)}
            for row in result.result_set
        ]

    def get_company_subgraph(self, company_name: str) -> list[dict]:
        """Get all relationships for a company."""
        return self.query(
            """MATCH (c:Company {name: $name})-[r]-(n)
            RETURN type(r) AS relationship, labels(n)[0] AS node_type,
                   n.name AS name, properties(r) AS props
            LIMIT 30""",
            params={"name": company_name},
        )

    def get_product_claims(self, product_name: str) -> list[dict]:
        """Get all claims targeting a product."""
        return self.query(
            """MATCH (l:LegalClaim)-[:TARGETS]->(p:Product {name: $name})
            RETURN l.case_name AS claim, l.claim_type AS type,
                   l.status AS status, l.monetary_value AS value
            ORDER BY l.monetary_value DESC""",
            params={"name": product_name},
        )

    def get_risk_factors_by_category(self) -> list[dict]:
        """Get risk factors grouped by category."""
        return self.query(
            """MATCH (rf:RiskFactor)<-[:DISCLOSES]-(d:Document)
            RETURN rf.name AS risk, rf.category AS category, rf.severity AS severity,
                   count(d) AS doc_count
            ORDER BY doc_count DESC"""
        )

    def get_litigation_exposure(self, company_name: str = "Monsanto Company") -> list[dict]:
        """Get total litigation exposure for a company."""
        return self.query(
            """MATCH (l:LegalClaim)-[:FILED_AGAINST]->(c:Company {name: $name})
            RETURN l.case_name AS claim, l.claim_type AS type,
                   l.monetary_value AS value, l.status AS status
            ORDER BY l.monetary_value DESC""",
            params={"name": company_name},
        )

    def get_schema(self) -> str:
        """Return the graph schema description for LLM prompts."""
        return GRAPH_SCHEMA

    def node_count(self) -> int:
        """Get total node count."""
        result = self.query("MATCH (n) RETURN count(n) AS cnt")
        return result[0]["cnt"] if result else 0

    def relationship_count(self) -> int:
        """Get total relationship count."""
        result = self.query("MATCH ()-[r]->() RETURN count(r) AS cnt")
        return result[0]["cnt"] if result else 0
