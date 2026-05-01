function loadDashboard() {
    fetch("/api/grouped-tickets")
    .then(res => res.json())
    .then(data => {
        const dashboard = document.getElementById("dashboard");
        dashboard.innerHTML = "";

        if (data.length === 0) {
            dashboard.innerHTML = "<p class='empty'>No tickets found</p>";
            return;
        }

        data.forEach(ticket => {
            const card = document.createElement("div");
            card.className = "ticket-card";

            const isResolved = ticket.latest_status === "Resolved";

            card.innerHTML = `
                <div class="card-header">
                    <h3>Order: ${ticket.order_id}</h3>
                    <span class="status ${isResolved ? "resolved" : "pending"}">
                        ${ticket.latest_status}
                    </span>
                </div>

                <p><b>Issue:</b> ${ticket.issue}</p>
                <p><b>Total Tickets:</b> ${ticket.total_tickets}</p>
                <p class="date">${new Date(ticket.created_at).toLocaleString()}</p>

                ${
                    ticket.image_url
                    ? `<img class="ticket-img" src="${ticket.image_url}">`
                    : ""
                }

                <div class="actions">
                    <a href="/ticket/${ticket.latest_ticket_id}">
                        <button class="view-btn">View</button>
                    </a>
                </div>

                <div class="actions">
                    <button class="full-btn"
                        onclick="resolveTicket('${ticket.latest_ticket_id}', 'full')"
                        ${isResolved ? "disabled" : ""}>
                        Full Refund
                    </button>

                    <button class="partial-btn"
                        onclick="resolveTicket('${ticket.latest_ticket_id}', 'partial')"
                        ${isResolved ? "disabled" : ""}>
                        Partial
                    </button>

                    <button class="reject-btn"
                        onclick="resolveTicket('${ticket.latest_ticket_id}', 'reject')"
                        ${isResolved ? "disabled" : ""}>
                        Reject
                    </button>
                </div>

                ${isResolved ? "<p class='resolved-msg'>✔ Already Resolved</p>" : ""}
            `;

            dashboard.appendChild(card);
        });
    })
    .catch(err => {
        console.error(err);
        document.getElementById("dashboard").innerHTML = "Error loading dashboard";
    });
}


function resolveTicket(id, action) {
    if (!confirm("Are you sure you want to resolve this ticket?")) return;

    let amount = null;

    if (action === "partial") {
        amount = prompt("Enter refund amount:");
        if (!amount) return;
    }

    const note = prompt("Enter resolution note:");
    if (!note) return;

    fetch(`/api/resolve/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            action: action,
            amount: amount,
            note: note
        })
    })
    .then(res => res.json())
    .then(() => {
        alert("✅ Ticket Resolved");
        loadDashboard();
    })
    .catch(err => {
        alert("❌ Error resolving ticket");
        console.error(err);
    });
}

window.onload = loadDashboard;