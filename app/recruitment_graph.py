

from app.llm import llm

from langgraph.graph import (
    StateGraph,
    START,
    END
)
from app.schemas import RecruiterAnalysis

from app.graph_state import RecruitmentState

from app.job_analyzer import analyze_job_description

from app.vector_store import search_candidates

from app.matcher import calculate_match

from app.resume_analyzer import analyze_resume


# =====================================
# NODE 1 — Analyze Job
# =====================================

def analyze_job_node(
    state: RecruitmentState
):

    print("\n[1] Analyzing Job Description...")

    job_description = state["job_description"]

    job = analyze_job_description(
        job_description
    )

    return {
        "job_profile": job
    }


# =====================================
# NODE 2 — Retrieve Candidates
# =====================================

def retrieve_candidates_node(
    state: RecruitmentState
):

    print("\n[2] Retrieving Candidates...")

    job_description = state["job_description"]

    results = search_candidates(
        job_description,
        k=10
    )

    candidates = []

    # Used to prevent the same candidate
    # from appearing multiple times
    seen_candidates = set()

    for document, distance in results:

        candidate_id = document.metadata.get(
            "candidate_id"
        )

        candidate_name = document.metadata.get(
            "candidate_name",
            "Unknown"
        )

        email = document.metadata.get(
            "email",
            ""
        ).lower().strip()

        # ---------------------------------
        # Deduplicate by email
        # ---------------------------------

        if email:
            unique_key = email
        else:
            unique_key = candidate_id

        if unique_key in seen_candidates:
            continue

        seen_candidates.add(unique_key)

        # ---------------------------------
        # Add unique candidate
        # ---------------------------------

        candidates.append({

            "candidate_id":
                candidate_id,

            "candidate_name":
                candidate_name,

            "email":
                email,

            "resume_text":
                document.page_content,

            "distance":
                distance
        })

    print(
        f"Retrieved {len(candidates)} unique candidates."
    )

    return {
        "retrieved_candidates":
            candidates
    }

# =====================================
# NODE 3 — Match Candidates
# =====================================

def match_candidates_node(
    state: RecruitmentState
):

    print("\n[3] Matching Candidates...")

    job = state["job_profile"]

    candidates = state["retrieved_candidates"]

    ranked_candidates = []

    for candidate in candidates:

        resume_profile = analyze_resume(
            candidate["resume_text"]
        )

        match_result = calculate_match(
            resume_profile,
            job
        )

        ranked_candidates.append({

            "candidate_id":
                candidate["candidate_id"],

            "candidate_name":
                candidate["candidate_name"],

            "email":
                candidate["email"],

            "vector_distance":
                candidate["distance"],

            "required_skill_score":
                match_result[
                    "required_skill_score"
                ],

            "semantic_skill_score":
                match_result[
                    "semantic_skill_score"
                ],

            "preferred_skill_score":
                match_result[
                    "preferred_skill_score"
                ],

            "experience_score":
                match_result[
                    "experience_score"
                ],

            "final_score":
                match_result[
                    "final_score"
                ]
        })

    return {
        "ranked_candidates": ranked_candidates
    }

def filter_candidates_node(state: RecruitmentState):

    print("\n[4] Filtering Candidates...")

    candidates = state["ranked_candidates"]

    threshold = state["threshold"]

    shortlisted = 0
    rejected = 0

    for candidate in candidates:

        if candidate["final_score"] >= threshold:

            candidate["screening_status"] = "shortlisted"
            shortlisted += 1

        else:

            candidate["screening_status"] = "rejected"
            rejected += 1

    print(f"Threshold: {threshold}%")
    print(f"Shortlisted: {shortlisted}")
    print(f"Rejected: {rejected}")

    # IMPORTANT:
    # Keep ALL candidates
    return {
        "ranked_candidates": candidates
    }
# =====================================
# NODE 4 — Rank Candidates
# =====================================

def rank_candidates_node(
    state: RecruitmentState
):

    print("\n[6] Ranking Candidates...")

    candidates = state["ranked_candidates"]

    candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    for index, candidate in enumerate(
        candidates,
        start=1
    ):

        candidate["rank"] = index

    return {
        "ranked_candidates": candidates
    }


# =====================================
# NODE 5 — AI Recruiter Analysis
# =====================================

