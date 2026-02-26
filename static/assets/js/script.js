// Demo storage (in memory)
let donors = [];

// Add Donor
const donorForm = document.getElementById('donorForm');
if (donorForm) {
    donorForm.addEventListener('submit', function(e){
        e.preventDefault();
        const donor = {
            name: document.getElementById('name').value,
            cnic: document.getElementById('cnic').value,
            father: document.getElementById('father').value,
            address: document.getElementById('address').value,
            city: document.getElementById('city').value,
            phone: document.getElementById('phone').value
        };
        donors.push(donor);
        document.getElementById('message').innerText = "Donor added successfully!";
        donorForm.reset();
    });
}


const donorSelect = document.getElementById('donor');
if (donorSelect) {
    donors.forEach(d => {
        const option = document.createElement('option');
        option.value = d.name;
        option.textContent = d.name;
        donorSelect.appendChild(option);
    });
}
