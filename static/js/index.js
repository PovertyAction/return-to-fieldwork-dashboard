// References:
//* https://leafletjs.com/examples/choropleth/


CreateMap();
CreateTable();


function CreateMap(){

    var mapboxAccessToken = 'pk.eyJ1IjoiZmhhbGFtb3MiLCJhIjoiY2tibGE1dzNsMHV6ODJxcGc0c3ZiZDRlaSJ9.Ay9GTz6DHTpPB0RsmEF1Nw';
    var map = L.map('map').setView([0, 0], 1.5);
    var geojson;
    //Custom control to show country info
    var info = L.control();

    //Add layer to map
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/light-v9',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);



    // Combine covid data with countries shape
    var countries_covid_and_shape = (function() {
      // Travers countries shape and if country present in covid data, add that info
      for (var i = 0; i < countries_shape.features.length; i++) {
        country_name = countries_shape.features[i].properties.name;

        if (country_name in country_stats) {
            countries_shape.features[i].properties.status = country_stats[country_name].status;
            countries_shape.features[i].properties.new_cases = country_stats[country_name].new_cases;
            countries_shape.features[i].properties.doubling_rate = country_stats[country_name].doubling_rate;
            countries_shape.features[i].properties.cases_per_100000 = country_stats[country_name].cases_per_100000;
            countries_shape.features[i].properties.government_restrictions = country_stats[country_name].government_restrictions;
            countries_shape.features[i].properties.subnational_outbreak_status = country_stats[country_name].subnational_outbreak_status;
        }
      }

      return countries_shape;
    })();


    //Listeners:
    //Highlighted visually when countries they are hovered with a mouse
    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 3,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }

        info.update(layer.feature.properties);
    }
    //DeHighlight:
    function resetHighlight(e) {
        geojson.resetStyle(e.target);

        info.update();
    }

    function zoomToFeature(e) {
        map.fitBounds(e.target.getBounds());
    }

    //Define style function for map, obtaining color based on country status
    function style(feature) {
        return {
            fillColor: getColor(feature.properties.status),
            weight: 1,
            opacity: 1,
            color: '#CDCDCD',//'white',
            fillOpacity: 0.7
        };
    }

    //Add listeners to country layers
    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
            //click: zoomToFeature
        });
    }

    //Load geojson data, style and listeners to it
    geojson = L.geoJson(countries_covid_and_shape, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);



    //Add control functionality

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };

    function update_text_boxes(country_name, new_cases, doubling_rate, cases_per_100000, government_restrictions, subnational_outbreak_status){
        text_box = document.getElementById("text-boxes")
        text_box.innerHTML = ''

        if (country_name){
            text_box.innerHTML = '<h3>'+country_name+'</h3>'+
            '<p>New cases per day(3-day avg): ' + new_cases + '</br>'+
            'Case doubling rate (days): ' + doubling_rate + '</br>'+
            'Cases per 100,000 people: ' + cases_per_100000+'</p>';
        }

        if (government_restrictions){
            text_box.innerHTML = text_box.innerHTML +
            '<h3>Government restrictions</h3>'+
            '<p>'+government_restrictions+'</p>';
        }

        if (subnational_outbreak_status){
            text_box.innerHTML = text_box.innerHTML +
            '<h3>Subnational outbreak status</h3>'+
            '<p>'+subnational_outbreak_status+'</p>';
        }
    }

    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {

        // Removing pop-up for the moment
        // this._div.innerHTML = (props && props.status?
        //     '<p id="info-box"><br><b id="info-box-text" style="color: black;">' + props.name + '</b><br/>' +
        //     '<br id="info-box-text">New cases per day(3-day avg): ' + props.new_cases + '<br />'+
        //     '<br id="info-box-text">Case doubling rate (days): ' + props.doubling_rate + '<br />'+
        //     '<br id="info-box-text">Cases per 100,000 people: ' + props.cases_per_100000 +'</p>'
        //     : '<p id="info-box">Hover over a country where IPA works</p>');

        if(props && props.status){
            update_text_boxes(props.name,
                props.new_cases,
                props.doubling_rate,
                props.cases_per_100000,
                props.government_restrictions,
                props.subnational_outbreak_status);
        }
        else{
            update_text_boxes("","");
        }

    };

    info.addTo(map);

    //Update subtitle
    document.getElementById("subtitle").innerHTML = "Regularly updated by IPA's Global Programs Director</br>To be used in assessing context for approving in-person field data collection";

    function fill_map_keys(){
        //Change visibility of keys
        for (let rectangle of document.getElementsByClassName('key-container')){
            rectangle.style.visibility = 'visible';
        }
    }

    fill_map_keys();
}

// Function to get color of country based on status
function getColor(status) {
    return status == 'red' ? '#CA3433' :
           status == 'yellow' ? '#E89423' :
           status == 'green' ? '#81B53C' :
           '#FFFFFF';//#CDCDCD
}

//Get status of country based on its covid stats
function get_status(new_cases, doubling_rate, cases_per_100000){

    //Parse all arguments to integers
    new_cases = parseInt(new_cases.toString().replace(">",""))
    doubling_rate = parseInt(doubling_rate.toString().replace(">",""))
    cases_per_100000 = parseInt(cases_per_100000.toString().replace(">",""))

    if(new_cases<100 && (doubling_rate>=10 || doubling_rate<=0) && cases_per_100000<50){
        return 'yellow';
    }
    else{
        return 'red';
    }
}



//Build table. ReferenceÑ https://www.valentinog.com/blog/html-table/
function CreateTable(){

    function generateTableHead(table, data) {
      let thead = table.createTHead();
      let row = thead.insertRow();
      for (let key of data){
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);
      }
    }

    function getRegionColor(region){

    }

    function generateTable(table, country_stats) {

      let odd_region=false;

      //For every country
      for (let country of Object.keys(country_stats)) {
        //Create row
        let row = table.insertRow();

        row.style.background = getColor(country_stats[country].status);

        //Insert region of country
        let cell = row.insertCell();

        //Paint region cell differently if region changed respect to previous one
        region = country_stats[country]['region'];
        if(region!=""){
            odd_region = !odd_region;
        }
        if(odd_region){
            cell.style.background = '#81B53C';
        }
        else{
            cell.style.background = '#D9EAD3';
            cell.style.colspan="2";
        }

        let text = document.createTextNode(country_stats[country]['region']);
        cell.appendChild(text);


        //Insert name of country
        cell = row.insertCell();
        text = document.createTextNode(country);
        cell.appendChild(text);

        //Insert each info of the country
        for (let key of ["new_cases", "doubling_rate","cases_per_100000","government_restrictions","subnational_outbreak_status"]) {
            console.log(key);
            let cell = row.insertCell();
            let text = document.createTextNode(country_stats[country][key]);
            cell.appendChild(text);
        }
      }
    }

    let table = document.querySelector("table");

    generateTable(table, country_stats);
    generateTableHead(table, ['Region','Country', 'New cases per day','Case doubling rate','Cases per 100,000 people', 'Government restrictions', 'Subnational outbreak status']);
}