def recruiter_analysis_node(
    state: RecruitmentState
):

    print("\n[5] Generating AI Recruiter Analysis...")

    candidates = state["ranked_candidates"]

    analyses = []

    # ---------------------------------
    # Structured LLM
    # ---------------------------------

    structured_llm = llm.with_structured_output(
        RecruiterAnalysis
    )

    for candidate in candidates:

        prompt = f"""
You are an AI recruitment assistant.

Analyze the candidate against the job description.

JOB DESCRIPTION:
{state["job_description"]}

CANDIDATE:
Name: {candidate["candidate_name"]}

MATCH SCORE:
{candidate["final_score"]}%

REQUIRED SKILL SCORE:
{candidate["required_skill_score"]}%

SEMANTIC SKILL SCORE:
{candidate["semantic_skill_score"]}%

PREFERRED SKILL SCORE:
{candidate["preferred_skill_score"]}%

EXPERIENCE SCORE:
{candidate["experience_score"]}%

Instructions:

1. Identify the strongest relevant skills.
2. Identify important missing or weak skills.
3. Give a hiring recommendation.
4. Give a concise explanation.
5. Do NOT invent information.
6. Only use information provided above.

Recommendation should be one of:

- Strong Hire
- Consider
- Reject
"""

        try:

            response = structured_llm.invoke(
                prompt
            )

            analyses.append({

                "candidate_id":
                    candidate["candidate_id"],

                "candidate_name":
                    candidate["candidate_name"],

                "final_score":
                    candidate["final_score"],

                "recommendation":
                    response.recommendation,

                "strengths":
                    response.strengths,

                "gaps":
                    response.gaps,

                "summary":
                    response.summary
            })

        except Exception as e:

            print(
                f"LLM analysis failed for "
                f"{candidate['candidate_name']}: {e}"
            )

            analyses.append({

                "candidate_id":
                    candidate["candidate_id"],

                "candidate_name":
                    candidate["candidate_name"],

                "final_score":
                    candidate["final_score"],

                "recommendation":
                    "Unable to determine",

                "strengths":
                    [],

                "gaps":
                    [],

                "summary":
                    "AI analysis failed."
            })

    return {

        "recruiter_analysis":
            analyses
    }

# =====================================
# NODE 6 — Generate Final Report
# =====================================

def generate_report_node(
    state: RecruitmentState
):

    print("\n[7] Generating Final Report...")

    candidates = state["ranked_candidates"]
    analyses = state["recruiter_analysis"]

    # Create lookup by candidate ID
    analysis_map = {
        analysis["candidate_id"]: analysis
        for analysis in analyses
    }

    report_lines = []

    report_lines.append(
        "# AI RECRUITMENT REPORT"
    )

    report_lines.append(
        "=" * 50
    )

    for candidate in candidates:

        candidate_id = candidate["candidate_id"]

        analysis = analysis_map.get(
            candidate_id,
            {}
        )

        report_lines.append(
            f"\nRank {candidate['rank']}"
        )

        report_lines.append(
            f"Candidate: "
            f"{candidate['candidate_name']}"
        )

        report_lines.append(
            f"Match Score: "
            f"{candidate['final_score']}%"
        )

        report_lines.append(
            f"Recommendation: "
            f"{analysis.get('recommendation', 'N/A')}"
        )

        report_lines.append(
            f"Required Skills: "
            f"{candidate['required_skill_score']}%"
        )

        report_lines.append(
            f"Semantic Skills: "
            f"{candidate['semantic_skill_score']}%"
        )

        report_lines.append(
            f"Preferred Skills: "
            f"{candidate['preferred_skill_score']}%"
        )

        report_lines.append(
            f"Experience: "
            f"{candidate['experience_score']}%"
        )

        report_lines.append(
            "\nStrengths:"
        )

        for strength in analysis.get(
            "strengths",
            []
        ):

            report_lines.append(
                f"  + {strength}"
            )

        report_lines.append(
            "\nGaps:"
        )

        for gap in analysis.get(
            "gaps",
            []
        ):

            report_lines.append(
                f"  - {gap}"
            )

        report_lines.append(
            "\nRecruiter Summary:"
        )

        report_lines.append(
            analysis.get(
                "summary",
                "No analysis available."
            )
        )

        report_lines.append(
            "-" * 50
        )

    report = "\n".join(
        report_lines
    )

    return {
        "final_report": report
    }


# =====================================
# BUILD LANGGRAPH
# =====================================

builder = StateGraph(
    RecruitmentState
)


# -------------------------------------
# Add Nodes
# -------------------------------------

builder.add_node(
    "analyze_job",
    analyze_job_node
)

builder.add_node(
    "retrieve_candidates",
    retrieve_candidates_node
)

builder.add_node(
    "match_candidates",
    match_candidates_node
)
builder.add_node(
    "filter_candidates",
    filter_candidates_node
)
builder.add_node(
    "rank_candidates",
    rank_candidates_node
)

builder.add_node(
    "recruiter_analysis",
    recruiter_analysis_node
)

builder.add_node(
    "generate_report",
    generate_report_node
)


# =====================================
# EDGES
# =====================================

builder.add_edge(
    START,
    "analyze_job"
)

builder.add_edge(
    "analyze_job",
    "retrieve_candidates"
)

builder.add_edge(
    "retrieve_candidates",
    "match_candidates"
)

builder.add_edge(
    "match_candidates",
    "filter_candidates"
)

builder.add_edge(
    "filter_candidates",
    "recruiter_analysis"
)

builder.add_edge(
    "recruiter_analysis",
    "rank_candidates"
)

builder.add_edge(
    "rank_candidates",
    "generate_report"
)

# =====================================
# COMPILE GRAPH
# =====================================




recruitment_graph = builder.compile()