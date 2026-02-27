// ====================================
// ADD DONOR PAGE - /add_donor
// ====================================
const donorForm = document.getElementById('donorForm');
if (donorForm && window.location.pathname === '/add_donor') {
    donorForm.addEventListener('submit', function(e){
        e.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const cnic = document.getElementById('cnic').value;
        const phone = document.getElementById('phone').value;
        
        // Send to Flask properly
        fetch('/add_donor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                name: name,
                cnic: cnic,
                phone: phone
            })
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('message').innerText = "✅ Donor added successfully!";
            donorForm.reset();
            
            // Hide message after 3 seconds
            setTimeout(() => {
                document.getElementById('message').innerText = '';
            }, 3000);
        })
        .catch(error => {
            document.getElementById('message').innerText = "❌ Error adding donor!";
            console.error('Error:', error);
        });
    });
}

// ====================================
// ADD DONATION PAGE - /add_donation
// ====================================
const donationForm = document.getElementById('donationForm');
if (donationForm && window.location.pathname === '/add_donation') {
    donationForm.addEventListener('submit', function(e){
        e.preventDefault();
        
        // Get form values
        const donor_id = document.getElementById('donor_id').value;
        const amount = document.getElementById('amount').value;
        
        // Validate
        if (!donor_id || !amount) {
            document.getElementById('message').innerText = "❌ Please fill all fields!";
            return;
        }
        
        // Send to Flask
        fetch('/add_donation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                donor_id: donor_id,
                amount: amount
            })
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('message').innerText = "✅ Donation added successfully!";
            donationForm.reset();
            
            // Hide message after 3 seconds
            setTimeout(() => {
                document.getElementById('message').innerText = '';
            }, 3000);
        })
        .catch(error => {
            document.getElementById('message').innerText = "❌ Error adding donation!";
            console.error('Error:', error);
        });
    });
}

// ====================================
// ADD EXPENSE PAGE - /add_expense
// ====================================
const expenseForm = document.getElementById('expenseForm');
if (expenseForm && window.location.pathname === '/add_expense') {
    expenseForm.addEventListener('submit', function(e){
        e.preventDefault();
        
        // Get form values
        const description = document.getElementById('description').value;
        const amount = document.getElementById('amount').value;
        
        // Validate
        if (!description || !amount) {
            document.getElementById('message').innerText = "❌ Please fill all fields!";
            return;
        }
        
        // Send to Flask
        fetch('/add_expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                description: description,
                amount: amount
            })
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('message').innerText = "✅ Expense added successfully!";
            expenseForm.reset();
            
            // Hide message after 3 seconds
            setTimeout(() => {
                document.getElementById('message').innerText = '';
            }, 3000);
        })
        .catch(error => {
            document.getElementById('message').innerText = "❌ Error adding expense!";
            console.error('Error:', error);
        });
    });
}

// ====================================
// AUTO-HIDE MESSAGES (works on all pages)
// ====================================
const messageDiv = document.getElementById('message');
if (messageDiv && messageDiv.innerText) {
    setTimeout(() => {
        messageDiv.style.transition = 'opacity 1s';
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.innerText = '';
            messageDiv.style.opacity = '1';
        }, 1000);
    }, 3000);
}

// ====================================
// CONFIRM DELETE (for view pages)
// ====================================
const deleteButtons = document.querySelectorAll('.delete-btn');
deleteButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this?')) {
            e.preventDefault();
        }
    });
});