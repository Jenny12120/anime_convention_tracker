let search_button = document.getElementById("search");


search_button.addEventListener("click", function(event) 
{
  let start_date = document.getElementById("start").value;
  let end_date = document.getElementById("end").value;
  let event_location = document.getElementById("location").value;
  let result = document.getElementById("search_result");
  let search_form = document.getElementById("form1")
  
  if (isStringValid(start_date) && isStringValid(end_date)) {
	  search_by_date(start_date, end_date);
  } else {
	  search_by_location(event_location)
  }
  search_form.reset()
  event.preventDefault()

});

async function search_by_date(start_date, end_date) {
	const url = `http://127.0.0.1:5000/api/search_conventions_by_date?start=${start_date}&end=${end_date}`;
	const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
    }
	const rawConventionData = await response.json();
	displayConventionsInTable(rawConventionData);
}

async function search_by_location(event_location) {
	const url = `http://127.0.0.1:5000/api/search_conventions_by_location?location=${event_location}`;
	const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
    }
	const rawConventionData = await response.json();
	displayConventionsInTable(rawConventionData);
}


function isStringValid(str) {
  return str !== null && str !== undefined && str.trim().length > 0;
}

function displayConventionsInTable(rawConventionData) {
    const tableBody = document.getElementById('conventions-body');
	let table = document.getElementById("results");
	let result = document.getElementById("search_result");

    tableBody.innerHTML = '';

	rawConventionData.forEach(convention => {
			const row = document.createElement('tr');
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
                {type: 'url', value: convention.url}
            ];
			

			fieldsData.forEach(field => {
				const cell = document.createElement('td');    
				if (field.type === 'url' && field.value) {
                    const link = document.createElement('a');
                    link.href = field.value;
                    link.textContent = field.value; 
					cell.appendChild(link);
				} else {
					cell.textContent = field.value;
				}

				row.appendChild(cell);
			});
			tableBody.appendChild(row);
		});
		
	if (rawConventionData.length > 0) {
		table.hidden = false;
	} else {
		table.hidden = true;
		result.textContent = "No conventions found in this date range.";
	}
}