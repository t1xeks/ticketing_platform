async function requestJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || `API request failed (HTTP ${response.status})`);
  }
  return data;
}

function showMessage(message, type = "info") {
  const box = document.getElementById("message-box");
  box.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function renderIssues(issues) {
  const body = document.getElementById("issues-body");
  body.innerHTML = "";
  issues.forEach((issue) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${issue.issue_id}</td>
      <td>${issue.employee_name}</td>
      <td>${issue.category}</td>
      <td>${issue.status}</td>
      <td>${issue.description}</td>
    `;
    body.appendChild(row);
  });
}

async function loadIssues() {
  try {
    const issues = await requestJSON("/api/issues");
    renderIssues(issues);
    showMessage("Issues loaded.", "success");
  } catch (error) {
    showMessage(error.message, "danger");
  }
}

async function createIssue() {
  const category = document.getElementById("issue-category").value.trim();
  const description = document.getElementById("issue-description").value.trim();
  if (!category || !description) {
    showMessage("Fill category and description before submit.", "warning");
    return;
  }
  try {
    await requestJSON("/api/issues", {
      method: "POST",
      body: JSON.stringify({ category, description }),
    });
    showMessage("Issue created.", "success");
    await loadIssues();
  } catch (error) {
    showMessage(error.message, "danger");
  }
}

document.getElementById("refresh-issues-btn").addEventListener("click", loadIssues);
const createButton = document.getElementById("create-issue-btn");
if (createButton) {
  createButton.addEventListener("click", createIssue);
}
loadIssues();
