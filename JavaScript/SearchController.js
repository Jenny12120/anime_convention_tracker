import {SearchContext, LocationSearch, DateRangeSearch} from '/Anime_Convention_Tracker/SearchStrategyPattern.js'
const search_button = document.getElementById("search");
const tableBody = document.getElementById("conventions-body");
const view_tracking = document.getElementById("view_tracking");

view_tracking.addEventListener("click", function(event) {
    window.open("TrackingPage.html");
})

tableBody.addEventListener("click", function(event) {
  if (event.target.closest('.add_to_tracking')) {
    const row = event.target.closest("tr");
    const convention_id = row.dataset.conventionId;
    const convention_name = row.dataset.conventionName;
    add_to_tracking(convention_id, convention_name);
  }       
})

async function add_to_tracking(convention_id, convention_name) {
    const url = `http://127.0.0.1:5000/api/add_to_tracking`;
    console.log(convention_id)
    console.log(convention_name)
    const response = await fetch(url, {method: "POST",
        headers: {
        'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
            id: convention_id,
            name: convention_name
        })
    })

  const success = document.getElementById("tracked");

  if (!response.ok) {
        success.textContent = "Failed to add to tracking list"
  } else {
        success.textContent = "Successfully to added to tracking list"
  }

  success.hidden = false;
  
  setTimeout(function() {
    success.hidden = true;
  }, 2000)
}

search_button.addEventListener("click", function(event) 
{
  const start_date = document.getElementById("start").value;
  const end_date = document.getElementById("end").value;
  const event_location = document.getElementById("location").value;
  const search_form = document.getElementById("search_form");
  let rawConventionData = {};
  let searchCriteria;
  const context = new SearchContext();
  
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

function displayConventionsInTable(conventionData) {
  const tableBody = document.getElementById('conventions-body');
	const table = document.getElementById("results");
	const no_result_found = document.getElementById("no_result");

    tableBody.innerHTML = '';

	conventionData.forEach(convention => {
			const row = document.createElement('tr');
      console.log(convention)
      row.setAttribute("data-convention-id", convention.convention_id);
      row.setAttribute("data-convention-name", convention.name);
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
					cell.style = "text-align: center;"
					cell.appendChild(setup_add_button(field, convention.convention_id));
				}else {
					cell.textContent = field.value;
				}

				row.appendChild(cell);
			});
			tableBody.appendChild(row);
		});
		
	if (conventionData.length > 0) {
		table.hidden = false;
		no_result_found.hidden = true;
	} else {
		table.hidden = true;
		no_result_found.hidden = false;
	}
}

function setup_add_button(field) {
  	const button = document.createElement('button');
    button.textContent = field.value; 
		button.style = "text-align: center;";
    button.classList = "add_to_tracking";

    return button;
}