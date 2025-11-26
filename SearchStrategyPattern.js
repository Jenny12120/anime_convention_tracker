export class SearchContext {
    constructor(searchStrategy) {
        this.searchStrategy = searchStrategy;
    }

    setSearchStrategy(searchStrategy) {
        this.searchStrategy = searchStrategy;
    }

    async performSearch(serachCriteria) {
        return this.searchStrategy.search(serachCriteria);
    }
}

class SearchStrategy {
    async search(serachCriteria) {
    }
}

export class LocationSearch extends SearchStrategy {
    async search(serachCriteria) {
		const event_location = serachCriteria.venue;
		
		const url = `http://127.0.0.1:5000/api/search_conventions_by_location?location=${event_location}`;
		const response = await fetch(url);
		
		if (!response.ok) {
			throw new Error(`Server error: ${response.statusText}`);
		}
		const rawConventionData = await response.json();
		return rawConventionData
    }
}

export class DateRangeSearch extends SearchStrategy {
    async search(serachCriteria) {
		const start_date = serachCriteria.start;
		const end_date = serachCriteria.end;
		
		const url = `http://127.0.0.1:5000/api/search_conventions_by_date?start=${start_date}&end=${end_date}`;
		const response = await fetch(url);
		
		if (!response.ok) {
			throw new Error(`Server error: ${response.statusText}`);
		}
		const rawConventionData = await response.json();
		return rawConventionData
    }
}


