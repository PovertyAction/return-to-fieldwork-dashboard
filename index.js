// References: 
//* https://leafletjs.com/examples/choropleth/
//* https://www.rgraph.net/canvas/sheets.html


//Get the covid data from gsheet
var covid_data = {};
var data = 'a';
var spreadsheetId = '1xvFTrmbjrJbYDHKej_AsEcCWEwsM7JCGxCdzYPZRQgk';

//Write everything inside this function, so that the map is built only once the covid data is loaded
new RGraph.Sheets(spreadsheetId, function (sheet)
{
    //Loading covid data
    data = sheet.get('C6:H26');
    for (var i = 0; i < data.length; i++){
        country = data[i][0];
        new_cases = data[i][1];
        doubling_rate = data[i][2];
        cases_per_100000 = data[i][3];
        government_restrictions = data[i][4];
        subnational_outbreak_status = data[i][5];

        covid_data[country] = {
                        "status":"red",
                        "new_cases":new_cases,
                        "doubling_rate":doubling_rate,
                        "cases_per_100000":cases_per_100000,
                        "government_restrictions":government_restrictions,
                        "subnational_outbreak_status":subnational_outbreak_status};
    }


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

    // Load countries geo data from json file
    var countriesData = (function() {
      var countries_json = null;
      $.ajax({
        'async': false,
        'global': false,
        'url': "./countries.json",
        'dataType': "json",
        'success': function(data) {
          countries_json = data;
        }
      });

      console.log(countries_json);

      //Include aditional covid data to geojson
      for (var i = 0; i < countries_json.features.length; i++) {
        country_name = countries_json.features[i].properties.name;
        if (country_name in covid_data) {
            countries_json.features[i].properties.status = covid_data[country_name].status;
            countries_json.features[i].properties.new_cases = covid_data[country_name].new_cases;
            countries_json.features[i].properties.doubling_rate = covid_data[country_name].doubling_rate;
            countries_json.features[i].properties.cases_per_100000 = covid_data[country_name].cases_per_100000;
            countries_json.features[i].properties.government_restrictions = covid_data[country_name].government_restrictions;
            countries_json.features[i].properties.subnational_outbreak_status = covid_data[country_name].subnational_outbreak_status;
        }
      }

      return countries_json;
    })();

    // Function to get color of country
    function getColor(d) {
        return d == 'red' ? 'red' :
               d == 'yellow' ? '#E89423' :
               d == 'green' ? '#81B53C' :
               '#CDCDCD';
    }



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
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
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
    geojson = L.geoJson(countriesData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);



    //Add control functionality

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
        this.update();
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {

        this._div.innerHTML = (props && props.status?
            '<p id="info-box"><br><b id="info-box-text" style="color: black;">' + props.name + '</b><br/>' + 
            '<br id="info-box-text">New cases per day(3-day avg): ' + props.new_cases + '<br />'+
            '<br id="info-box-text">Case doubling rate (days): ' + props.doubling_rate + '<br />'+
            '<br id="info-box-text">Cases per 100,000 people: ' + props.cases_per_100000 +'</p>'
            : '<p id="info-box">Hover over a country where IPA works</p>');
        // console.log(props.abbrev);

        if(props && props.status){
            update_text_boxes(props.government_restrictions, props.subnational_outbreak_status);
        }
        else{
            update_text_boxes("","");
        }
        
    };

    info.addTo(map);

    update_subtitle();



});

function update_subtitle(){
    document.getElementById("subtitle").innerHTML = "Regularly updated by IPA's Global Programs Director</br>To be used in assessing context for approving in-person field data collection"; 
}

function update_text_boxes(government_restrictions, subnational_outbreak_status){
    
    text_box = document.getElementById("text-boxes")
    text_box.innerHTML = ''

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



