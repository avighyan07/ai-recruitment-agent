// ============================================
// CONFIGURATION
// ============================================

const API_BASE_URL = "http://51.20.54.111:8000";


// ============================================
// HOME BUTTON
// ============================================

document.addEventListener("DOMContentLoaded", function () {

    const homeButton = document.getElementById("homeBtn");

    if (homeButton) {

        homeButton.addEventListener("click", function () {

            // Completely reset the frontend
            window.location.href = "/";

        });

    }

});


// ============================================
// FILE SELECTION
// ============================================

const resumeFiles = document.getElementById("resumeFiles");
const fileInfo = document.getElementById("fileInfo");


if (resumeFiles) {

    resumeFiles.addEventListener("change", function () {

        const files = resumeFiles.files;

        if (files.length === 0) {

            fileInfo.textContent =
                "You can upload multiple PDF resumes.";

            return;
        }

        fileInfo.textContent =
            `${files.length} resume(s) selected`;

    });

}


// ============================================
// START RECRUITMENT
// ============================================

async function startRecruitment() {

    const jobDescription =
        document.getElementById("jobDescription").value.trim();

    const files =
        document.getElementById("resumeFiles").files;

    const threshold =
        Number(
            document.getElementById("threshold").value
        );


    // ========================================
    // VALIDATION
    // ========================================

    if (!jobDescription) {

        alert("Please enter a job description.");

        return;
    }


    if (files.length === 0) {

        alert("Please upload at least one resume.");

        return;
    }


    if (threshold < 0 || threshold > 100) {

        alert("Threshold must be between 0 and 100.");

        return;
    }


    // ========================================
    // SHOW LOADING
    // ========================================

    const loading =
        document.getElementById("loading");

    const results =
        document.getElementById("results");

    const recruitButton =
        document.getElementById("recruitButton");


    loading.classList.remove("hidden");

    results.classList.add("hidden");

    recruitButton.disabled = true;


    try {

        // ====================================
        // STEP 1 — UPLOAD RESUMES
        // ====================================

        const formData = new FormData();


        for (let i = 0; i < files.length; i++) {

            formData.append(
                "files",
                files[i]
            );

        }


        const uploadResponse =
            await fetch(
                `${API_BASE_URL}/upload-resumes`,
                {
                    method: "POST",
                    body: formData
                }
            );


        if (!uploadResponse.ok) {

            throw new Error(
                "Resume upload failed."
            );

        }


        const uploadResult =
            await uploadResponse.json();


        console.log(
            "Upload result:",
            uploadResult
        );


        // ====================================
        // STEP 2 — RECRUIT
        // ====================================

        const recruitResponse =
            await fetch(
                `${API_BASE_URL}/recruit`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        job_description:
                            jobDescription,

                        threshold:
                            threshold

                    })
                }
            );


        if (!recruitResponse.ok) {

            const errorData =
                await recruitResponse.json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                "Recruitment failed."
            );

        }


        const recruitmentResult =
            await recruitResponse.json();


        console.log(
            "Recruitment result:",
            recruitmentResult
        );


        // ====================================
        // STEP 3 — DISPLAY RESULTS
        // ====================================

        displayResults(
            recruitmentResult
        );


    } catch (error) {

        console.error(
            "Recruitment error:",
            error
        );

        alert(
            "Error: " + error.message
        );

    } finally {

        loading.classList.add("hidden");

        recruitButton.disabled = false;

    }

}


// ============================================
// DISPLAY RESULTS
// ============================================

function displayResults(data) {

    const results =
        document.getElementById("results");

    const container =
        document.getElementById(
            "candidateContainer"
        );


    container.innerHTML = "";


    const candidates =
        data.candidates || [];


    // ========================================
    // NO CANDIDATES
    // ========================================

    if (candidates.length === 0) {

        container.innerHTML = `

            <div class="no-results">

                <h3>😕 No candidates found</h3>

                <p>
                    No candidates passed the
                    current screening threshold.
                </p>

            </div>

        `;

        results.classList.remove("hidden");

        return;
    }


    // ========================================
    // CREATE CANDIDATE CARDS
    // ========================================

    candidates.forEach(
        (candidate, index) => {

            const card =
                document.createElement("div");

            card.className =
                "candidate-card";


            const rank =
                candidate.rank ||
                index + 1;


            let medal = "";

            if (rank === 1) {
                medal = "🥇";
            }

            else if (rank === 2) {
                medal = "🥈";
            }

            else if (rank === 3) {
                medal = "🥉";
            }


            card.innerHTML = `

                <div class="candidate-header">

                    <h3>
                        ${medal}
                        #${rank}
                        ${candidate.candidate_name}
                    </h3>

                    <span class="score">
                        ${candidate.final_score}%
                    </span>

                </div>


                <p class="email">
                    ${candidate.email || "No email"}
                </p>


                <span class="status">
                    ${candidate.screening_status || "shortlisted"}
                </span>


                <div class="scores">

                    <div>
                        <strong>
                            ${candidate.required_skill_score}%
                        </strong>

                        <span>
                            Required Skills
                        </span>
                    </div>


                    <div>
                        <strong>
                            ${candidate.semantic_skill_score}%
                        </strong>

                        <span>
                            Semantic Skills
                        </span>
                    </div>


                    <div>
                        <strong>
                            ${candidate.preferred_skill_score}%
                        </strong>

                        <span>
                            Preferred Skills
                        </span>
                    </div>


                    <div>
                        <strong>
                            ${candidate.experience_score}%
                        </strong>

                        <span>
                            Experience
                        </span>
                    </div>

                </div>


                <button
                    class="analysis-btn"
                    onclick="showAnalysis('${candidate.candidate_id}')"
                >
                    🤖 View AI Recruiter Analysis
                </button>

            `;


            container.appendChild(card);

        }
    );


    // ========================================
    // STORE ANALYSIS
    // ========================================

    window.recruiterAnalysis =
        data.recruiter_analysis || [];


    results.classList.remove("hidden");

}


// ============================================
// SHOW AI RECRUITER ANALYSIS
// ============================================

function showAnalysis(candidateId) {

    const analyses =
        window.recruiterAnalysis || [];


    const analysis =
        analyses.find(
            item =>
                item.candidate_id ===
                candidateId
        );


    if (!analysis) {

        alert(
            "Recruiter analysis not available."
        );

        return;
    }


    const strengths =
        (analysis.strengths || [])
            .map(
                skill =>
                    `<li>✓ ${skill}</li>`
            )
            .join("");


    const gaps =
        (analysis.gaps || [])
            .map(
                skill =>
                    `<li>✗ ${skill}</li>`
            )
            .join("");


    alert(

        `AI RECRUITER ANALYSIS\n\n` +

        `Candidate: ${analysis.candidate_name}\n\n` +

        `Recommendation: ${analysis.recommendation}\n\n` +

        `Match Score: ${analysis.final_score}%\n\n` +

        `Strengths:\n` +
        (analysis.strengths || []).join(", ") +

        `\n\nGaps:\n` +
        (analysis.gaps || []).join(", ") +

        `\n\nSummary:\n` +
        analysis.summary

    );

}