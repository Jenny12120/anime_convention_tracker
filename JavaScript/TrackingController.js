window.onload = load_interested_list;

const tableBody = document.getElementById("interested-body");

async function load_interested_list() {
  const url = `http://127.0.0.1:5000/api/get_all_tracked_conventions`;
  const response = await fetch(url);

  if (response.ok) {
    const rawConventionData = await response.json();
    displayConventionsInTable(rawConventionData);
  }
}

async function remove_from_tracking(convention_id, row) {
    const url = `http://127.0.0.1:5000/api/delete_from_tracking`;
    const response = await fetch(url, {
            method: "DELETE",
            headers: {
            'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                id: convention_id,
            })
        }
    );

    const deleted = document.getElementById("deleted");

    if (!response.ok) {
        deleted.textContent = "Failed to delete tracking list"
        deleted.hidden = false;
        setTimeout(function() {
            deleted.hidden = true;
            }, 2000)
	} 

    row.remove();  
}

tableBody.addEventListener("click", function(event) 
{
    if (event.target.closest('.remove_convention')) {
        const row = event.target.closest("tr");
        const tracking_id = row.dataset.trackingId;
        remove_from_tracking(tracking_id, row)
  }       
});


function displayConventionsInTable(conventionData) {
    const tableBody = document.getElementById('interested-body');
	let table = document.getElementById("interested");
	let empty_list = document.getElementById("no_item");

    tableBody.innerHTML = '';

	conventionData.forEach(convention => {
			const row = document.createElement('tr');
            row.setAttribute("data-tracking-id", convention.id);	
            row.setAttribute("data-url", convention.url);	

            const formatDate = (dateString) => {
                const parts = dateString.split(' ');
                const dateParts = parts.slice(0, 4);
                return dateParts.join(' '); 
            };
            const formatted_start_date = formatDate(convention.start_date);
            const formatted_end_date = formatDate(convention.end_date);
			
			const fieldsData = [
                {type: 'text', value: convention.name},
                {type: 'date', value: formatted_start_date},
                {type: 'date', value: formatted_end_date},
                {type: 'text', value: convention.venue},
				{type: 'button', value: 'Actions'} 
            ];
			

			fieldsData.forEach(field => {
				const cell = document.createElement('td');    
				if (field.type === 'url' && field.value) {
                    const link = document.createElement('a');
                    link.href = field.value;
                    link.textContent = field.value; 
					cell.appendChild(link);
				} else if (field.type === 'button') {
					setup_buttons(cell);
				} else {
					cell.textContent = field.value;
				}

				row.appendChild(cell);
			});
			tableBody.appendChild(row);
		});
		
	if (conventionData.length > 0) {
		table.hidden = false;
		empty_list.hidden = true;
	} else {
		table.hidden = true;
		empty_list.hidden = false;
	}

    function setup_buttons(cell) {
        const remove_button = document.createElement('button');
        const download_button = document.createElement('button');
        remove_button.textContent = "Remove"; 
        remove_button.classList = "remove_convention"
        download_button.textContent = "Download Calendar File"; 
        download_button.classList = "download_ics"
        remove_button.style = "text-align: center;"
        download_button.style = "text-align: center;"
        cell.style = "text-align: center;"
        const space = document.createTextNode('\u00A0');
        cell.appendChild(remove_button);
        cell.appendChild(space);
        cell.appendChild(download_button);
    }
}