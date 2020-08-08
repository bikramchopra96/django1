queue()
    .defer(d3.json, "/boardgames/all")
    .await(makeGraphs);

function makeGraphs(error, boardGamesJson) {
	
	//Format boardGames data
	var boardGames = boardGamesJson;
	boardGames.forEach(function(d) {
		d["price"] = parseInt(d["price"]);
	});

	//Define Dimensions
	var GameCount = ndx.dimension(function(d) { return d["name"]; });
	var AgeGroup = ndx.dimension(function(d) { return d["min_age"]; });
	var Price = ndx.dimension(function(d) { return d["price"]; });
	var MaxPlayers = ndx.dimension(function(d) { return d["max_players"]; });
	var MaxPlaytime  = ndx.dimension(function(d) { return d["max_playtime"]; });
	var RedditCounts  = ndx.dimension(function(d) { return d["reddit_all_time_count"]; });


	//Calculate metrics
	var numGameCount = GameCount.group(); 
	var numAgeGroup = AgeGroup.group();
	var numPrice = Price.group();
	var totalGameCount = ndx.groupAll().reduceSum(function(d) {
		return count(d["name"]);
	});

	var all = ndx.groupAll();
	var totalDonations = ndx.groupAll().reduceSum(function(d) {return d["total_donations"];});

	var max_state = totalDonationsByState.top(1)[0].value;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["date_posted"];
	var maxDate = dateDim.top(1)[0]["date_posted"];

    //Charts
	var agePieChart = dc.barChart("#age-pie-chart");
	var priceBarChart = dc.rowChart("#price-bar-chart");
	var popularityTrendChart = dc.rowChart("#popularity-trend");

	agePieChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numProjectsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	priceBarChart
        .width(300)
        .height(250)
        .dimension(resourceTypeDim)
        .group(numProjectsByResourceType)
        .xAxis().ticks(4);

	popularityTrendChart
		.width(300)
		.height(250)
        .dimension(povertyLevelDim)
        .group(numProjectsByPovertyLevel)
        .xAxis().ticks(4);

    dc.renderAll();

};