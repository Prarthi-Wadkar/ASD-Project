const API_BASE = "http://localhost:5000/api";

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Request failed.");
    }

    return data;
}

function switchView(viewId) {
    document.querySelectorAll(".view-section").forEach((section) => {
        section.classList.add("hidden");
    });

    document.getElementById(viewId)?.classList.remove("hidden");

    if (viewId === "browse") {
        fetchItems();
    }
}

function getItemPayload(prefix) {
    return {
        title: document.getElementById(`${prefix}-title`).value.trim(),
        description: document.getElementById(`${prefix}-desc`).value.trim(),
        category: document.getElementById(`${prefix}-category`)?.value || "other",
        location: document.getElementById(`${prefix}-location`).value.trim(),
        date: document.getElementById(`${prefix}-date`).value
    };
}

async function submitItem(event, itemType) {
    event.preventDefault();

    const form = event.currentTarget;
    const prefix = itemType === "lost" ? "lost" : "found";

    try {
        await apiRequest(`${API_BASE}/items/${itemType}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(getItemPayload(prefix))
        });

        alert(`${itemType === "lost" ? "Lost" : "Found"} item reported successfully!`);
        form.reset();
        switchView("browse");
    } catch (error) {
        alert(error.message || "Unable to connect to the backend.");
    }
}

document.getElementById("lost-form")?.addEventListener("submit", (event) => {
    submitItem(event, "lost");
});

document.getElementById("found-form")?.addEventListener("submit", (event) => {
    submitItem(event, "found");
});

async function fetchItems() {
    const container = document.getElementById("items-list");
    container.innerHTML = '<p class="text-gray-500">Loading items...</p>';

    try {
        const items = await apiRequest(`${API_BASE}/items`);

        if (!items.length) {
            container.innerHTML = '<p class="text-gray-500">No items reported yet.</p>';
            return;
        }

        container.innerHTML = items.map((item) => `
            <article class="bg-white p-5 rounded-lg shadow">
                <div class="flex flex-wrap justify-between gap-2 mb-2">
                    <h3 class="font-bold text-lg">${escapeHTML(item.title)}</h3>
                    <span class="px-3 py-1 rounded text-sm ${
                        item.item_type === "lost"
                            ? "bg-red-100 text-red-700"
                            : "bg-green-100 text-green-700"
                    }">
                        ${escapeHTML(item.item_type).toUpperCase()} ITEM
                    </span>
                </div>

                <p class="text-gray-700 mb-2">${escapeHTML(item.description)}</p>
                <p class="text-sm text-gray-600">
                    Category: ${escapeHTML(item.category)}
                </p>
                <p class="text-sm text-blue-600">
                    Location: ${escapeHTML(item.location)}
                </p>
                <p class="text-sm text-gray-500 mb-4">
                    Date: ${escapeHTML(item.date)}
                </p>

                ${item.item_type === "lost" ? `
                    <button
                        type="button"
                        onclick="showMatches(${Number(item.id)})"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
                        Find Matches
                    </button>
                    <div id="matches-${Number(item.id)}" class="mt-4"></div>
                ` : ""}
            </article>
        `).join("");
    } catch (error) {
        container.innerHTML = `
            <p class="text-red-600">
                Could not load items: ${escapeHTML(error.message)}
            </p>
            <button onclick="fetchItems()"
                class="mt-2 bg-blue-600 text-white px-3 py-2 rounded">
                Try Again
            </button>
        `;
    }
}

async function showMatches(lostItemId) {
    const container = document.getElementById(`matches-${lostItemId}`);

    if (!container) return;

    container.innerHTML =
        '<p class="text-gray-500">Calculating possible matches...</p>';

    try {
        const result = await apiRequest(
            `${API_BASE}/matches/${lostItemId}`
        );

        if (!result.matches.length) {
            container.innerHTML = `
                <p class="text-gray-600">
                    No found items available to compare yet.
                </p>
            `;
            return;
        }

        container.innerHTML = `
            <h4 class="font-semibold text-lg mb-3">Matching Results</h4>
            <div class="space-y-3">
                ${result.matches.map((match) => {
                    const score = Number(match.score);
                    const safeScore = Number.isFinite(score)
                        ? Math.max(0, Math.min(100, score))
                        : 0;

                    const badgeClass =
                        match.label === "High Match"
                            ? "bg-green-100 text-green-800"
                            : match.label === "Possible Match"
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-gray-100 text-gray-700";

                    const found = match.found_item;

                    return `
                        <div class="border rounded-lg p-4">
                            <div class="flex flex-wrap items-center justify-between gap-2">
                                <h5 class="font-semibold">
                                    ${escapeHTML(found.title)}
                                </h5>
                                <span class="px-3 py-1 rounded-full text-sm font-semibold ${badgeClass}">
                                    ${escapeHTML(match.label)}
                                </span>
                            </div>

                            <p class="text-2xl font-bold text-blue-700 mt-2">
                                ${safeScore.toFixed(2)}% Match
                            </p>

                            <div class="w-full bg-gray-200 rounded-full h-3 mt-2 mb-3">
                                <div
                                    class="bg-blue-600 h-3 rounded-full"
                                    style="width: ${safeScore}%">
                                </div>
                            </div>

                            <p class="text-sm text-gray-600 mb-3">
                                ${escapeHTML(found.description)}
                            </p>

                            <p class="text-sm text-gray-600">
                                Location: ${escapeHTML(found.location)}
                            </p>

                            <p class="font-medium mt-3 mb-2">
                                Score Breakdown
                            </p>

                            <div class="grid grid-cols-2 gap-2 text-sm">
                                ${Object.entries(match.breakdown || {}).map(
                                    ([key, value]) => `
                                        <div class="bg-gray-50 p-2 rounded">
                                            <span class="capitalize">
                                                ${escapeHTML(key)}
                                            </span>
                                            <strong class="float-right">
                                                ${Number(value).toFixed(2)}%
                                            </strong>
                                        </div>
                                    `
                                ).join("")}
                            </div>
                        </div>
                    `;
                }).join("")}
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <p class="text-red-600">
                Could not calculate matches: ${escapeHTML(error.message)}
            </p>
        `;
    }
}