"""Generate synthetic Bayer-Monsanto M&A due diligence documents.

Creates ~48 realistic documents modeled after real document types found
in an M&A due diligence data room, covering both the English (Monsanto/US)
and German (Bayer) sides of the $63B acquisition.

Usage:
    uv run python scripts/generate_sample_documents.py
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.config import DATA_DIR

DOCS_DIR = DATA_DIR / "sample_documents"

# ─────────────────────────────────────────────────────────────────────────────
# ENGLISH DOCUMENTS (Monsanto / US side) — 22 documents
# ─────────────────────────────────────────────────────────────────────────────

ENGLISH_DOCS = [
    # --- Litigation Filings (5) ---
    {
        "id": "LEX-LIT-001",
        "title": "Johnson v. Monsanto Company - Product Liability Complaint",
        "content": (
            "Plaintiff Dewayne Johnson, a former school groundskeeper in Benicia, California, "
            "brings this product liability action against Monsanto Company. Plaintiff alleges that "
            "prolonged occupational exposure to Monsanto's Roundup and Ranger Pro herbicide products, "
            "both containing the active ingredient glyphosate, was a substantial contributing factor "
            "in causing his terminal non-Hodgkin lymphoma (NHL). Plaintiff regularly applied Roundup "
            "products as part of his employment duties from 2012 through 2015, often using backpack "
            "sprayers that resulted in direct skin contact and inhalation exposure. Despite knowing of "
            "scientific evidence linking glyphosate to cancer, Monsanto failed to warn users of the "
            "carcinogenic risks associated with its products. The International Agency for Research on "
            "Cancer (IARC), a specialized agency of the World Health Organization, classified glyphosate "
            "as 'probably carcinogenic to humans' (Group 2A) in March 2015. Internal Monsanto documents "
            "reveal a corporate strategy to 'ghostwrite' scientific papers supporting glyphosate safety "
            "and to suppress independent research raising cancer concerns. Plaintiff seeks compensatory "
            "damages for medical expenses, pain and suffering, lost wages, and loss of future earning "
            "capacity, as well as punitive damages for Monsanto's willful and conscious disregard of "
            "consumer safety. This case was initially filed in San Francisco County Superior Court and "
            "represents one of the first Roundup cancer cases to proceed to trial."
        ),
        "summary": "First Roundup/NHL lawsuit to go to trial. Groundskeeper alleges glyphosate exposure caused cancer.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2016-01-28",
        "parties": ["Dewayne Johnson", "Monsanto Company"],
        "products": ["Roundup", "Ranger Pro"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Product Liability", "NHL Cancer Link", "Failure to Warn"],
        "monetary_value": 289000000,
        "regulatory_bodies": ["IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-SCI-001", "LEX-REG-002"],
        "confidentiality": "public",
        "tags": ["roundup", "glyphosate", "nhl", "product_liability", "bellwether"],
    },
    {
        "id": "LEX-LIT-002",
        "title": "Pilliod v. Monsanto Company - Punitive Damages Complaint",
        "content": (
            "Plaintiffs Alva and Alberta Pilliod, a married couple from Livermore, California, bring "
            "this product liability action against Monsanto Company. Both plaintiffs were diagnosed with "
            "non-Hodgkin lymphoma after using Roundup products on their residential properties for "
            "approximately thirty years. Plaintiffs allege that Monsanto knew or should have known that "
            "glyphosate-based herbicides posed a cancer risk to consumers and failed to provide adequate "
            "warnings. Discovery in prior litigation has revealed internal Monsanto communications "
            "demonstrating that the company actively sought to discredit the IARC classification and "
            "manipulate the scientific record regarding glyphosate carcinogenicity. Monsanto's internal "
            "risk assessments acknowledged potential liability exposure from product liability claims "
            "but prioritized market share protection over consumer safety disclosures. Plaintiffs seek "
            "compensatory damages of $55 million and punitive damages to deter future corporate "
            "misconduct. The magnitude of punitive damages sought reflects the egregious nature of "
            "Monsanto's conduct, including evidence of ghostwriting, regulatory manipulation, and "
            "systematic suppression of cancer research findings."
        ),
        "summary": "Married couple both diagnosed with NHL after 30 years of Roundup use. Seeking $55M compensatory plus punitive damages.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2017-11-15",
        "parties": ["Alva Pilliod", "Alberta Pilliod", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Product Liability", "NHL Cancer Link", "Punitive Damages"],
        "monetary_value": 2055000000,
        "regulatory_bodies": ["IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-LIT-001", "LEX-SCI-001"],
        "confidentiality": "public",
        "tags": ["roundup", "glyphosate", "nhl", "punitive_damages"],
    },
    {
        "id": "LEX-LIT-003",
        "title": "Hardeman v. Monsanto Company - Federal Bellwether Trial",
        "content": (
            "Plaintiff Edwin Hardeman brings this product liability action in the United States "
            "District Court for the Northern District of California as part of the multidistrict "
            "litigation In re Roundup Products Liability Litigation (MDL No. 2741). Mr. Hardeman "
            "used Roundup products on his residential property in Sonoma County for approximately "
            "twenty-six years beginning in 1986. He was diagnosed with non-Hodgkin lymphoma in "
            "February 2015. This case was selected as the first federal bellwether trial to test "
            "the strength of plaintiffs' claims linking Roundup to cancer. The trial was bifurcated "
            "into a causation phase and a liability/damages phase. In the causation phase, the jury "
            "found that plaintiff's exposure to Roundup was a substantial factor in causing his NHL. "
            "Expert testimony included epidemiological studies, animal carcinogenicity studies, and "
            "mechanistic data supporting a causal link between glyphosate exposure and NHL. Monsanto's "
            "defense relied on regulatory approvals from the EPA and other agencies finding glyphosate "
            "unlikely to be carcinogenic. The jury ultimately awarded $80 million in damages, later "
            "reduced to $25 million by the trial court."
        ),
        "summary": "First federal bellwether trial in MDL 2741. Jury found Roundup substantially caused plaintiff's NHL. $80M verdict.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2016-02-24",
        "parties": ["Edwin Hardeman", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Product Liability", "NHL Cancer Link", "Federal MDL"],
        "monetary_value": 80000000,
        "regulatory_bodies": ["EPA"],
        "contract_clauses": [],
        "related_docs": ["LEX-LIT-004", "LEX-SCI-002"],
        "confidentiality": "public",
        "tags": ["roundup", "glyphosate", "nhl", "bellwether", "mdl_2741"],
    },
    {
        "id": "LEX-LIT-004",
        "title": "In re Roundup Products Liability Litigation - MDL 2741 Transfer Order",
        "content": (
            "The United States Judicial Panel on Multidistrict Litigation hereby transfers all pending "
            "federal cases alleging that exposure to Roundup herbicide products caused non-Hodgkin "
            "lymphoma and other cancers to the Northern District of California for coordinated pretrial "
            "proceedings. As of the date of this order, approximately 400 cases are pending in 42 "
            "federal district courts across the United States. These cases share common questions of "
            "fact regarding the alleged carcinogenicity of glyphosate, Monsanto's knowledge of health "
            "risks, and the adequacy of product warnings. The transferee court will manage discovery, "
            "Daubert challenges to expert testimony, and selection of bellwether trials. Monsanto "
            "estimates that thousands of additional cases may be filed as plaintiff advertising "
            "continues. The company's internal projections indicate potential liability exposure in "
            "the billions of dollars if early bellwether trials result in plaintiff verdicts. This "
            "MDL consolidation represents one of the largest product liability litigations in US "
            "history and poses material risk to Monsanto's financial condition and operations."
        ),
        "summary": "MDL 2741 consolidation order. 400+ federal Roundup/NHL cases centralized. Billions in projected exposure.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2016-10-03",
        "parties": ["MDL Plaintiffs", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Mass Tort Litigation", "Product Liability", "Financial Exposure"],
        "monetary_value": 5000000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-LIT-003", "LEX-RISK-001"],
        "confidentiality": "public",
        "tags": ["mdl_2741", "mass_tort", "product_liability"],
    },
    {
        "id": "LEX-LIT-005",
        "title": "Class Action - Dicamba Crop Damage Claims Against Monsanto",
        "content": (
            "Plaintiffs, a class of agricultural producers in the Midwest United States, bring this "
            "action against Monsanto Company and BASF for damages caused by off-target movement of "
            "dicamba herbicide. Monsanto's XtendiMax with VaporGrip Technology, designed for use with "
            "dicamba-tolerant Xtend crops, caused widespread drift damage to neighboring non-tolerant "
            "crops during the 2017 growing season. An estimated 3.6 million acres of soybeans were "
            "damaged across multiple states. Plaintiffs allege that Monsanto knew the dicamba "
            "formulation was prone to volatilization and drift but rushed the product to market to "
            "maintain its competitive position in the seed and herbicide market. State agricultural "
            "departments received thousands of drift complaints. The class seeks compensatory damages "
            "for crop losses, diminished land values, and additional farming expenses. This litigation "
            "represents an additional product liability exposure beyond the Roundup/glyphosate claims "
            "and demonstrates a pattern of Monsanto prioritizing market share over product safety."
        ),
        "summary": "Class action for dicamba crop drift damage. 3.6M acres affected. Additional product liability beyond Roundup.",
        "language": "en",
        "doc_type": "litigation_filing",
        "jurisdiction": "US",
        "date": "2017-10-20",
        "parties": ["Midwest Agricultural Producers", "Monsanto Company", "BASF"],
        "products": ["XtendiMax"],
        "chemicals": ["Dicamba"],
        "risk_factors": ["Product Liability", "Crop Damage", "Environmental"],
        "monetary_value": 400000000,
        "regulatory_bodies": ["EPA"],
        "contract_clauses": [],
        "related_docs": ["LEX-REG-001"],
        "confidentiality": "public",
        "tags": ["dicamba", "crop_damage", "product_liability"],
    },

    # --- Regulatory Correspondence (3) ---
    {
        "id": "LEX-REG-001",
        "title": "EPA Glyphosate Registration Review - Interim Decision",
        "content": (
            "The United States Environmental Protection Agency (EPA) has completed its interim "
            "registration review of glyphosate, the active ingredient in Roundup and numerous other "
            "herbicide products. After evaluating the available epidemiological, animal carcinogenicity, "
            "and genotoxicity studies, EPA's Office of Pesticide Programs concludes that glyphosate is "
            "not likely to be carcinogenic to humans at doses relevant to human health risk assessment. "
            "This determination is consistent with the conclusions of other regulatory bodies including "
            "the European Food Safety Authority (EFSA) and the Joint FAO/WHO Meeting on Pesticide "
            "Residues (JMPR). However, EPA acknowledges that the IARC classification of glyphosate as "
            "'probably carcinogenic' (Group 2A) in 2015 has generated scientific controversy. EPA's "
            "assessment differs from IARC's primarily in the hazard-based versus risk-based approach "
            "and the inclusion of unpublished regulatory studies in EPA's review. EPA requires updated "
            "product labeling and restricts certain application methods. The registration of glyphosate "
            "products remains in effect, subject to ongoing monitoring of new scientific evidence."
        ),
        "summary": "EPA concludes glyphosate 'not likely carcinogenic' but acknowledges IARC controversy. Registration continues.",
        "language": "en",
        "doc_type": "regulatory_correspondence",
        "jurisdiction": "US",
        "date": "2017-12-18",
        "parties": ["EPA", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Regulatory Risk", "Carcinogenicity Debate"],
        "monetary_value": 0,
        "regulatory_bodies": ["EPA", "IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-REG-002", "LEX-SCI-002"],
        "confidentiality": "public",
        "tags": ["epa", "glyphosate", "registration_review", "carcinogenicity"],
    },
    {
        "id": "LEX-REG-002",
        "title": "IARC Monograph 112 - Glyphosate Classification Notification",
        "content": (
            "The International Agency for Research on Cancer (IARC) hereby notifies stakeholders of "
            "the publication of IARC Monograph Volume 112, evaluating the carcinogenicity of five "
            "organophosphate insecticides and herbicides, including glyphosate. Following review by "
            "a Working Group of 17 international experts from 11 countries, IARC has classified "
            "glyphosate as 'probably carcinogenic to humans' (Group 2A). This classification is "
            "based on 'limited' evidence of cancer in humans for non-Hodgkin lymphoma, 'sufficient' "
            "evidence of cancer in experimental animals, and 'strong' evidence of genotoxicity and "
            "oxidative stress mechanisms. The human evidence includes case-control studies of "
            "occupational exposure in the USA, Canada, and Sweden reporting increased risks of NHL "
            "among agricultural workers exposed to glyphosate. The Working Group noted that glyphosate "
            "is the most widely used herbicide globally, with production volumes that have increased "
            "approximately 100-fold since 1974. IARC emphasizes that its evaluations are hazard "
            "identifications and do not quantify risk at specific exposure levels. This classification "
            "has significant implications for regulatory agencies worldwide and for ongoing product "
            "liability litigation in the United States."
        ),
        "summary": "IARC classifies glyphosate as Group 2A 'probably carcinogenic.' Based on NHL evidence in agricultural workers.",
        "language": "en",
        "doc_type": "regulatory_correspondence",
        "jurisdiction": "INTL",
        "date": "2015-03-20",
        "parties": ["IARC", "WHO"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Carcinogenicity Classification", "Regulatory Risk", "NHL Cancer Link"],
        "monetary_value": 0,
        "regulatory_bodies": ["IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-REG-001", "LEX-SCI-001"],
        "confidentiality": "public",
        "tags": ["iarc", "glyphosate", "carcinogenic", "group_2a", "nhl"],
    },
    {
        "id": "LEX-REG-003",
        "title": "EPA Response to IARC Classification - Glyphosate Issue Paper",
        "content": (
            "The EPA Office of Pesticide Programs issues this white paper in response to the IARC "
            "Monograph 112 classification of glyphosate as Group 2A. EPA reaffirms its position that "
            "glyphosate does not pose carcinogenic risks to humans based on currently registered uses. "
            "EPA notes several methodological differences between its assessment and IARC's evaluation: "
            "(1) EPA reviewed approximately 100 additional regulatory studies not available to IARC, "
            "including Good Laboratory Practice (GLP) compliant long-term animal studies submitted by "
            "registrants; (2) EPA conducts risk assessment incorporating exposure levels, whereas IARC "
            "performs hazard identification only; (3) EPA and IARC weight-of-evidence frameworks differ "
            "in their treatment of mechanistic data. EPA acknowledges that the IARC classification has "
            "created uncertainty in the marketplace and among consumers. EPA recommends continued "
            "monitoring of epidemiological literature and notes that several large prospective cohort "
            "studies, including the Agricultural Health Study, have not found consistent associations "
            "between glyphosate use and NHL risk. The Agency will complete its full registration review "
            "and draft risk assessment within 18 months."
        ),
        "summary": "EPA rebuts IARC classification. Cites 100+ additional studies. Acknowledges marketplace uncertainty.",
        "language": "en",
        "doc_type": "regulatory_correspondence",
        "jurisdiction": "US",
        "date": "2016-09-12",
        "parties": ["EPA"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Regulatory Uncertainty", "Conflicting Scientific Assessments"],
        "monetary_value": 0,
        "regulatory_bodies": ["EPA", "IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-REG-001", "LEX-REG-002"],
        "confidentiality": "public",
        "tags": ["epa", "iarc", "glyphosate", "rebuttal"],
    },

    # --- Internal Risk Assessments (2) ---
    {
        "id": "LEX-RISK-001",
        "title": "Monsanto Internal Litigation Risk Assessment - Roundup Product Liability",
        "content": (
            "CONFIDENTIAL - ATTORNEY-CLIENT PRIVILEGED. This memorandum presents an updated risk "
            "assessment of Monsanto's litigation exposure from Roundup product liability claims. As "
            "of Q3 2017, approximately 3,500 plaintiffs have filed lawsuits alleging that Roundup "
            "caused non-Hodgkin lymphoma. Plaintiff filings are accelerating, with an estimated 500 "
            "new cases per month following televised plaintiff attorney advertising. Internal modeling "
            "projects total claim filings could reach 20,000-50,000 by 2020. Assuming an average "
            "settlement value of $150,000-$200,000 per claim (based on historical mass tort "
            "settlements) and a 70% claim validation rate, the estimated liability range is $2.1 "
            "billion to $7.0 billion. However, if bellwether trial verdicts establish large damage "
            "awards, settlement values could increase substantially. The Johnson v. Monsanto trial "
            "scheduled for 2018 presents critical risk: an adverse verdict with significant punitive "
            "damages could drive up overall settlement costs by 2-3x. Key risk factors include: (1) "
            "IARC carcinogenicity classification provides plaintiffs with credible expert basis; (2) "
            "internal Monsanto communications regarding ghostwriting and regulatory manipulation may "
            "support punitive damages findings; (3) sympathetic plaintiff narratives resonate with "
            "juries. Recommendation: establish litigation reserve of $5 billion and consider global "
            "settlement strategies before bellwether trial results."
        ),
        "summary": "Internal Monsanto memo projects 20,000-50,000 claims and $2.1-7.0B liability. Recommends $5B reserve.",
        "language": "en",
        "doc_type": "risk_assessment",
        "jurisdiction": "US",
        "date": "2017-09-30",
        "parties": ["Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Mass Tort Liability", "Punitive Damages Risk", "Accelerating Claim Filings", "Ghostwriting Exposure"],
        "monetary_value": 5000000000,
        "regulatory_bodies": ["IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-LIT-001", "LEX-LIT-004"],
        "confidentiality": "privileged",
        "tags": ["internal", "risk_assessment", "litigation_reserve", "roundup"],
    },
    {
        "id": "LEX-RISK-002",
        "title": "Monsanto Product Liability Portfolio Risk Review - All Products",
        "content": (
            "CONFIDENTIAL. Annual product liability portfolio review for Monsanto's full product line. "
            "Summary of key exposure areas: (1) ROUNDUP/GLYPHOSATE: Critical risk. See detailed "
            "assessment LEX-RISK-001. Total projected exposure: $2.1-7.0 billion. Claim count growing "
            "500/month. Multiple bellwether trials scheduled 2018-2019. (2) DICAMBA/XTEND SYSTEM: "
            "High risk. Approximately 1,000 crop damage complaints filed with state agricultural "
            "departments in 2017. Class action litigation pending. Estimated exposure: $300-500 million. "
            "(3) PCBs (LEGACY): Moderate risk. Monsanto manufactured PCBs until 1977. Ongoing "
            "environmental remediation obligations and personal injury claims. Current reserve: $400 "
            "million. (4) AGENT ORANGE (LEGACY): Low active risk. Prior settlements have resolved most "
            "claims. Residual exposure estimated at $50 million. (5) BOVINE GROWTH HORMONE (rBGH): "
            "Minimal risk. Limited ongoing claims. TOTAL PORTFOLIO EXPOSURE: $3.0-8.0 billion across "
            "all product lines. The Roundup/glyphosate litigation represents approximately 85-90% of "
            "total portfolio risk. Adequacy of insurance coverage: Product liability insurance policies "
            "provide $750 million in aggregate coverage, well below projected exposure."
        ),
        "summary": "Portfolio-wide risk review. Total exposure $3-8B. Roundup is 85-90% of risk. Insurance covers only $750M.",
        "language": "en",
        "doc_type": "risk_assessment",
        "jurisdiction": "US",
        "date": "2017-12-15",
        "parties": ["Monsanto Company"],
        "products": ["Roundup", "XtendiMax", "Ranger Pro"],
        "chemicals": ["Glyphosate", "Dicamba"],
        "risk_factors": ["Product Liability Portfolio", "Insurance Gap", "Legacy Liabilities"],
        "monetary_value": 8000000000,
        "regulatory_bodies": ["EPA"],
        "contract_clauses": [],
        "related_docs": ["LEX-RISK-001", "LEX-INS-001"],
        "confidentiality": "privileged",
        "tags": ["risk_review", "portfolio", "insurance_gap", "pcb", "dicamba"],
    },

    # --- Settlement Agreements (2) ---
    {
        "id": "LEX-SET-001",
        "title": "Johnson v. Monsanto - Appeal Settlement Terms",
        "content": (
            "SETTLEMENT AGREEMENT AND RELEASE. This agreement is entered into by and between Dewayne "
            "Johnson ('Plaintiff') and Monsanto Company (now a subsidiary of Bayer AG) to resolve "
            "all claims arising from Johnson v. Monsanto Company, San Francisco Superior Court Case "
            "No. CGC-16-550128. The jury originally awarded $289 million, comprising $39.2 million in "
            "compensatory damages and $250 million in punitive damages. The trial court subsequently "
            "reduced the award to $78.5 million. Following appeal to the California Court of Appeal, "
            "the parties have reached a confidential settlement. Key terms: (1) Monsanto/Bayer will "
            "pay an undisclosed settlement amount to Plaintiff within 30 days; (2) Plaintiff releases "
            "all claims against Monsanto, Bayer, their subsidiaries, and affiliates; (3) This "
            "settlement does not constitute an admission of liability, causation, or wrongdoing; "
            "(4) The terms of this agreement are confidential and may not be disclosed except as "
            "required by law or regulatory obligation. The settlement of this bellwether case does not "
            "resolve the approximately 42,000 other pending Roundup claims."
        ),
        "summary": "Confidential settlement of first bellwether case. Original $289M verdict reduced on appeal. ~42,000 claims remain.",
        "language": "en",
        "doc_type": "settlement_agreement",
        "jurisdiction": "US",
        "date": "2020-06-22",
        "parties": ["Dewayne Johnson", "Monsanto Company", "Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Settlement Precedent", "Confidential Terms"],
        "monetary_value": 78500000,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "release_of_claims", "summary": "Full release of all claims against Monsanto and Bayer", "language": "en"}],
        "related_docs": ["LEX-LIT-001"],
        "confidentiality": "confidential",
        "tags": ["settlement", "bellwether", "roundup"],
    },
    {
        "id": "LEX-SET-002",
        "title": "Roundup MDL Global Settlement Framework - $10.9 Billion Resolution",
        "content": (
            "Bayer AG announces a comprehensive settlement framework to resolve the Roundup litigation "
            "in the United States. The agreement provides approximately $10.9 billion to resolve "
            "approximately 100,000 current and potential future claims alleging Roundup herbicide "
            "caused non-Hodgkin lymphoma. The settlement is structured as follows: (1) $8.8-9.6 "
            "billion to resolve approximately 75% of currently filed claims through a series of "
            "plaintiff-firm-specific agreements; (2) $1.25 billion to address potential future claims "
            "through a proposed class settlement establishing a science panel to evaluate the "
            "glyphosate-NHL link; (3) Individual settlements for cases not covered by firm-specific "
            "agreements. The settlement does not include an admission of liability or wrongdoing. "
            "Bayer will continue to sell Roundup products and will not add cancer warnings to product "
            "labels. The proposed future claims resolution was subsequently rejected by the Eighth "
            "Circuit Court of Appeals, leaving Bayer exposed to ongoing claim filings. As of 2026, "
            "approximately 65,000 claims remain unresolved, and Bayer has proposed a $7.25 billion "
            "class-action settlement for these remaining cases."
        ),
        "summary": "$10.9B global settlement for ~100,000 claims. Future claims class rejected. 65,000 claims still pending in 2026.",
        "language": "en",
        "doc_type": "settlement_agreement",
        "jurisdiction": "US",
        "date": "2020-06-24",
        "parties": ["Bayer AG", "MDL Plaintiffs"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Mass Settlement", "Future Claims Exposure", "Ongoing Liability"],
        "monetary_value": 10900000000,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "mass_settlement", "summary": "$10.9B framework for 100,000 claims", "language": "en"}],
        "related_docs": ["LEX-LIT-004", "LEX-RISK-001"],
        "confidentiality": "public",
        "tags": ["global_settlement", "roundup", "10_billion"],
    },

    # --- Insurance Policies (2) ---
    {
        "id": "LEX-INS-001",
        "title": "Monsanto Product Liability Insurance Policy - Primary Coverage",
        "content": (
            "PRODUCT LIABILITY INSURANCE POLICY. Insured: Monsanto Company and subsidiaries. Policy "
            "Period: January 1, 2017 - December 31, 2017. Insurer: Global Re Insurance Group. "
            "Coverage: Products-Completed Operations Liability. Per-Occurrence Limit: $100,000,000. "
            "Annual Aggregate Limit: $250,000,000. Self-Insured Retention: $25,000,000 per occurrence. "
            "COVERED PRODUCTS: All herbicide, pesticide, and agricultural biotechnology products "
            "manufactured, sold, or distributed by the Insured. EXCLUSIONS: (a) Known or expected "
            "liabilities as of policy inception; (b) Punitive or exemplary damages where prohibited "
            "by law; (c) Environmental remediation costs; (d) Product recall expenses; (e) Liabilities "
            "arising from intentional misconduct or fraud. CLAIMS-MADE TRIGGER: Coverage applies to "
            "claims first made during the policy period, regardless of when the alleged injury occurred. "
            "IMPORTANT LIMITATION: Given the volume of Roundup-related claims filed prior to policy "
            "inception, the Known Liability exclusion (a) may preclude coverage for substantially all "
            "glyphosate/NHL claims. The insurer reserves all rights to deny coverage under this "
            "exclusion pending further investigation."
        ),
        "summary": "Primary liability policy: $250M aggregate. Known liability exclusion likely precludes Roundup coverage.",
        "language": "en",
        "doc_type": "insurance_policy",
        "jurisdiction": "US",
        "date": "2017-01-01",
        "parties": ["Monsanto Company", "Global Re Insurance Group"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Insurance Coverage Gap", "Known Liability Exclusion"],
        "monetary_value": 250000000,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "known_liability_exclusion", "summary": "Excludes known or expected liabilities at inception", "language": "en"}],
        "related_docs": ["LEX-INS-002", "LEX-RISK-002"],
        "confidentiality": "confidential",
        "tags": ["insurance", "product_liability", "exclusion"],
    },
    {
        "id": "LEX-INS-002",
        "title": "Monsanto Excess Liability Coverage - Tower Structure Summary",
        "content": (
            "EXCESS LIABILITY INSURANCE TOWER SUMMARY. This document summarizes the layered excess "
            "liability insurance program maintained by Monsanto Company for the 2017 policy year. "
            "Layer 1 (Primary): Global Re Insurance Group, $250M aggregate, subject to $25M SIR. "
            "Layer 2: Atlantic Specialty Insurance, $250M xs $250M. Layer 3: Pacific Mutual Re, "
            "$250M xs $500M. TOTAL TOWER: $750,000,000 in aggregate coverage. CRITICAL NOTE: All "
            "layers contain known-or-expected-liability exclusions and follow-form to the primary "
            "policy exclusions. Given that Roundup/glyphosate litigation was well-established prior "
            "to the 2017 policy inception, coverage counsel advises that recovery under these policies "
            "for Roundup-related claims is unlikely. The $750M total tower is materially insufficient "
            "relative to projected Roundup liability exposure of $3-8 billion. The insurance program "
            "was designed before the scale of Roundup litigation became apparent. Monsanto's risk "
            "management team recommends exploring retroactive liability coverage options and captive "
            "insurance alternatives for the 2018 policy renewal."
        ),
        "summary": "Total insurance tower: $750M. Likely no coverage for Roundup claims. Projected exposure: $3-8B. Massive gap.",
        "language": "en",
        "doc_type": "insurance_policy",
        "jurisdiction": "US",
        "date": "2017-01-15",
        "parties": ["Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Insurance Tower Inadequacy", "Coverage Gap", "Uninsured Liability"],
        "monetary_value": 750000000,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "follow_form_exclusion", "summary": "All excess layers follow primary exclusions", "language": "en"}],
        "related_docs": ["LEX-INS-001", "LEX-RISK-002"],
        "confidentiality": "confidential",
        "tags": ["insurance_tower", "coverage_gap", "excess_liability"],
    },

    # --- Indemnification / Contracts (2) ---
    {
        "id": "LEX-CON-001",
        "title": "Monsanto Distributor Agreement - Indemnification Provisions",
        "content": (
            "DISTRIBUTION AGREEMENT between Monsanto Company ('Manufacturer') and AgriChem "
            "Distributors, Inc. ('Distributor'). Section 12 - INDEMNIFICATION: 12.1 Manufacturer "
            "shall indemnify, defend, and hold harmless Distributor from and against any and all "
            "claims, damages, losses, costs, and expenses (including reasonable attorneys' fees) "
            "arising from: (a) product defects in Manufacturer's products; (b) failure of "
            "Manufacturer to provide adequate warnings regarding health or environmental risks; "
            "(c) personal injury or property damage claims related to Manufacturer's products. "
            "12.2 THE INDEMNIFICATION OBLIGATION UNDER THIS SECTION IS UNLIMITED and shall survive "
            "termination of this agreement. 12.3 Manufacturer shall maintain product liability "
            "insurance with minimum limits of $50 million per occurrence and $100 million annual "
            "aggregate. 12.4 Distributor shall promptly notify Manufacturer of any claim and "
            "cooperate in the defense thereof. IMPORTANT: This unlimited indemnification provision "
            "creates open-ended liability for Monsanto for all downstream product claims made through "
            "the distribution channel. Similar provisions exist in approximately 200 distributor "
            "agreements covering North American, Latin American, and European distribution networks."
        ),
        "summary": "Unlimited indemnification of distributors for product claims. ~200 similar agreements in force worldwide.",
        "language": "en",
        "doc_type": "indemnification_clause",
        "jurisdiction": "US",
        "date": "2015-03-01",
        "parties": ["Monsanto Company", "AgriChem Distributors"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Unlimited Indemnification", "Downstream Liability"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "unlimited_indemnification", "summary": "Unlimited indemnity for product defect and failure-to-warn claims", "language": "en"}],
        "related_docs": ["LEX-CON-002", "LEX-MRG-001"],
        "confidentiality": "confidential",
        "tags": ["indemnification", "distributor", "unlimited_liability"],
    },
    {
        "id": "LEX-CON-002",
        "title": "Monsanto Supplier Contract - Liability Allocation for Glyphosate Raw Materials",
        "content": (
            "SUPPLY AGREEMENT between ChemSource International Ltd. ('Supplier') and Monsanto "
            "Company ('Buyer'). Section 8 - LIABILITY AND INDEMNIFICATION: 8.1 Supplier warrants "
            "that all glyphosate technical grade material supplied under this agreement meets the "
            "specifications set forth in Exhibit A and complies with all applicable regulatory "
            "requirements. 8.2 Supplier shall indemnify Buyer for claims arising from non-conforming "
            "product or contamination. 8.3 LIMITATION: Supplier's total liability under this "
            "agreement shall not exceed the purchase price paid in the twelve months preceding the "
            "claim. 8.4 EXCLUSION: Supplier shall not be liable for claims arising from Buyer's "
            "formulation, labeling, marketing, or end-use applications of products containing "
            "Supplier's raw material. NOTE: This liability structure creates a significant asymmetry "
            "- Monsanto bears unlimited indemnification obligations to its distributors (LEX-CON-001) "
            "but has only limited recourse against its raw material suppliers. Product liability "
            "claims related to health effects of formulated products fall entirely on Monsanto."
        ),
        "summary": "Supplier liability capped at 12 months of purchases. Monsanto bears all formulation/labeling liability.",
        "language": "en",
        "doc_type": "indemnification_clause",
        "jurisdiction": "US",
        "date": "2016-06-01",
        "parties": ["ChemSource International", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Liability Asymmetry", "Limited Supplier Recourse"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "liability_cap", "summary": "Supplier liability limited to 12 months purchase price", "language": "en"}],
        "related_docs": ["LEX-CON-001"],
        "confidentiality": "confidential",
        "tags": ["supplier", "liability_cap", "indemnification"],
    },

    # --- SEC Filings (2) ---
    {
        "id": "LEX-SEC-001",
        "title": "Monsanto 10-K Annual Report - Risk Factor Disclosures FY2017",
        "content": (
            "MONSANTO COMPANY - FORM 10-K FOR THE FISCAL YEAR ENDED AUGUST 31, 2017. ITEM 1A - RISK "
            "FACTORS (EXCERPT): Product Liability Litigation: We are defendants in a number of "
            "lawsuits alleging that our Roundup herbicide products cause cancer, specifically non-Hodgkin "
            "lymphoma. As of August 31, 2017, approximately 3,500 plaintiffs have filed lawsuits in "
            "state and federal courts throughout the United States. The first trial is expected in "
            "2018. We believe these claims are without merit and intend to vigorously defend against "
            "them. However, the outcome of litigation is inherently uncertain, and adverse verdicts "
            "in one or more of these cases could result in significant financial liability. We have "
            "not established a litigation reserve for these claims as we believe the probability of "
            "loss is not yet determinable. Regulatory Matters: The IARC classification of glyphosate "
            "as Group 2A 'probably carcinogenic' has generated negative publicity and could adversely "
            "affect consumer perceptions of our products. Although we disagree with the IARC "
            "classification and regulatory authorities including the EPA continue to find glyphosate "
            "safe for use as directed, the classification may result in additional regulatory actions "
            "or restrictions in certain jurisdictions."
        ),
        "summary": "10-K discloses 3,500 Roundup lawsuits. No litigation reserve established. Claims deemed 'without merit.'",
        "language": "en",
        "doc_type": "sec_filing",
        "jurisdiction": "US",
        "date": "2017-10-20",
        "parties": ["Monsanto Company", "SEC"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Litigation Risk Disclosure", "No Reserve Established", "Regulatory Uncertainty"],
        "monetary_value": 0,
        "regulatory_bodies": ["SEC", "EPA", "IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-SEC-002", "LEX-RISK-001"],
        "confidentiality": "public",
        "tags": ["sec", "10k", "risk_factors", "no_reserve"],
    },
    {
        "id": "LEX-SEC-002",
        "title": "Monsanto 8-K Current Report - Merger Agreement with Bayer",
        "content": (
            "MONSANTO COMPANY - FORM 8-K CURRENT REPORT. Item 1.01 - Entry into a Material "
            "Definitive Agreement. On September 14, 2016, Monsanto Company entered into an Agreement "
            "and Plan of Merger with Bayer Aktiengesellschaft, a German company, and KWA Investment "
            "Co., a wholly-owned subsidiary of Bayer, pursuant to which Bayer will acquire all "
            "outstanding shares of Monsanto common stock for $128.00 per share in an all-cash "
            "transaction valued at approximately $63 billion, including Monsanto's net debt. The "
            "merger is subject to: (a) approval by Monsanto shareholders; (b) regulatory approvals "
            "including from the US Department of Justice, European Commission, and other competition "
            "authorities; (c) customary closing conditions. The merger agreement contains customary "
            "representations and warranties, including representations by Monsanto regarding pending "
            "litigation and regulatory proceedings. Item 8.01 - Pending Litigation: Monsanto has "
            "disclosed to Bayer the existence of lawsuits alleging Roundup causes cancer. As of the "
            "date of this report, approximately 2,000 such cases are pending. The merger agreement "
            "includes a Material Adverse Effect clause with standard carve-outs. Notably, the "
            "words 'Roundup' and 'glyphosate' do not appear in the merger agreement."
        ),
        "summary": "$63B merger announced. MAE clause uses standard carve-outs. ~2,000 Roundup cases pending at signing.",
        "language": "en",
        "doc_type": "sec_filing",
        "jurisdiction": "US",
        "date": "2016-09-14",
        "parties": ["Monsanto Company", "Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["MAE Threshold", "Litigation Disclosure", "Merger Risk"],
        "monetary_value": 63000000000,
        "regulatory_bodies": ["SEC", "DOJ", "EU Commission"],
        "contract_clauses": [{"clause_type": "material_adverse_effect", "summary": "MAE uses standard carve-outs; Roundup/glyphosate not mentioned by name", "language": "en"}],
        "related_docs": ["LEX-MRG-001", "LEX-CRB-001"],
        "confidentiality": "public",
        "tags": ["sec", "8k", "merger", "mae_clause"],
    },

    # --- Scientific Studies (4) ---
    {
        "id": "LEX-SCI-001",
        "title": "IARC Working Group - Glyphosate Carcinogenicity Evaluation Summary",
        "content": (
            "Summary of IARC Monograph 112 Working Group evaluation of glyphosate carcinogenicity. "
            "HUMAN EVIDENCE (Limited): Meta-analysis of six case-control studies of NHL and glyphosate "
            "exposure showed a statistically significant positive association (meta-RR = 1.3, 95% CI "
            "1.0-1.6). Positive associations were observed in studies from the United States, Canada, "
            "and Sweden. The Agricultural Health Study, a large US prospective cohort, did not show a "
            "statistically significant association but had limited follow-up time. ANIMAL EVIDENCE "
            "(Sufficient): Significant increases in renal tubule carcinoma in male CD-1 mice and "
            "hemangiosarcoma in male CD-1 mice in two studies. Rare tumor types were also observed. "
            "MECHANISTIC EVIDENCE (Strong): Glyphosate caused DNA damage in multiple in vitro and "
            "in vivo test systems. Oxidative stress biomarkers were elevated in exposed human "
            "populations. Genotoxicity was observed in human cells at concentrations achievable "
            "through occupational exposure. OVERALL EVALUATION: Group 2A - Probably carcinogenic to "
            "humans."
        ),
        "summary": "IARC evaluation: limited human evidence (NHL meta-RR 1.3), sufficient animal evidence, strong mechanistic data.",
        "language": "en",
        "doc_type": "scientific_study",
        "jurisdiction": "INTL",
        "date": "2015-07-29",
        "parties": ["IARC"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Carcinogenicity Evidence", "NHL Association"],
        "monetary_value": 0,
        "regulatory_bodies": ["IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-REG-002", "LEX-SCI-002"],
        "confidentiality": "public",
        "tags": ["iarc", "carcinogenicity", "meta_analysis", "nhl"],
    },
    {
        "id": "LEX-SCI-002",
        "title": "EPA Office of Pesticide Programs - Glyphosate Cancer Assessment",
        "content": (
            "EPA Office of Pesticide Programs Revised Glyphosate Issue Paper: Evaluation of "
            "Carcinogenic Potential. EPA evaluated the full body of evidence including epidemiological "
            "studies, animal carcinogenicity studies, and genotoxicity assays. EPIDEMIOLOGICAL EVIDENCE: "
            "EPA reviewed 23 epidemiological studies of glyphosate and cancer, including 16 case-control "
            "studies and 7 cohort studies. The Agricultural Health Study (AHS), a prospective cohort of "
            "over 50,000 licensed pesticide applicators, found no statistically significant association "
            "between glyphosate use and NHL overall or any specific NHL subtype. EPA gave greatest "
            "weight to the AHS due to its prospective design and detailed exposure assessment. "
            "ANIMAL EVIDENCE: EPA reviewed 15 chronic/carcinogenicity studies in rats and mice. EPA "
            "concluded that the tumor findings cited by IARC were not treatment-related based on "
            "historical control data, lack of dose-response, and statistical considerations. "
            "GENOTOXICITY: EPA found the weight of evidence does not support a mutagenic mode of "
            "action. OVERALL CONCLUSION: Not likely to be carcinogenic to humans."
        ),
        "summary": "EPA concludes 'not likely carcinogenic.' Gives most weight to Agricultural Health Study showing no NHL link.",
        "language": "en",
        "doc_type": "scientific_study",
        "jurisdiction": "US",
        "date": "2016-09-12",
        "parties": ["EPA"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Conflicting Scientific Evidence"],
        "monetary_value": 0,
        "regulatory_bodies": ["EPA"],
        "contract_clauses": [],
        "related_docs": ["LEX-SCI-001", "LEX-REG-001"],
        "confidentiality": "public",
        "tags": ["epa", "cancer_assessment", "not_carcinogenic"],
    },
    {
        "id": "LEX-SCI-003",
        "title": "Independent Epidemiology Meta-Analysis - Glyphosate and NHL Risk",
        "content": (
            "Meta-Analysis of Glyphosate Exposure and Risk of Non-Hodgkin Lymphoma. Published in "
            "Mutation Research/Reviews in Mutation Research, 2019. Authors: Zhang L, Rana I, Shaffer "
            "RM, et al., University of Washington. This updated meta-analysis incorporates published "
            "and unpublished data from the Agricultural Health Study (AHS) through 2015 follow-up. "
            "METHODS: Systematic review of all epidemiological studies published through 2018. "
            "Six case-control studies and one cohort study (AHS) met inclusion criteria. Random-effects "
            "meta-analysis was performed. RESULTS: The overall meta-relative risk for NHL with the "
            "highest exposure category of glyphosate was 1.41 (95% CI: 1.13-1.75). When restricted "
            "to studies adjusting for other pesticide exposure, the association strengthened (meta-RR "
            "= 1.45, 95% CI: 1.11-1.91). Inclusion of updated AHS data did not materially change "
            "the results. CONCLUSIONS: This meta-analysis confirms a compelling link between exposure "
            "to glyphosate-based herbicides and increased risk of NHL. The findings are consistent "
            "with the IARC assessment and support the biological plausibility of a causal relationship."
        ),
        "summary": "Independent meta-analysis finds 41% increased NHL risk (RR 1.41). Confirms IARC assessment.",
        "language": "en",
        "doc_type": "scientific_study",
        "jurisdiction": "US",
        "date": "2019-02-10",
        "parties": [],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Epidemiological Evidence", "NHL Risk Increase"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-SCI-001", "LEX-SCI-004"],
        "confidentiality": "public",
        "tags": ["meta_analysis", "nhl", "independent_research"],
    },
    {
        "id": "LEX-SCI-004",
        "title": "Monsanto-Funded Safety Study - Glyphosate Chronic Toxicity Review",
        "content": (
            "Comprehensive Review of Glyphosate Chronic Toxicity and Carcinogenicity Studies. "
            "Sponsored by Monsanto Company. Prepared by Regulatory Science Associates LLC. This "
            "review examines the complete database of chronic toxicity and carcinogenicity studies "
            "submitted to regulatory agencies worldwide. The database includes 15 chronic feeding "
            "studies in rats and 10 in mice, spanning over 40 years of testing. KEY FINDINGS: "
            "(1) No consistent pattern of tumors across studies. Isolated tumor findings in individual "
            "studies are within historical control ranges. (2) No evidence of a dose-response "
            "relationship for any tumor type. (3) The renal tubule tumors in male mice cited by IARC "
            "are a known spontaneous background finding in CD-1 mice with high historical control "
            "rates. (4) The hemangiosarcoma findings are within historical control ranges when "
            "appropriate concurrent controls are used. CONCLUSION: The weight of evidence from "
            "regulatory-quality animal studies does not support classification of glyphosate as a "
            "carcinogen. This conclusion is consistent with the findings of EPA, EFSA, JMPR, and "
            "other regulatory authorities. NOTE: This study was funded by Monsanto. Disclosure of "
            "funding source is provided per journal policy."
        ),
        "summary": "Monsanto-funded review finds no carcinogenic evidence. Notes tumor findings within historical controls.",
        "language": "en",
        "doc_type": "scientific_study",
        "jurisdiction": "US",
        "date": "2016-03-15",
        "parties": ["Monsanto Company", "Regulatory Science Associates"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Conflict of Interest", "Industry-Funded Research"],
        "monetary_value": 0,
        "regulatory_bodies": ["EPA"],
        "contract_clauses": [],
        "related_docs": ["LEX-SCI-002", "LEX-SCI-003"],
        "confidentiality": "public",
        "tags": ["industry_funded", "safety_study", "not_carcinogenic"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# GERMAN DOCUMENTS (Bayer side) — 18 documents
# ─────────────────────────────────────────────────────────────────────────────

GERMAN_DOCS = [
    # --- Board Minutes (3) ---
    {
        "id": "LEX-BD-001",
        "title": "Protokoll der Vorstandssitzung - Uebernahmerisikobewertung Monsanto",
        "content": (
            "VERTRAULICH - Protokoll der Vorstandssitzung der Bayer AG vom 14. September 2016. "
            "Tagesordnungspunkt 3: Bewertung der Uebernahmerisiken bei der geplanten Akquisition "
            "der Monsanto Company. Der Vorstandsvorsitzende praesentiert die Ergebnisse der "
            "Sorgfaltspruefung. Wesentliche Feststellungen: (1) Monsanto ist globaler Marktfuehrer "
            "bei Saatgut und Pflanzenschutzmitteln mit einem Jahresumsatz von 14,6 Milliarden USD. "
            "(2) Das Produktportfolio umfasst Roundup (Glyphosat-basiert), gentechnisch veraendertes "
            "Saatgut und digitale Landwirtschaftsloesungen. (3) Rechtsrisiken: Es sind derzeit "
            "etwa 2.000 Klagen wegen angeblicher Krebsverursachung durch Roundup anhaengig. Die "
            "Rechtsabteilung stuft das Haftungsrisiko als beherrschbar ein. "
            "(4) Regulatorische Risiken: Die IARC-Klassifizierung von Glyphosat als wahrscheinlich "
            "krebserregend wird als beherrschbar eingestuft, da EPA und EFSA weiterhin die "
            "Unbedenklichkeit bestaetigen. BESCHLUSS: Der Vorstand genehmigt die Fortsetzung der "
            "Uebernahmeverhandlungen zum Angebotspreis von 128 USD je Aktie. Das Gesamtvolumen "
            "der Transaktion betraegt ca. 63 Milliarden USD einschliesslich Schuldenuebernahme."
        ),
        "summary": "Vorstandssitzung genehmigt Monsanto-Uebernahme. Haftungsrisiko als beherrschbar eingestuft. 2.000 Klagen bekannt.",
        "language": "de",
        "doc_type": "board_minutes",
        "jurisdiction": "DE",
        "date": "2016-09-14",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Uebernahmerisiko", "Haftungsrisiko", "Unterschaetzung der Klagezahl"],
        "monetary_value": 63000000000,
        "regulatory_bodies": ["BaFin", "IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-DD-001", "LEX-MRG-001"],
        "confidentiality": "internal",
        "tags": ["vorstand", "uebernahme", "risikobewertung", "glyphosat"],
    },
    {
        "id": "LEX-BD-002",
        "title": "Aufsichtsratssitzung - Diskussion der Haftungsrisiken Monsanto",
        "content": (
            "VERTRAULICH - Protokoll der Aufsichtsratssitzung der Bayer AG vom 28. November 2016. "
            "Der Aufsichtsrat eroertert die Haftungsrisiken der Monsanto-Uebernahme im Detail. "
            "Praesentiert werden die Ergebnisse der rechtlichen Sorgfaltspruefung durch die "
            "US-amerikanische Anwaltskanzlei Davis Polk. Wesentliche Punkte: (1) Die aktuell "
            "anhaengigen Roundup-Klagen sind in ihrer Gesamtheit als beherrschbar einzustufen. "
            "Die Klaeger stuetzen sich hauptsaechlich auf die IARC-Klassifizierung, waehrend "
            "die EPA-Bewertung Monsantos Position stuetzt. (2) Die Verschmelzungsvereinbarung "
            "enthaelt eine Material-Adverse-Effect-Klausel, die bestehende Rechtsstreitigkeiten "
            "standardmaessige Ausschluesse (Wirtschaftslage, Maerkte, Branchenveraenderungen) enthaelt. "
            "(3) Arbeitnehmervertreter aeussern Bedenken hinsichtlich des Reputationsrisikos "
            "fuer die Marke Bayer. (4) Der Vorstand sichert zu, dass eine umfassende "
            "Produkthaftungsversicherung abgeschlossen wird. BESCHLUSS: Der Aufsichtsrat "
            "stimmt der Uebernahme mit 16 zu 4 Stimmen zu."
        ),
        "summary": "Aufsichtsrat genehmigt Uebernahme (16:4). Haftung als 'beherrschbar' eingestuft. MAE-Klausel mit Standardausschluessen.",
        "language": "de",
        "doc_type": "board_minutes",
        "jurisdiction": "DE",
        "date": "2016-11-28",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Aufsichtsratsentscheidung", "Reputationsrisiko", "Beherrschbarkeitsbewertung"],
        "monetary_value": 0,
        "regulatory_bodies": ["BaFin"],
        "contract_clauses": [{"clause_type": "material_adverse_effect", "summary": "MAE-Klausel mit Standardausschluessen, keine spezifische Roundup-Schwelle", "language": "de"}],
        "related_docs": ["LEX-BD-001", "LEX-MRG-002"],
        "confidentiality": "internal",
        "tags": ["aufsichtsrat", "haftung", "genehmigung"],
    },
    {
        "id": "LEX-BD-003",
        "title": "Vorstandssitzung - Integrationsplanung Post-Merger Monsanto",
        "content": (
            "VERTRAULICH - Protokoll der Vorstandssitzung der Bayer AG vom 15. Januar 2018. "
            "Tagesordnungspunkt 2: Status der Integration nach Vollzug der Monsanto-Uebernahme. "
            "Der Integrationsleiter berichtet ueber den Fortschritt: (1) Organisationsstruktur: "
            "Monsantos Geschaeftsbereiche werden in die Division Crop Science integriert. "
            "(2) Markensstrategie: Die Marke Monsanto wird schrittweise durch Bayer ersetzt. "
            "(3) Rechtsabteilung: Zusammenfuehrung der Rechtsabteilungen in Leverkusen und "
            "St. Louis. Deutsche Anwaelte werden in das US-Prozessmanagement eingebunden. "
            "(4) AKTUALISIERUNG RECHTSRISIKEN: Die Zahl der Roundup-Klagen ist seit "
            "Vertragsunterzeichnung auf ueber 8.000 angestiegen (gegenueber 2.000 bei "
            "Vertragsschluss). Der Vorstand nimmt diese Entwicklung mit Besorgnis zur "
            "Kenntnis. Die Rechtsabteilung wird beauftragt, eine aktualisierte "
            "Risikoanalyse vorzulegen. (5) Synergien: Geplante jaehrliche Synergien "
            "von 1,2 Milliarden USD bis 2022."
        ),
        "summary": "Post-Merger Integration. Roundup-Klagen auf 8.000 gestiegen (von 2.000 bei Vertragsschluss). Vorstand besorgt.",
        "language": "de",
        "doc_type": "board_minutes",
        "jurisdiction": "DE",
        "date": "2018-01-15",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Klagezahl vervierfacht", "Integrationsrisiko"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-BD-001", "LEX-INT-001"],
        "confidentiality": "internal",
        "tags": ["integration", "klagezahl", "post_merger"],
    },

    # --- Due Diligence Reports (3) ---
    {
        "id": "LEX-DD-001",
        "title": "Sorgfaltspruefung - Produkthaftungsrisiken USA",
        "content": (
            "VERTRAULICH - Bericht der rechtlichen Sorgfaltspruefung fuer die geplante "
            "Uebernahme der Monsanto Company. Abschnitt: Produkthaftungsrisiken in den USA. "
            "Zusammenfassung: Monsanto ist derzeit Beklagte in ca. 2.000 Produkthaftungsklagen "
            "im Zusammenhang mit Roundup-Herbiziden. Die Klaeger behaupten, dass Glyphosat "
            "Non-Hodgkin-Lymphome verursacht. RISIKOBEWERTUNG: (1) Rechtsgrundlage der Klagen: "
            "Die Klaeger stuetzen sich auf die IARC-Einstufung von Glyphosat als wahrscheinlich "
            "krebserregend (Gruppe 2A). (2) Verteidigungsposition: Monsantos Verteidigung basiert "
            "auf den Bewertungen der EPA und EFSA, die Glyphosat als nicht krebserregend einstufen. "
            "(3) Haftungsschaetzung: Bei einer angenommenen Vergleichssumme von 100.000-200.000 "
            "USD pro Klage und einer Anerkennungsquote von 50-60% ergibt sich ein geschaetztes "
            "Gesamtrisiko von 100-240 Millionen USD. (4) WORST-CASE-SZENARIO: Bei einem "
            "ungenuegenden Ausgang der Bellwether-Verfahren koennten sich die Vergleichswerte "
            "auf 500.000-1.000.000 USD pro Klage erhoehen. Worst-Case-Gesamtexposition: "
            "1-2 Milliarden USD. EMPFEHLUNG: Das Produkthaftungsrisiko ist als beherrschbar "
            "einzustufen und rechtfertigt keinen Abbruch der Uebernahmeverhandlungen."
        ),
        "summary": "Due Diligence schaetzt Roundup-Haftung auf 100-240 Mio USD (Worst Case: 1-2 Mrd). Als 'beherrschbar' bewertet.",
        "language": "de",
        "doc_type": "due_diligence_report",
        "jurisdiction": "DE",
        "date": "2016-08-30",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Unterschaetzte Haftung", "Produkthaftung", "Fehlbewertung"],
        "monetary_value": 2000000000,
        "regulatory_bodies": ["EPA", "IARC"],
        "contract_clauses": [],
        "related_docs": ["LEX-BD-001", "LEX-DD-002"],
        "confidentiality": "privileged",
        "tags": ["due_diligence", "produkthaftung", "unterschaetzung"],
    },
    {
        "id": "LEX-DD-002",
        "title": "Sorgfaltspruefung - Regulatorische Risiken Glyphosat",
        "content": (
            "VERTRAULICH - Bericht der regulatorischen Sorgfaltspruefung. Abschnitt: "
            "Regulatorische Risiken der Glyphosat-Registrierung weltweit. (1) USA: Die EPA hat "
            "die Neubewertung von Glyphosat eingeleitet. Eine Registrierungserneuerung wird "
            "fuer 2019 erwartet. Risiko eines Registrierungsentzugs: GERING. (2) EU: Die "
            "Europaeische Kommission hat die Genehmigung von Glyphosat im November 2017 um "
            "fuenf Jahre verlaengert. Einige Mitgliedstaaten (Frankreich, Oesterreich) haben "
            "nationale Verbote angekuendigt. Risiko eines EU-weiten Verbots: MITTEL. (3) Asien: "
            "Vietnam hat ein Importverbot fuer Glyphosat eingefuehrt. Thailand hat ein befristetes "
            "Verbot verhaengt. Risiko: GERING bis MITTEL je nach Markt. (4) Lateinamerika: "
            "Kolumbien hat die Anwendung von Glyphosat fuer Kokainvernichtung eingestellt. "
            "Ansonsten keine wesentlichen regulatorischen Risiken. GESAMTBEWERTUNG: Die "
            "regulatorischen Risiken sind diversifiziert und in der Gesamtheit als beherrschbar "
            "einzustufen. Ein weltweites Verbot von Glyphosat ist unwahrscheinlich."
        ),
        "summary": "Regulatorische Due Diligence: EPA-Risiko gering, EU-Verbot mittel. Gesamtbewertung: beherrschbar.",
        "language": "de",
        "doc_type": "due_diligence_report",
        "jurisdiction": "DE",
        "date": "2016-09-05",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Regulatorisches Risiko", "EU-Verbotsrisiko", "Internationale Restriktionen"],
        "monetary_value": 0,
        "regulatory_bodies": ["EPA", "EU Commission"],
        "contract_clauses": [],
        "related_docs": ["LEX-DD-001", "LEX-DD-003"],
        "confidentiality": "privileged",
        "tags": ["regulatorisch", "glyphosat", "eu_verbot"],
    },
    {
        "id": "LEX-DD-003",
        "title": "Finanzielle Bewertung - Klagenkomplex Roundup",
        "content": (
            "VERTRAULICH - Finanzielle Bewertung des Roundup-Klagenkomplexes fuer die "
            "Vorstandsentscheidung. Erstellt von der Finanzabteilung in Zusammenarbeit mit "
            "externen Beratern. METHODIK: Vergleichsanalyse historischer Massenschadensfaelle "
            "in den USA (Asbest, Tabak, Opioid-Krise). ERGEBNISSE: (1) Basissszenario: "
            "5.000 Klagen, durchschnittliche Vergleichssumme 100.000 USD = 500 Millionen USD. "
            "(2) Moderates Szenario: 15.000 Klagen, durchschnittliche Vergleichssumme "
            "200.000 USD = 3 Milliarden USD. (3) Pessimistisches Szenario: 50.000 Klagen, "
            "durchschnittliche Vergleichssumme 200.000 USD = 10 Milliarden USD. "
            "ANMERKUNG: Das pessimistische Szenario wurde als unwahrscheinlich eingestuft, "
            "da es eine zehnfache Zunahme der Klagezahl voraussetzt. EMPFEHLUNG: "
            "Einstellung einer Ruecklage von 1 Milliarde USD im Rahmen der Uebernahmeplanung. "
            "Die tatsaechliche Haftung wird voraussichtlich im Bereich des Basisszenarios liegen."
        ),
        "summary": "Finanzanalyse: 3 Szenarien von 500 Mio bis 10 Mrd USD. Pessimistisches Szenario als 'unwahrscheinlich' bewertet.",
        "language": "de",
        "doc_type": "due_diligence_report",
        "jurisdiction": "DE",
        "date": "2016-09-10",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Finanzielle Fehlbewertung", "Unterschaetzte Klagezahl", "Szenarienanalyse"],
        "monetary_value": 10000000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-DD-001", "LEX-BD-001"],
        "confidentiality": "privileged",
        "tags": ["finanzanalyse", "szenarien", "unterschaetzung"],
    },

    # --- BaFin Filings (2) ---
    {
        "id": "LEX-BAF-001",
        "title": "BaFin Meldung - Uebernahmevorhaben Bayer/Monsanto",
        "content": (
            "Pflichtmitteilung gemaess Wertpapiererwerbs- und Uebernahmegesetz (WpUeG). "
            "Die Bayer Aktiengesellschaft, Leverkusen, beabsichtigt, saemtliche Anteile der "
            "Monsanto Company, Wilmington, Delaware, USA, im Wege eines oeffentlichen "
            "Uebernahmeangebots zu erwerben. Der Angebotspreis betraegt 128 USD je Stammaktie "
            "der Monsanto Company. Das Gesamtvolumen der Transaktion belaeuft sich auf "
            "ca. 63 Milliarden USD. Die Transaktion soll durch eine Kombination aus "
            "Fremdkapital (ca. 57 Milliarden USD), einer Kapitalerhoehung und vorhandenen "
            "Barmitteln finanziert werden. Bayer hat verbindliche Finanzierungszusagen von "
            "Bank of America, Credit Suisse und HSBC erhalten. Die Durchfuehrung des Angebots "
            "steht unter dem Vorbehalt kartellrechtlicher Genehmigungen in den USA, der EU "
            "und weiteren Jurisdiktionen."
        ),
        "summary": "Pflichtmeldung an BaFin. 63 Mrd USD Uebernahme, finanziert durch 57 Mrd Fremdkapital plus Kapitalerhoehung.",
        "language": "de",
        "doc_type": "bafin_filing",
        "jurisdiction": "DE",
        "date": "2016-09-15",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Verschuldungsrisiko", "Finanzierungsrisiko"],
        "monetary_value": 63000000000,
        "regulatory_bodies": ["BaFin"],
        "contract_clauses": [],
        "related_docs": ["LEX-BAF-002", "LEX-SEC-002"],
        "confidentiality": "public",
        "tags": ["bafin", "pflichtmeldung", "uebernahme"],
    },
    {
        "id": "LEX-BAF-002",
        "title": "BaFin Pflichtmitteilung - Kontrollwechsel und Stimmrechtsmeldung",
        "content": (
            "Stimmrechtsmitteilung gemaess Paragraf 33 Wertpapierhandelsgesetz (WpHG). "
            "Die Bayer AG teilt mit, dass durch den Vollzug der Uebernahme der Monsanto "
            "Company die folgenden wesentlichen Aenderungen in der Beteiligungsstruktur "
            "eingetreten sind: (1) Bayer haelt nunmehr 100% der Stimmrechte an Monsanto. "
            "(2) Die Finanzierung der Transaktion hat zu einer Erhoehung der Nettoverschuldung "
            "auf ca. 35 Milliarden EUR gefuehrt. (3) Das Eigenkapitalverhaeltnis der Bayer AG "
            "hat sich von 38% auf 22% reduziert. Die BaFin wird ueber die Einhaltung der "
            "Offenlegungspflichten und die ordnungsgemaesse Abwicklung der Transaktion wachen. "
            "Bayer bestaetigt, dass alle erforderlichen kartellrechtlichen Genehmigungen "
            "eingeholt wurden, einschliesslich der Freigabe durch die EU-Kommission unter "
            "Auflagen (Veraeusserung bestimmter Geschaeftsbereiche an BASF)."
        ),
        "summary": "Kontrollwechsel-Meldung. Nettoverschuldung auf 35 Mrd EUR. Eigenkapitalquote von 38% auf 22% gesunken.",
        "language": "de",
        "doc_type": "bafin_filing",
        "jurisdiction": "DE",
        "date": "2018-06-07",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Verschuldung", "Eigenkapitalverduennung", "Bilanzrisiko"],
        "monetary_value": 35000000000,
        "regulatory_bodies": ["BaFin", "EU Commission"],
        "contract_clauses": [],
        "related_docs": ["LEX-BAF-001", "LEX-CRB-001"],
        "confidentiality": "public",
        "tags": ["bafin", "kontrollwechsel", "verschuldung"],
    },

    # --- Legal Memos (3) ---
    {
        "id": "LEX-MEM-001",
        "title": "Rechtsabteilung - Memorandum zur US-Produkthaftung",
        "content": (
            "VERTRAULICH - Memorandum der Rechtsabteilung der Bayer AG. Betreff: Grundzuege "
            "des US-amerikanischen Produkthaftungsrechts und Auswirkungen auf die "
            "Monsanto-Uebernahme. Das US-Produkthaftungsrecht unterscheidet sich grundlegend "
            "vom deutschen Recht: (1) STRICT LIABILITY: In den meisten US-Bundesstaaten "
            "haftet der Hersteller verschuldensunabhaengig fuer Produktfehler. Dies bedeutet, "
            "dass Monsanto auch dann haften kann, wenn es die Sorgfalt eines ordentlichen "
            "Herstellers beachtet hat. (2) PUNITIVE DAMAGES: US-Gerichte koennen Strafschadenersatz "
            "in Hoehe des Vielfachen des eigentlichen Schadens zusprechen. In Produkthaftungsfaellen "
            "koennen Punitive Damages die kompensatorischen Schaeden um das 10- bis 100-Fache "
            "uebersteigen. (3) CLASS ACTIONS und MDL: Das US-System ermoeglicht Sammelklagen "
            "und die Buendelung tausender Einzelklagen in einem Verfahren (Multidistrict "
            "Litigation). (4) CONTINGENCY FEES: Klaegeranwaelte arbeiten auf Erfolgsbasis, "
            "was die Klagebereitschaft erheblich senkt. BEWERTUNG: Das US-Produkthaftungssystem "
            "ist fuer europaeische Unternehmen besonders risikoreich. Die Kombination aus Strict "
            "Liability, Punitive Damages und dem MDL-System kann zu exponentiellen "
            "Haftungseskalationen fuehren."
        ),
        "summary": "Memo erklaert US-Produkthaftung: Strict Liability, Punitive Damages, MDL-System. Warnt vor exponentieller Eskalation.",
        "language": "de",
        "doc_type": "legal_memo",
        "jurisdiction": "DE",
        "date": "2016-07-20",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": [],
        "risk_factors": ["US Strict Liability", "Punitive Damages Risiko", "MDL-Eskalation"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-MEM-002", "LEX-DD-001"],
        "confidentiality": "privileged",
        "tags": ["rechtsanalyse", "produkthaftung", "us_recht", "punitive_damages"],
    },
    {
        "id": "LEX-MEM-002",
        "title": "Haftungsanalyse - Glyphosat-Klagen aus deutscher Perspektive",
        "content": (
            "VERTRAULICH - Memorandum der Rechtsabteilung. Analyse der Glyphosat-Klagen "
            "aus der Perspektive des deutschen Rechts. VERGLEICH: Im deutschen Recht waeren "
            "die Roundup-Klagen nach dem Produkthaftungsgesetz (ProdHaftG) zu beurteilen. "
            "Wesentliche Unterschiede: (1) Haftungshoechstgrenze: Das deutsche ProdHaftG "
            "begrenzt die Haftung auf 85 Millionen EUR fuer Personenschaeden durch gleichartige "
            "Fehler. In den USA gibt es keine solche Obergrenze. (2) Kein Strafschadenersatz: "
            "Punitive Damages sind im deutschen Recht nicht vorgesehen. (3) Beweislast: Im "
            "deutschen Recht muss der Klaeger den Kausalzusammenhang beweisen. In den USA "
            "genuegt unter Strict Liability der Nachweis eines Produktfehlers. (4) Keine "
            "Sammelklagen: Das deutsche Recht kennt kein Aequivalent zu Class Actions oder MDL. "
            "SCHLUSSFOLGERUNG: Die Haftungsrisiken der Monsanto-Uebernahme koennen nicht anhand "
            "deutscher Rechtsmasstaebe bewertet werden. Die Rechtsabteilung empfiehlt die "
            "Einschaltung spezialisierter US-Produkthaftungsanwaelte fuer eine unabhaengige "
            "Risikobewertung."
        ),
        "summary": "Vergleich DE/US Produkthaftungsrecht. Deutsches Recht: 85 Mio EUR Grenze, keine Punitive Damages. US: unbegrenzt.",
        "language": "de",
        "doc_type": "legal_memo",
        "jurisdiction": "DE",
        "date": "2016-08-05",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Rechtsvergleich DE/US", "Unbegrenzte US-Haftung", "Fehlende Expertise"],
        "monetary_value": 85000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-MEM-001", "LEX-MEM-003"],
        "confidentiality": "privileged",
        "tags": ["rechtsvergleich", "produkthaftung", "haftungsgrenze"],
    },
    {
        "id": "LEX-MEM-003",
        "title": "Vergleich der Freistellungsklauseln - Merger Agreement vs. Bestandsvertraege",
        "content": (
            "VERTRAULICH - Memorandum der Rechtsabteilung. Vergleichende Analyse der "
            "Freistellungsklauseln (Indemnification) in der Verschmelzungsvereinbarung "
            "und den bestehenden Monsanto-Vertraegen. ERGEBNISSE: (1) MERGER AGREEMENT: "
            "Die Verschmelzungsvereinbarung enthaelt eine Freistellungsklausel zugunsten "
            "von Bayer, die auf Verletzungen von Zusicherungen und Gewaehrleistungen "
            "beschraenkt ist. Die Freistellung ist auf 2 Milliarden USD begrenzt und "
            "unterliegt einem Freibetrag (Basket) von 250 Millionen USD. (2) MONSANTO "
            "DISTRIBUTIONSVERTRAEGE: Monsantos bestehende Distributionsvertraege enthalten "
            "UNBEGRENZTE Freistellungsklauseln zugunsten der Distribuoren fuer "
            "Produkthaftungsansprueche. Es bestehen ca. 200 solcher Vertraege weltweit. "
            "(3) LUECKE: Die Merger-Freistellung von 2 Milliarden USD steht in krassem "
            "Misverhaeltnis zu den unbegrenzten Freistellungsverpflichtungen gegenueber "
            "Distributoren. Nach Vollzug der Uebernahme werden diese unbegrenzten "
            "Verpflichtungen auf Bayer uebergehen."
        ),
        "summary": "Merger-Freistellung: 2 Mrd USD gedeckelt. Distributor-Vertraege: UNBEGRENZT. Massive Deckungsluecke identifiziert.",
        "language": "de",
        "doc_type": "legal_memo",
        "jurisdiction": "DE",
        "date": "2016-10-15",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": [],
        "risk_factors": ["Freistellungsluecke", "Unbegrenzte Distributorenhaftung", "Vertragsrisiko"],
        "monetary_value": 2000000000,
        "regulatory_bodies": [],
        "contract_clauses": [
            {"clause_type": "merger_indemnification_cap", "summary": "Merger-Freistellung auf 2 Mrd USD begrenzt", "language": "de"},
            {"clause_type": "unlimited_distributor_indemnity", "summary": "Unbegrenzte Freistellung in Distributionsvertraegen", "language": "de"},
        ],
        "related_docs": ["LEX-CON-001", "LEX-MRG-002"],
        "confidentiality": "privileged",
        "tags": ["freistellung", "indemnification", "deckungsluecke"],
    },

    # --- Integration Plans (2) ---
    {
        "id": "LEX-INT-001",
        "title": "Integrationsplan - Zusammenfuehrung der Rechtsabteilungen",
        "content": (
            "VERTRAULICH - Projektplan zur Integration der Rechtsabteilungen von Bayer AG "
            "und Monsanto Company. Phase 1 (Monate 1-6): Bestandsaufnahme aller laufenden "
            "Rechtsstreitigkeiten, Vertraege und regulatorischen Verfahren. Uebertragung der "
            "Prozessfuehrung fuer US-Verfahren an Bayer-Prozessmanagement. Phase 2 (Monate "
            "7-12): Harmonisierung der Compliance-Systeme und internen Richtlinien. "
            "Implementierung einheitlicher Vertragsstandards. Phase 3 (Monate 13-18): "
            "Konsolidierung der Rechtsabteilungsstandorte. KRITISCHER RISIKOFAKTOR: Die "
            "laufende Roundup-Litigation erfordert unmittelbare Aufmerksamkeit. Es werden "
            "mindestens 50 zusaetzliche US-Prozessanwaelte benoetigt. Die jaehrlichen "
            "Prozesskosten werden auf 400-600 Millionen USD geschaetzt. Die Integration "
            "wird durch Sprachbarrieren zwischen deutschen und amerikanischen Juristen "
            "erschwert. Empfehlung: Einrichtung eines bilingualen Litigation Management "
            "Teams in St. Louis."
        ),
        "summary": "Integrationsplan Rechtsabteilungen. 50 US-Anwaelte benoetigt. 400-600 Mio USD jaehrliche Prozesskosten.",
        "language": "de",
        "doc_type": "integration_plan",
        "jurisdiction": "DE",
        "date": "2018-03-01",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": [],
        "risk_factors": ["Integrationskosten", "Sprachbarrieren", "Prozesskosten"],
        "monetary_value": 600000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-BD-003", "LEX-INT-002"],
        "confidentiality": "internal",
        "tags": ["integration", "rechtsabteilung", "prozesskosten"],
    },
    {
        "id": "LEX-INT-002",
        "title": "Integrationsplan - IT-Systeme und Compliance",
        "content": (
            "VERTRAULICH - Projektplan zur Integration der IT-Systeme und "
            "Compliance-Infrastruktur. SCHWERPUNKTE: (1) Zusammenfuehrung der "
            "Dokumentenmanagementsysteme: Monsanto nutzt ein US-basiertes System "
            "mit ausschliesslich englischsprachiger Oberflaeche. Bayer verwendet "
            "SAP-basierte Loesungen mit deutscher Lokalisierung. Die Migration "
            "erfordert zweisprachige Indizierung aller Dokumente. (2) E-Discovery "
            "Readiness: Angesichts der laufenden Roundup-Litigation muss das "
            "konsolidierte System US-E-Discovery-Anforderungen erfuellen. "
            "Saemtliche relevanten Dokumente muessen in englischer Sprache "
            "durchsuchbar sein. (3) Compliance-Training: Alle Bayer-Mitarbeiter "
            "mit Zugang zu Monsanto-Daten muessen in US-Datenschutz und "
            "Litigation-Hold-Verfahren geschult werden. (4) Budget: Geschaetzte "
            "IT-Integrationskosten: 150-200 Millionen USD ueber drei Jahre."
        ),
        "summary": "IT-Integration: zweisprachige Dokumentensysteme, E-Discovery Readiness. Kosten: 150-200 Mio USD.",
        "language": "de",
        "doc_type": "integration_plan",
        "jurisdiction": "DE",
        "date": "2018-04-15",
        "parties": ["Bayer AG"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["IT-Integrationskosten", "E-Discovery Anforderungen", "Sprachbarrieren"],
        "monetary_value": 200000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-INT-001"],
        "confidentiality": "internal",
        "tags": ["it_integration", "compliance", "e_discovery"],
    },

    # --- Shareholder Communications (2) ---
    {
        "id": "LEX-SH-001",
        "title": "Einladung zur Hauptversammlung - Beschlussfassung Monsanto-Uebernahme",
        "content": (
            "BAYER AKTIENGESELLSCHAFT - Einladung zur ausserordentlichen Hauptversammlung "
            "am 28. April 2017 in Bonn. Tagesordnungspunkt: Genehmigung der geplanten "
            "Kapitalerhoehung zur teilweisen Finanzierung der Uebernahme der Monsanto "
            "Company. Der Vorstand und Aufsichtsrat empfehlen die Annahme des Beschlusses. "
            "BEGRUENDUNG: Die Uebernahme von Monsanto wird Bayer zum weltweit fuehrenden "
            "Unternehmen in der Agrarwirtschaft machen. Erwartete Synergien von 1,2 "
            "Milliarden USD jaehrlich ab 2022. Die strategischen Vorteile ueberwiegen "
            "die Risiken. HINWEIS AUF RISIKEN: Die Monsanto-Uebernahme ist mit Risiken "
            "verbunden, insbesondere: (a) Produkthaftungsklagen in den USA wegen "
            "Roundup-Herbiziden; (b) regulatorische Risiken; (c) Integrationsrisiken; "
            "(d) Verschuldungsrisiko. Details zu den Risiken entnehmen Sie bitte dem "
            "beigefuegten Uebernahmebericht."
        ),
        "summary": "Hauptversammlung zur Kapitalerhoehung. Synergien von 1,2 Mrd USD angepriesen. Risiken nur knapp erwaehnt.",
        "language": "de",
        "doc_type": "shareholder_communication",
        "jurisdiction": "DE",
        "date": "2017-03-15",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": [],
        "risk_factors": ["Aktionaersinformation", "Unzureichende Risikodarstellung"],
        "monetary_value": 0,
        "regulatory_bodies": ["BaFin"],
        "contract_clauses": [],
        "related_docs": ["LEX-SH-002", "LEX-BD-001"],
        "confidentiality": "public",
        "tags": ["hauptversammlung", "kapitalerhoehung", "aktionaere"],
    },
    {
        "id": "LEX-SH-002",
        "title": "Aktionaersbrief - Aktualisierte Risikobewertung Monsanto",
        "content": (
            "Sehr geehrte Aktionaere, der Vorstand der Bayer AG informiert Sie ueber "
            "den aktuellen Stand der Monsanto-Integration. Nach dem erfolgreichen "
            "Abschluss der Uebernahme im Juni 2018 schreitet die Integration planmaessig "
            "voran. Wir moechten Sie jedoch ueber eine wesentliche Entwicklung informieren: "
            "Die Zahl der Produkthaftungsklagen im Zusammenhang mit Roundup-Herbiziden hat "
            "sich seit Abschluss der Transaktion erheblich erhoeht. Derzeit sind weltweit "
            "ca. 11.200 Klagen anhaengig (gegenueber 8.000 zum Zeitpunkt des Closings und "
            "2.000 zum Zeitpunkt der Vertragsunterzeichnung). Bayer ist weiterhin ueberzeugt, "
            "dass Glyphosat bei sachgemaesser Anwendung sicher ist und wird sich gegen "
            "unberechtigt Klagen nachdrucklich verteidigen. Unser Ziel bleibt es, langfristig "
            "Werte fuer unsere Aktionaere zu schaffen. Die erwarteten Synergien der "
            "Monsanto-Integration von 1,2 Milliarden USD jaehrlich werden ab 2022 "
            "vollstaendig realisiert."
        ),
        "summary": "Aktionaersbrief: Klagen auf 11.200 gestiegen. War 2.000 bei Vertragsschluss. Synergien weiter betont.",
        "language": "de",
        "doc_type": "shareholder_communication",
        "jurisdiction": "DE",
        "date": "2018-11-30",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Klagenexplosion", "Aktionaerstransparenz"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-SH-001", "LEX-BD-003"],
        "confidentiality": "public",
        "tags": ["aktionaersbrief", "klagezahl", "transparenz"],
    },

    # --- German Contract Templates (2) ---
    {
        "id": "LEX-CON-DE-001",
        "title": "Bayer Produkthaftungs-Vertragsmuster fuer Distributoren",
        "content": (
            "MUSTERVERTRAG - Bayer AG Standardvertrag fuer Distributionsvereinbarungen. "
            "Paragraf 8 - Haftung und Freistellung: 8.1 Die Haftung des Herstellers fuer "
            "Sachmaengel ist auf Nachbesserung oder Ersatzlieferung beschraenkt. 8.2 Die "
            "Haftung fuer Mangelfolgeschaeden ist auf den vorhersehbaren, vertragstypischen "
            "Schaden begrenzt. 8.3 Die Gesamthaftung des Herstellers ist auf den zweifachen "
            "Jahresumsatz mit dem jeweiligen Distributor begrenzt. 8.4 Die Haftung fuer "
            "Vorsatz und grobe Fahrlaessigkeit sowie fuer Schaeden aus der Verletzung des "
            "Lebens, des Koerpers oder der Gesundheit bleibt unberuehrt. VERGLEICH MIT "
            "MONSANTO-VERTRAEGEN: Das Bayer-Vertragsmuster enthaelt Haftungsbegrenzungen, "
            "die in den Monsanto-Distributionsvertraegen vollstaendig fehlen. Die Integration "
            "erfordert die Harmonisierung der Vertragsstandards."
        ),
        "summary": "Bayer-Standard: Haftung auf 2x Jahresumsatz begrenzt. Monsanto-Vertraege: UNBEGRENZT. Harmonisierung noetig.",
        "language": "de",
        "doc_type": "contract_template",
        "jurisdiction": "DE",
        "date": "2017-06-01",
        "parties": ["Bayer AG"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Vertragsinkonsistenz", "Haftungsdivergenz"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "haftungsbegrenzung", "summary": "Haftung auf zweifachen Jahresumsatz begrenzt", "language": "de"}],
        "related_docs": ["LEX-CON-001", "LEX-MEM-003"],
        "confidentiality": "internal",
        "tags": ["vertragsmuster", "haftungsbegrenzung", "distributoren"],
    },
    {
        "id": "LEX-CON-DE-002",
        "title": "Bayer Freistellungsklausel-Muster fuer Lieferantenvertraege",
        "content": (
            "MUSTERVERTRAG - Bayer AG Standardfreistellungsklausel fuer Lieferantenvertraege. "
            "Paragraf 12 - Freistellung: 12.1 Der Lieferant stellt den Kaeufer von allen "
            "Anspruechen Dritter frei, die auf Maengeln des gelieferten Materials beruhen. "
            "12.2 Die Freistellungsverpflichtung ist auf den Nettorechnungswert der "
            "betroffenen Lieferung begrenzt. 12.3 Die Freistellung umfasst nicht Ansprueche, "
            "die auf der Weiterverarbeitung, Formulierung oder Kennzeichnung durch den "
            "Kaeufer beruhen. ANMERKUNG: Diese Freistellungsklausel entspricht dem "
            "deutschen Branchenstandard und reflektiert das Prinzip der verschuldensabhaengigen "
            "Haftung im deutschen Recht. Im Vergleich zu den US-amerikanischen Monsanto-Vertraegen "
            "(siehe LEX-CON-002) besteht ein erheblicher Unterschied in der Haftungsallokation."
        ),
        "summary": "Bayer-Standard: Freistellung auf Rechnungswert begrenzt. Kontrast zu unbegrenzter US-Praxis.",
        "language": "de",
        "doc_type": "contract_template",
        "jurisdiction": "DE",
        "date": "2017-06-01",
        "parties": ["Bayer AG"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Vertragsstandard-Divergenz"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "freistellung_begrenzt", "summary": "Freistellung auf Nettorechnungswert begrenzt", "language": "de"}],
        "related_docs": ["LEX-CON-002", "LEX-CON-DE-001"],
        "confidentiality": "internal",
        "tags": ["freistellungsklausel", "lieferanten", "branchenstandard"],
    },

    # --- German Risk Assessment (1) ---
    {
        "id": "LEX-RISK-DE-001",
        "title": "Interne Risikobewertung - Gesamtexposition nach Uebernahme",
        "content": (
            "STRENG VERTRAULICH - Aktualisierte Risikobewertung der Bayer AG Rechtsabteilung. "
            "Stand: Dezember 2018. Nach Vollzug der Monsanto-Uebernahme und den ersten "
            "Gerichtsverfahren (Johnson-Urteil: 289 Millionen USD, spaeter reduziert auf "
            "78,5 Millionen USD) wird die Risikoeinschaetzung grundlegend ueberarbeitet. "
            "AKTUALISIERTE ZAHLEN: (1) Anhaengige Klagen: 11.200 (gegenueber 2.000 bei "
            "Vertragsschluss). (2) Monatliche Neuzugaenge: ca. 1.500 Klagen. (3) Prognose "
            "Gesamtklagen bis 2020: 40.000-60.000. (4) Durchschnittliche Vergleichssumme "
            "nach Johnson-Urteil: 150.000-250.000 USD. (5) GESCHAETZTE GESAMTEXPOSITION: "
            "8-15 Milliarden USD. Dies liegt erheblich ueber der urspruenglichen "
            "Sorgfaltspruefung, die ein Worst-Case-Szenario von 1-2 Milliarden USD "
            "angenommen hatte. Die Due-Diligence-Bewertung hat die tatsaechliche "
            "Haftungsexposition um den Faktor 5-10 unterschaetzt. SOFORTMASSNAHMEN: "
            "(a) Einstellung einer Ruecklage von 5 Milliarden EUR; (b) Aufnahme von "
            "Vergleichsverhandlungen; (c) Einrichtung eines spezialisierten "
            "Prozessteams in St. Louis."
        ),
        "summary": "Aktualisierte Bewertung: 8-15 Mrd USD Exposition. Due Diligence hat um Faktor 5-10 unterschaetzt. 5 Mrd Ruecklage.",
        "language": "de",
        "doc_type": "risk_assessment",
        "jurisdiction": "DE",
        "date": "2018-12-15",
        "parties": ["Bayer AG"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["Massive Unterschaetzung", "Due-Diligence-Versagen", "Haftungsexplosion"],
        "monetary_value": 15000000000,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-DD-001", "LEX-DD-003", "LEX-RISK-001"],
        "confidentiality": "privileged",
        "tags": ["risikobewertung", "unterschaetzung", "haftungsexplosion"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# BILINGUAL / CROSS-REFERENCE DOCUMENTS — 8 documents
# ─────────────────────────────────────────────────────────────────────────────

BILINGUAL_DOCS = [
    # --- Merger Agreement (4) ---
    {
        "id": "LEX-MRG-001",
        "title": "Agreement and Plan of Merger - Key Terms Summary",
        "content": (
            "AGREEMENT AND PLAN OF MERGER dated September 14, 2016, by and among Bayer "
            "Aktiengesellschaft, KWA Investment Co. (a wholly-owned subsidiary of Bayer), "
            "and Monsanto Company. KEY TERMS: (1) MERGER CONSIDERATION: $128.00 per share "
            "in cash, representing a 44% premium over Monsanto's undisturbed stock price. "
            "Total transaction value: approximately $63 billion including net debt. "
            "(2) REPRESENTATIONS AND WARRANTIES: Monsanto represents that all material "
            "litigation has been disclosed in the Litigation Disclosure Schedule (Exhibit F). "
            "As of the date hereof, approximately 2,000 product liability claims related to "
            "Roundup herbicide are pending. (3) MATERIAL ADVERSE EFFECT: The MAE definition "
            "excludes the effect of pending or threatened litigation unless such litigation "
            "uses standard carve-outs (economy, markets, industry changes, weather, accounting). Notably, the words 'Roundup' and 'glyphosate' do not appear anywhere in the 301,000-word merger agreement. "
            "(4) INDEMNIFICATION: Bayer's indemnification rights for breaches of representations "
            "and warranties are capped at $2 billion and subject to a $250 million basket. "
            "(5) TERMINATION FEE: $2 billion payable by Monsanto if the agreement is terminated "
            "under certain circumstances. (6) REGULATORY APPROVALS: Required from DOJ, EC, "
            "and authorities in approximately 30 jurisdictions."
        ),
        "summary": "$63B merger. MAE uses standard carve-outs; Roundup not named. Indemnification capped at $2B. 2,000 Roundup claims pending.",
        "language": "en",
        "doc_type": "merger_agreement",
        "jurisdiction": "US",
        "date": "2016-09-14",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["MAE Threshold Inadequacy", "Indemnification Cap", "Disclosure Limitations"],
        "monetary_value": 63000000000,
        "regulatory_bodies": ["DOJ", "EU Commission"],
        "contract_clauses": [
            {"clause_type": "material_adverse_effect", "summary": "MAE uses standard carve-outs; Roundup/glyphosate not named in agreement", "language": "en"},
            {"clause_type": "indemnification_cap", "summary": "Indemnification capped at $2B with $250M basket", "language": "en"},
            {"clause_type": "termination_fee", "summary": "$2B reverse termination fee", "language": "en"},
        ],
        "related_docs": ["LEX-MRG-002", "LEX-SEC-002"],
        "confidentiality": "public",
        "tags": ["merger_agreement", "mae", "indemnification", "key_terms"],
    },
    {
        "id": "LEX-MRG-002",
        "title": "Verschmelzungsvertrag - Wesentliche Klauseln (Deutsche Zusammenfassung)",
        "content": (
            "ZUSAMMENFASSUNG DER WESENTLICHEN KLAUSELN des Verschmelzungsvertrages zwischen "
            "Bayer AG und Monsanto Company. (1) KAUFPREIS: 128 USD je Aktie, Gesamtvolumen "
            "ca. 63 Milliarden USD. (2) ZUSICHERUNGEN UND GEWAEHRLEISTUNGEN: Monsanto "
            "sichert zu, alle wesentlichen Rechtsstreitigkeiten offengelegt zu haben. Der "
            "Offenlegungsanhang (Exhibit F) listet ca. 2.000 Produkthaftungsklagen im "
            "Zusammenhang mit Roundup auf. (3) WESENTLICHE NACHTEILIGE VERAENDERUNG (MAE): "
            "Die MAE-Definition schliesst laufende Rechtsstreitigkeiten aus, sofern die "
            "standardmaessige Ausschluesse (Wirtschaft, Maerkte, Branche) enthaelt. KRITISCHE BEWERTUNG: "
            "Die MAE-Klausel adressiert Roundup-Rechtsstreitigkeiten nicht namentlich. Die Worte 'Roundup' und 'Glyphosat' erscheinen nicht im Verschmelzungsvertrag. Die Due-Diligence-Einschaetzung "
            "vom August 2016, die die tatsaechliche Haftung massiv unterschaetzt hat. "
            "(4) FREISTELLUNG: Bayer kann Freistellung fuer Verletzungen von Zusicherungen "
            "verlangen, begrenzt auf 2 Milliarden USD mit einem Freibetrag von 250 Millionen "
            "USD. Diese Obergrenze ist angesichts der tatsaechlichen Exposition von 10+ "
            "Milliarden USD voellig unzureichend."
        ),
        "summary": "Deutsche Zusammenfassung des Merger Agreement. MAE mit Standardausschluessen, Roundup nicht namentlich adressiert. Freistellung bei 2 Mrd.",
        "language": "de",
        "doc_type": "merger_agreement",
        "jurisdiction": "DE",
        "date": "2016-09-14",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["MAE-Schwelle unzureichend", "Freistellungsgrenze unzureichend"],
        "monetary_value": 63000000000,
        "regulatory_bodies": [],
        "contract_clauses": [
            {"clause_type": "mae_klausel", "summary": "MAE mit Standardausschluessen, keine spezifische Roundup-Schwelle", "language": "de"},
            {"clause_type": "freistellungsobergrenze", "summary": "Freistellung auf 2 Mrd USD begrenzt", "language": "de"},
        ],
        "related_docs": ["LEX-MRG-001", "LEX-MEM-003"],
        "confidentiality": "internal",
        "tags": ["verschmelzungsvertrag", "mae", "freistellung"],
    },
    {
        "id": "LEX-MRG-003",
        "title": "Representations and Warranties - Litigation Disclosure Analysis",
        "content": (
            "ANALYSIS OF REPRESENTATIONS AND WARRANTIES in the Agreement and Plan of Merger. "
            "Section 3.09 - Litigation: Monsanto represents that the Litigation Disclosure "
            "Schedule is complete and accurate as of the date of the agreement. REVIEW OF "
            "DISCLOSURE SCHEDULE (Exhibit F): The schedule lists approximately 2,000 Roundup "
            "product liability claims as of September 2016. GAPS IDENTIFIED: (1) The schedule "
            "does not include claims filed after the agreement date but before closing "
            "(approximately 6,000 additional claims). (2) The schedule does not quantify "
            "potential future claims or claim filing trends. (3) Internal Monsanto risk "
            "assessments projecting 20,000-50,000 total claims were NOT included in the "
            "disclosure schedule. (4) The ghostwriting and regulatory manipulation evidence "
            "that has surfaced in discovery was not specifically disclosed. (5) The schedule "
            "does not reference the approximately 200 distributor agreements with unlimited "
            "indemnification provisions. CONCLUSION: The representations and warranties in "
            "the merger agreement provided an incomplete picture of Monsanto's litigation "
            "exposure, potentially constituting a breach."
        ),
        "summary": "R&W analysis: Disclosure schedule incomplete. Internal 20-50K claim projections NOT disclosed. Potential breach.",
        "language": "en",
        "doc_type": "merger_agreement",
        "jurisdiction": "US",
        "date": "2019-06-15",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosate"],
        "risk_factors": ["Incomplete Disclosure", "Representation Breach", "Hidden Risk Projections"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [{"clause_type": "representations_warranties", "summary": "Litigation disclosure potentially incomplete - breach risk", "language": "en"}],
        "related_docs": ["LEX-MRG-001", "LEX-RISK-001"],
        "confidentiality": "privileged",
        "tags": ["representations", "warranties", "disclosure_gaps", "breach"],
    },
    {
        "id": "LEX-MRG-004",
        "title": "Gewaehrleistungen und Zusicherungen - Analyse der Offenlegungsluecken",
        "content": (
            "VERTRAULICH - Analyse der Gewaehrleistungen und Zusicherungen im "
            "Verschmelzungsvertrag. Die Rechtsabteilung der Bayer AG hat die Offenlegungen "
            "von Monsanto im Rahmen der Gewaehrleistungen einer nachtaeglichen Ueberpruefung "
            "unterzogen. ERGEBNISSE: (1) Die Offenlegung der Roundup-Klagen war zum Zeitpunkt "
            "des Vertragsschlusses formal korrekt (ca. 2.000 Klagen), spiegelte jedoch nicht "
            "das tatsaechliche Risikoprofil wider. (2) Monsantos interne Risikobewertung "
            "(Projektion: 20.000-50.000 Klagen, 2-7 Milliarden USD Haftung) wurde Bayer "
            "nicht zur Verfuegung gestellt. (3) Die englischsprachigen Gerichtsakten und "
            "internen Monsanto-Dokumente wurden von der deutschen Rechtsabteilung nicht "
            "vollstaendig ausgewertet. Schaetzungsweise 68% der relevanten US-Prozessakten "
            "haben keinen Niederschlag in den deutschsprachigen Due-Diligence-Berichten "
            "gefunden. (4) EMPFEHLUNG: Pruefung etwaiger Ansprueche aus Verletzung der "
            "Gewaehrleistungen, begrenzt durch die Freistellungsobergrenze von 2 Mrd USD."
        ),
        "summary": "68% der US-Prozessakten nicht in deutschen DD-Berichten beruecksichtigt. Interne Risikoprojektion nicht offengelegt.",
        "language": "de",
        "doc_type": "merger_agreement",
        "jurisdiction": "DE",
        "date": "2019-07-01",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": ["Roundup"],
        "chemicals": ["Glyphosat"],
        "risk_factors": ["68% Dokumentenluecke", "Unvollstaendige Auswertung", "Sprachbarriere"],
        "monetary_value": 0,
        "regulatory_bodies": [],
        "contract_clauses": [],
        "related_docs": ["LEX-MRG-003", "LEX-DD-001"],
        "confidentiality": "privileged",
        "tags": ["gewaehrleistung", "offenlegungsluecke", "sprachbarriere", "68_prozent"],
    },

    # --- Cross-Border Regulatory (4) ---
    {
        "id": "LEX-CRB-001",
        "title": "EU Commission Merger Approval - Conditional Clearance",
        "content": (
            "EUROPEAN COMMISSION - Case M.8084 - Bayer/Monsanto. The Commission has decided "
            "to declare the concentration compatible with the internal market and the EEA "
            "Agreement, subject to the following conditions: (1) DIVESTITURE: Bayer shall "
            "divest its entire vegetable seeds business, its digital agriculture business, "
            "certain herbicide businesses, and certain trait and breeding research. The "
            "divestiture package, valued at approximately EUR 7.6 billion, will be acquired "
            "by BASF. (2) RATIONALE: The Commission found that the merger as notified would "
            "significantly impede effective competition in seeds, traits, and pesticides "
            "markets. The divestitures eliminate horizontal overlaps and vertical concerns. "
            "(3) MONITORING: A Monitoring Trustee will oversee the divestiture process. "
            "NOTE: The Commission's review focused on competition concerns and did not "
            "assess product liability risks associated with Monsanto's Roundup litigation."
        ),
        "summary": "EU approves merger with EUR 7.6B divestiture to BASF. Competition focus only - no review of Roundup liability.",
        "language": "en",
        "doc_type": "cross_border_regulatory",
        "jurisdiction": "EU",
        "date": "2018-03-21",
        "parties": ["Bayer AG", "Monsanto Company", "BASF", "EU Commission"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Divestiture Costs", "No Liability Review by EC"],
        "monetary_value": 7600000000,
        "regulatory_bodies": ["EU Commission"],
        "contract_clauses": [],
        "related_docs": ["LEX-CRB-002", "LEX-CRB-003"],
        "confidentiality": "public",
        "tags": ["eu_commission", "merger_approval", "divestiture", "basf"],
    },
    {
        "id": "LEX-CRB-002",
        "title": "Bundeskartellamt Freigabebescheid - Bayer/Monsanto Zusammenschluss",
        "content": (
            "BUNDESKARTELLAMT - Beschluss in dem Zusammenschlussvorhaben B2-39/17 "
            "Bayer AG / Monsanto Company. Das Bundeskartellamt gibt den Zusammenschluss "
            "der Bayer AG mit der Monsanto Company frei. Die Freigabe erfolgt im Hinblick "
            "auf die von der Europaeischen Kommission verfuegten Auflagen und "
            "Veraeusserungen. Das Bundeskartellamt hat die Wettbewerbsauswirkungen auf "
            "den deutschen und europaeischen Saatgut- und Pflanzenschutzmarkt geprueft "
            "und kommt zu dem Ergebnis, dass der Zusammenschluss unter Beruecksichtigung "
            "der EU-Auflagen den wirksamen Wettbewerb nicht erheblich behindert. "
            "ANMERKUNG: Die kartellrechtliche Pruefung umfasst keine Bewertung der "
            "Produkthaftungsrisiken in den USA. Das Bundeskartellamt weist ausdruecklich "
            "darauf hin, dass die Freigabe keine Aussage ueber die wirtschaftliche "
            "Tragfaehigkeit der Transaktion beinhaltet."
        ),
        "summary": "Bundeskartellamt gibt Zusammenschluss frei. Keine Bewertung der US-Produkthaftungsrisiken vorgenommen.",
        "language": "de",
        "doc_type": "cross_border_regulatory",
        "jurisdiction": "DE",
        "date": "2018-03-15",
        "parties": ["Bayer AG", "Monsanto Company"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Keine Haftungspruefung", "Nur Wettbewerbsrecht"],
        "monetary_value": 0,
        "regulatory_bodies": ["Bundeskartellamt"],
        "contract_clauses": [],
        "related_docs": ["LEX-CRB-001"],
        "confidentiality": "public",
        "tags": ["bundeskartellamt", "freigabe", "kartellrecht"],
    },
    {
        "id": "LEX-CRB-003",
        "title": "DOJ Antitrust Division - Bayer/Monsanto Merger Review",
        "content": (
            "UNITED STATES DEPARTMENT OF JUSTICE - Antitrust Division. The Department of "
            "Justice announces that it will permit Bayer's acquisition of Monsanto to proceed, "
            "subject to the divestiture of approximately $9 billion in Bayer and Monsanto "
            "assets to BASF. The required divestitures include Bayer's Liberty herbicide "
            "and LibertyLink trait businesses, Bayer's cotton, soybean, and canola seed "
            "businesses, and Monsanto's vegetable seed business intellectual property. "
            "The Department found that without these divestitures, the transaction would "
            "likely substantially lessen competition in multiple seed and crop protection "
            "markets. The DOJ consent decree requires completion of divestitures within "
            "specified timeframes and includes provisions for a divestiture trustee. "
            "NOTE: The DOJ review was limited to antitrust considerations. The Department "
            "did not evaluate Monsanto's product liability exposure from Roundup litigation "
            "as part of its merger review."
        ),
        "summary": "DOJ permits merger with $9B divestiture to BASF. Antitrust only - no Roundup liability assessment.",
        "language": "en",
        "doc_type": "cross_border_regulatory",
        "jurisdiction": "US",
        "date": "2018-05-29",
        "parties": ["Bayer AG", "Monsanto Company", "BASF", "DOJ"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Divestiture Cost", "No Product Liability Review"],
        "monetary_value": 9000000000,
        "regulatory_bodies": ["DOJ"],
        "contract_clauses": [],
        "related_docs": ["LEX-CRB-001", "LEX-MRG-001"],
        "confidentiality": "public",
        "tags": ["doj", "antitrust", "divestiture", "basf"],
    },
    {
        "id": "LEX-CRB-004",
        "title": "CFIUS National Security Review - Agricultural Technology Assessment",
        "content": (
            "COMMITTEE ON FOREIGN INVESTMENT IN THE UNITED STATES (CFIUS) - Review of "
            "Bayer AG Acquisition of Monsanto Company. CFIUS has completed its review of "
            "the proposed acquisition and has determined that the transaction does not pose "
            "an unresolved national security risk. KEY CONSIDERATIONS: (1) Monsanto's "
            "agricultural biotechnology and digital farming platforms were evaluated for "
            "national security implications. (2) CFIUS required certain mitigation measures "
            "including data protection protocols for US agricultural data collected through "
            "Monsanto's Climate Corporation subsidiary. (3) The Committee required that "
            "Monsanto's seed trait genetic data remain accessible to US researchers and "
            "that critical agricultural technology not be transferred to restricted entities. "
            "(4) CFIUS did not evaluate product liability risks, environmental claims, or "
            "pending litigation as these fall outside the Committee's jurisdiction. The "
            "approval allows the transaction to proceed subject to compliance with the "
            "mitigation agreement."
        ),
        "summary": "CFIUS clears acquisition with data protection conditions. No review of product liability or litigation exposure.",
        "language": "en",
        "doc_type": "cross_border_regulatory",
        "jurisdiction": "US",
        "date": "2018-04-10",
        "parties": ["Bayer AG", "Monsanto Company", "CFIUS"],
        "products": [],
        "chemicals": [],
        "risk_factors": ["Data Security Requirements", "No Liability Review"],
        "monetary_value": 0,
        "regulatory_bodies": ["CFIUS"],
        "contract_clauses": [],
        "related_docs": ["LEX-CRB-003"],
        "confidentiality": "public",
        "tags": ["cfius", "national_security", "agricultural_technology"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE URLS — map each document to its real-world public reference
# ─────────────────────────────────────────────────────────────────────────────

SOURCE_URLS = {
    # --- Litigation filings (verified court documents) ---
    "LEX-LIT-001": "https://en.wikipedia.org/wiki/Johnson_v._Monsanto_Co.",
    "LEX-LIT-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-LIT-002.md",
    "LEX-LIT-003": "https://cdn.ca9.uscourts.gov/datastore/opinions/2021/05/14/19-16636.pdf",
    "LEX-LIT-004": "https://www.courtlistener.com/docket/4579168/in-re-roundup-products-liability-litigation/",
    "LEX-LIT-005": "https://www.reuters.com/legal/litigation/bayer-basf-must-pay-250-mln-peach-farmer-dicamba-case-us-jury-2024-02-09/",
    # --- Scientific studies (verified publications) ---
    "LEX-SCI-001": "https://publications.iarc.who.int/549",
    "LEX-SCI-002": "https://www.epa.gov/sites/default/files/2020-01/documents/glyphosate-interim-reg-review-decision-case-num-0178.pdf",
    "LEX-SCI-003": "https://pubmed.ncbi.nlm.nih.gov/31342895/",
    "LEX-SCI-004": "https://pubmed.ncbi.nlm.nih.gov/10854122/",
    # --- Regulatory correspondence (verified agency documents) ---
    "LEX-REG-001": "https://www.epa.gov/ingredients-used-pesticide-products/glyphosate",
    "LEX-REG-002": "https://www.iarc.who.int/wp-content/uploads/2018/07/MonographVolume112-1.pdf",
    "LEX-REG-003": "https://www.epa.gov/pesticides/epa-withdraws-glyphosate-interim-decision",
    # --- SEC filings (verified EDGAR — Monsanto CIK 1110783) ---
    "LEX-SEC-001": "https://www.sec.gov/Archives/edgar/data/1110783/000111078317000187/mon-20170831x10k.htm",
    "LEX-SEC-002": "https://www.sec.gov/Archives/edgar/data/1110783/000119312516714915/d234658d8k.htm",
    # --- Merger agreement (verified SEC filings) ---
    "LEX-MRG-001": "https://www.sec.gov/Archives/edgar/data/1110783/000119312516714915/d234658dex21.htm",
    "LEX-MRG-002": "https://www.sec.gov/Archives/edgar/data/1110783/000119312516765991/d252304ddefm14a.htm",
    "LEX-MRG-003": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-MRG-003.md",
    "LEX-MRG-004": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-MRG-004.md",
    # --- Competition / regulatory clearance (verified agency decisions) ---
    "LEX-CRB-001": "https://ec.europa.eu/commission/presscorner/detail/en/ip_18_2282",
    "LEX-CRB-002": "https://www.bundeskartellamt.de/SharedDocs/Meldung/EN/Pressemitteilungen/2018/15_03_2018_Bayer_Monsanto.html",
    "LEX-CRB-003": "https://www.justice.gov/archives/opa/pr/justice-department-secures-largest-merger-divestiture-ever-preserve-competition-threatened",
    "LEX-CRB-004": "https://www.justice.gov/atr/case/us-v-bayer-ag-and-monsanto-company",
    # --- Internal risk assessments (synthetic — modeled after Monsanto 10-K disclosures) ---
    "LEX-RISK-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-RISK-001.md",
    "LEX-RISK-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-RISK-002.md",
    # --- Insurance policies (synthetic) ---
    "LEX-INS-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-INS-001.md",
    "LEX-INS-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-INS-002.md",
    # --- Contracts (synthetic) ---
    "LEX-CON-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-CON-001.md",
    "LEX-CON-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-CON-002.md",
    # --- Settlements (verified news/press releases) ---
    "LEX-SET-001": "https://en.wikipedia.org/wiki/Johnson_v._Monsanto_Co.",
    "LEX-SET-002": "https://www.bayer.com/media/en-us/bayer-announces-agreements-to-resolve-major-legacy-monsanto-litigation/",
    # --- Bayer board minutes (synthetic) ---
    "LEX-BD-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-BD-001.md",
    "LEX-BD-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-BD-002.md",
    "LEX-BD-003": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-BD-003.md",
    # --- Due diligence (synthetic) ---
    "LEX-DD-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-DD-001.md",
    "LEX-DD-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-DD-002.md",
    "LEX-DD-003": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-DD-003.md",
    # --- Legal memos (synthetic) ---
    "LEX-MEM-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-MEM-001.md",
    "LEX-MEM-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-MEM-002.md",
    "LEX-MEM-003": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-MEM-003.md",
    # --- Integration plans (synthetic) ---
    "LEX-INT-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-INT-001.md",
    "LEX-INT-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-INT-002.md",
    # --- BaFin filings ---
    "LEX-BAF-001": "https://en.wikipedia.org/wiki/Bayer",
    "LEX-BAF-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-BAF-002.md",
    # --- Shareholder communications (from Bayer annual reports) ---
    "LEX-SH-001": "https://www.annualreports.com/HostedData/AnnualReportArchive/b/OTC_BAYZF_2017.pdf",
    "LEX-SH-002": "https://www.annualreports.com/HostedData/AnnualReportArchive/b/OTC_BAYZF_2018.pdf",
    # --- German contract templates (synthetic) ---
    "LEX-CON-DE-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-CON-DE-001.md",
    "LEX-CON-DE-002": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-CON-DE-002.md",
    # --- German risk assessment (synthetic) ---
    "LEX-RISK-DE-001": "https://github.com/pankajarm/LexBridge/blob/main/docs/synthetic_documents/LEX-RISK-DE-001.md",
}


# ─────────────────────────────────────────────────────────────────────────────
# ENTITY ALIASES (cross-lingual resolution)
# ─────────────────────────────────────────────────────────────────────────────

ENTITY_ALIASES = {
    "Bayer AG": ["Bayer", "Bayer CropScience"],
    "Monsanto Company": ["Monsanto", "Monsanto Co."],
    "Roundup": ["Roundup Ready", "Roundup PowerMax"],
    "Glyphosate": ["Glyphosat", "N-(phosphonomethyl)glycine"],
    "EPA": ["Environmental Protection Agency", "US EPA"],
    "BaFin": ["Bundesanstalt fuer Finanzdienstleistungsaufsicht"],
    "Non-Hodgkin Lymphoma": ["NHL", "Non-Hodgkin-Lymphom"],
    "Product Liability": ["Produkthaftung"],
    "Due Diligence": ["Sorgfaltspruefung"],
    "Indemnification": ["Freistellung", "Freistellungsklausel"],
    "Risk Assessment": ["Risikobewertung"],
    "Board Meeting": ["Vorstandssitzung"],
    "Settlement": ["Vergleich", "Vergleichsvereinbarung"],
    "Merger Agreement": ["Verschmelzungsvertrag"],
    "Material Adverse Effect": ["Wesentliche Nachteilige Veraenderung", "MAE"],
}


SCRAPED_CACHE_DIR = DATA_DIR / "scraped_cache"


def _load_scraped_cache() -> dict[str, str]:
    """Load scraped content from cache directory. Returns {doc_id: content_text}."""
    cache = {}
    if not SCRAPED_CACHE_DIR.exists():
        return cache
    for fpath in sorted(SCRAPED_CACHE_DIR.glob("LEX-*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            text = data.get("raw_text", "").strip()
            if text and len(text) > 100:
                cache[data["doc_id"]] = text
        except Exception as e:
            print(f"  Warning: could not load cache {fpath.name}: {e}")
    return cache


def main():
    """Generate documents: overlay scraped real content where available."""
    import os
    os.makedirs(DOCS_DIR, exist_ok=True)

    all_docs = ENGLISH_DOCS + GERMAN_DOCS + BILINGUAL_DOCS
    scraped = _load_scraped_cache()

    print(f"Generating {len(all_docs)} M&A due diligence documents...")
    print(f"  Scraped cache: {len(scraped)} documents with real content")

    overlay_count = 0
    for doc in all_docs:
        doc["source_url"] = SOURCE_URLS.get(doc["id"], "")
        if doc["id"] in scraped:
            doc["content"] = scraped[doc["id"]]
            overlay_count += 1

        filepath = DOCS_DIR / f"{doc['id']}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

    # Write entity aliases
    aliases_path = DOCS_DIR / "_entity_aliases.json"
    with open(aliases_path, "w", encoding="utf-8") as f:
        json.dump(ENTITY_ALIASES, f, indent=2, ensure_ascii=False)

    print(f"  English documents: {len(ENGLISH_DOCS)}")
    print(f"  German documents: {len(GERMAN_DOCS)}")
    print(f"  Bilingual documents: {len(BILINGUAL_DOCS)}")
    print(f"  Real content overlaid: {overlay_count} documents")
    print(f"  Synthetic content kept: {len(all_docs) - overlay_count} documents")
    print(f"  Entity aliases: {len(ENTITY_ALIASES)} entries")
    print(f"  Output: {DOCS_DIR}")


if __name__ == "__main__":
    main()
