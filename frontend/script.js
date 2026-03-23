const BASE_URL = 'http://127.0.0.1:8000';

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
        const data = await response.json();

        document.getElementById('extractionResult').classList.remove('hidden');
        document.getElementById('extRole').innerText = data.extracted.role;
        document.getElementById('extExp').innerText = data.extracted.experience;
        document.getElementById('recJob').innerText = data.recommended;
        document.getElementById('extSkills').innerText = data.extracted.skills.join(", ");
    } catch (error) {
        alert("Error uploading resume. Ensure backend is running.");
    } finally {
        toggleLoading('uploadBtn', false);
    }
}

async function getDetailedAnalysis() {
    try {
        const response = await fetch(`${BASE_URL}/resume_analysis/tell_me`, { method: 'POST' });
        const data = await response.json();
        const resDiv = document.getElementById('analysisResult');
        resDiv.classList.remove('hidden');
        resDiv.innerHTML = data.analysis;
    } catch (error) {
        alert("Failed to get analysis. Did you upload the resume first?");
    }
}

async function getPercentageMatch() {
    const job = document.getElementById('desiredJob').value;
    if (!job) return alert("Enter a job title");

    try {
        // Sending as query parameter as per your FastAPI definition
        const response = await fetch(`${BASE_URL}/resume_analysis/percentage?desired_job=${encodeURIComponent(job)}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        document.getElementById('percentageResult').classList.remove('hidden');
        document.getElementById('matchScore').innerText = data.analysis.match_percentage;
        
        let detailsHtml = `<b>Missing Skills:</b> ${data.analysis.missing_skills.join(", ")}<br><br>`;
        detailsHtml += `<b>Suggestions:</b> ${data.analysis.improvement_suggestions.join(". ")}`;
        document.getElementById('matchDetails').innerHTML = detailsHtml;
    } catch (error) {
        alert("Error calculating percentage.");
    }
}

function toggleLoading(btnId, isLoading) {
    const btn = document.getElementById(btnId);
    btn.innerText = isLoading ? "Processing..." : "Analyze & Extract";
    btn.disabled = isLoading;
}