async function makeReservation() {
    const courtNumber = document.getElementById('court').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const user = document.getElementById('user').value;

    const response = await fetch('/reservations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ courtNumber, date, time, user })
    });

    if (response.ok) {
        alert('Reservation successful!');
    } else {
        const result = await response.json();
        alert(result.message);
    }
}

async function checkAvailability() {
    const courtNumber = document.getElementById('checkCourt').value;
    const date = document.getElementById('checkDate').value;
    const response = await fetch(`/courts/${courtNumber}/availability?date=${date}`);

    if (response.ok) {
        const reservations = await response.json();
        const availabilityList = document.getElementById('availabilityList');
        availabilityList.innerHTML = '';

        reservations.forEach(reservation => {
            const li = document.createElement('li');
            li.textContent = `Time: ${reservation.time} - Reserved by ${reservation.user}`;
            availabilityList.appendChild(li);
        });
    } else {
        alert('Error checking availability');
    }
}
