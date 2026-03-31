const BASE_URL = '';
let currentSessionId = null; // ← global variable session store karne ke liye

async function uploadResume() {
    const fileInput = document.getElementById('resumeFile');
    if (!fileInput.files[0]) return alert("Please select a file!");

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    toggleLoading('uploadBtn', true);

    try {
        const response = await fetch(`${BASE_URL}/resume_analysis`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error("Upload failed");

        const data = await response.json();

        currentSessionId = data.session_id; // ← session_id save kar lo

        document.getElementById('extractionResult').classList.remove('hidden');
        document.getElementById('extRole').innerText = data.extracted.role || "";
        document.getElementById('extExp').innerText = data.extracted.experience || "";
        document.getElementById('recJob').innerText = data.recommended || "";
        document.getElementById('extSkills').innerText = (data.extracted.skills || []).join(", ");

    } catch (error) {
        alert("Error uploading resume. Check backend.");
        console.error(error);
    } finally {
        toggleLoading('uploadBtn', false);
    }
}

async function getDetailedAnalysis() {
    if (!currentSessionId) return alert("Pehle resume upload karo!"); // ← guard check

    try {
        const response = await fetch(`${BASE_URL}/resume_analysis/tell_me?session_id=${currentSessionId}`, {
            method: 'POST' // ← session_id automatically lag raha hai
        });

        if (!response.ok) throw new Error("Analysis failed");

        const data = await response.json();

        const resDiv = document.getElementById('analysisResult');
        resDiv.classList.remove('hidden');
        resDiv.innerText = data.analysis || "No data";

    } catch (error) {
        alert("Failed to get analysis.");
        console.error(error);
    }
}

async function getPercentageMatch() {
    const job = document.getElementById('desiredJob').value;
    if (!job) return alert("Enter a job title");
    if (!currentSessionId) return alert("Pehle resume upload karo!"); // ← guard check

    try {
        const response = await fetch(
            `${BASE_URL}/resume_analysis/percentage?session_id=${currentSessionId}&desired_job=${encodeURIComponent(job)}`,
            { method: 'POST' } // ← dono params automatically
        );

        if (!response.ok) throw new Error("Percentage failed");

        const data = await response.json();

        document.getElementById('percentageResult').classList.remove('hidden');
        document.getElementById('matchScore').innerText = data.analysis?.match_percentage ?? 0;

        let detailsHtml = `<b>Missing Skills:</b> ${(data.analysis?.missing_skills || []).join(", ")}<br><br>`;
        detailsHtml += `<b>Suggestions:</b> ${(data.analysis?.improvement_suggestions || []).join(". ")}`;

        document.getElementById('matchDetails').innerHTML = detailsHtml;

    } catch (error) {
        alert("Error calculating percentage.");
        console.error(error);
    }
}

function toggleLoading(btnId, isLoading) {
    const btn = document.getElementById(btnId);
    btn.innerText = isLoading ? "Processing..." : "Analyze & Extract";
    btn.disabled = isLoading;
}