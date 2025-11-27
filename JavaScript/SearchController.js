import {SearchContext, LocationSearch, DateRangeSearch} from '/Anime_Convention_Tracker/SearchStrategyPattern.js'
let search_button = document.getElementById("search");


search_button.addEventListener("click", function(event) 
{
  let start_date = document.getElementById("start").value;
  let end_date = document.getElementById("end").value;
  let event_location = document.getElementById("location").value;
  let result = document.getElementById("search_result");
  let search_form = document.getElementById("form1");
  let rawConventionData = {};
  let searchCriteria;
  let context = new SearchContext();
  
  if (isStringValid(start_date) && isStringValid(end_date)) {
    searchCriteria = { 
        start: start_date, 
        end: end_date 
    };
    context.setSearchStrategy(new DateRangeSearch());
  } else {
    searchCriteria = { 
        venue: event_location 
	};
    context.setSearchStrategy(new LocationSearch());
  }
  rawConventionData = context.performSearch(searchCriteria);
  
  rawConventionData
	.then(actualRawConventionData => {
		displayConventionsInTable(actualRawConventionData);
	})
  search_form.reset()
  event.preventDefault()

});

function isStringValid(str) {
  return str !== null && str !== undefined && str.trim().length > 0;
}

function displayConventionsInTable(rawConventionData) {
    const tableBody = document.getElementById('conventions-body');
	let table = document.getElementById("results");
	let no_result_found = document.getElementById("no_result");

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
                {type: 'url', value: convention.url},
				{type: 'button', value: 'Add'} 
            ];
			

			fieldsData.forEach(field => {
				const cell = document.createElement('td');    
				if (field.type === 'url' && field.value) {
                    const link = document.createElement('a');
                    link.href = field.value;
                    link.textContent = field.value; 
					cell.appendChild(link);
				} else if (field.type === 'button') {
					const button = document.createElement('button');
                    button.textContent = field.value; 
					button.style = "text-align: center;"
					cell.style = "text-align: center;"
					cell.appendChild(button);
				}else {
					cell.textContent = field.value;
				}

				row.appendChild(cell);
			});
			tableBody.appendChild(row);
		});
		
	if (rawConventionData.length > 0) {
		table.hidden = false;
		no_result_found.hidden = true;
	} else {
		table.hidden = true;
		no_result_found.hidden = false;
	}
}