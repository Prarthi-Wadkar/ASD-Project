const API_BASE = "http://localhost:5000/api"; // Points to backend container/service

function switchView(viewId) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.add('hidden'));
    document.getElementById(viewId).classList.remove('hidden');
    if (viewId === 'browse') fetchItems();
}

document.getElementById('lost-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        title: document.getElementById('lost-title').value,
        description: document.getElementById('lost-desc').value,
        location: document.getElementById('lost-location').value,
        date: document.getElementById('lost-date').value
    };

    const res = await fetch(`${API_BASE}/items/lost`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert('Lost item reported successfully!');
        e.target.reset();
    } else {
        alert('Error submitting report.');
    }
});

async function fetchItems() {
    const res = await fetch(`${API_BASE}/items`);
    const items = await res.json();
    const container = document.getElementById('items-list');
    container.innerHTML = items.map(item => `
        <div class="bg-white p-4 rounded shadow">
            <h3 class="font-bold text-lg">${item.title}</h3>
            <p>${item.description}</p>
            <p class="text-sm text-blue-500">Location: ${item.location}</p>
        </div>
    `).join('');
}