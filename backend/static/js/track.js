async function trackTicket() {
    const id = document.getElementById("track_id").value;

    if (!id) {
        alert("Enter Ticket ID");
        return;
    }

    const res = await fetch(`/api/tickets/${id}`);
    const data = await res.json();

    const result = document.getElementById("result");

    if (res.ok) {
        result.innerHTML = `
            <p><b>Ticket ID:</b> ${data.ticket_id}</p>
            <p><b>Issue:</b> ${data.issue}</p>
            <p><b>Order ID:</b> ${data.order_id}</p>
            <p><b>Status:</b> ${data.status}</p>
            ${data.image_url ? `<img src="${data.image_url}">` : ""}
        `;
    } else {
        result.innerHTML = `<p style="color:red;">${data.error}</p>`;
    }
}