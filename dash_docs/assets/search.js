if (window.location.pathname.replace(/\//g, '') === 'search'){
	var interval = setInterval(searchInterval, 500);
    var searchSelector = '#search-input';
	function searchInterval(){
        if (!document.querySelector(searchSelector)) {
            return;
        }

		var search = instantsearch({
			// Replace with your own values
			appId: '7EK9KHJW8M',
			apiKey: '4dae07ded6a721de73bde7356eec9280',
			indexName: 'dash_docs',
			urlSync: false,
			searchFunction: function (helper) {
				if (helper.state.query === '') {
					document.querySelector('#hits').innerHTML = '';
					return;
				}

				helper.search();
			}
		});

		search.addWidget(
			instantsearch.widgets.searchBox({
				container: searchSelector,
				magnifier: false,
				reset: false,
				queryHook: function(query, search) {
					if (query === "") {
						search();
					} else {
						search(query);
					}
				}
			})
		);

		search.addWidget(
			instantsearch.widgets.hits({
				container: '#hits',
				templates: {
					item: document.getElementById('hit-template').innerHTML,
					empty: "We didn't find any results for the search <em>\"{{query}}\"</em>"
				}
			})
		);
		clearInterval(interval);

		search.start();
	};
};
