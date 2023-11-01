async function sendDataToBackend(data, endpoint) {
    try {
        const response = await fetch(`http://localhost:5000/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            console.log('Response status:', response.status, response.statusText);
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    }
}



function getFormData() {
    const resume = document.getElementById("resume").value;
    const interests = document.getElementById("interests").value;
    const draft = document.getElementById("draft").value;
    const school = document.getElementById("school").value;
    const prompt = document.getElementById("prompt").value;

    return {
        resume,
        interests,
        draft,
        school,
        prompt
    };
}

function submitStudentData() {
    const data = getFormData();
    sendDataToBackend(data, 'submit')
        .then(response => {
            if (response.message === "Data saved successfully") {
                generateEssay();
            }
        });
}

function generateEssay() {
    const data = getFormData();
    sendDataToBackend(data, 'submit_and_generate')
        .then(response => {
            const outputDiv = document.getElementById("output");
            outputDiv.innerHTML = response.generated_essay;
        });
}

document.addEventListener("DOMContentLoaded", function() {
    const submitBtn = document.getElementById("submitBtn");
    submitBtn.addEventListener("click", submitStudentData);
});

function updatePromptOptions() {
    const school = document.getElementById("school").value;
    const promptSelect = document.getElementById("prompt");

    // Clear previous options
    promptSelect.innerHTML = "";
    
    // Create new options based on the selected school
    const essay1 = document.createElement("option");
    essay1.value = `${school} supplemental essay 1`;
    essay1.text = `${school} supplemental essay 1`;
    promptSelect.add(essay1);

    const whySchool = document.createElement("option");
    whySchool.value = `${school} Why School Essay`;
    whySchool.text = `${school} Why School Essay`;
    promptSelect.add(whySchool);

    const howFit = document.createElement("option");
    howFit.value = `${school} How would you fit`;
    howFit.text = `${school} How would you fit`;
    promptSelect.add(howFit);
}
