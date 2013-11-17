$(document).ready(function () {
    var cuntries_source =
    {
        datatype: "json",
        datafields: [
            { name: 'iso' },
            { name: 'eng_name' }
        ],
        url: "http://127.0.0.1:8000/countries"
    };
    var cities_source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'eng_name' }
        ],
        url: "http://127.0.0.1:8000/cities"
    };
    var airports_source =
    {
        datatype: "json",
        datafields: [
            { name: 'iata' },
            { name: 'eng_name' }
        ],
        url: "http://127.0.0.1:8000/airports"
    };
    var dataAdapterCountries = new $.jqx.dataAdapter(cuntries_source, {});
    var dataAdapterCities = new $.jqx.dataAdapter(cities_source, {});
    var dataAdapterAirports = new $.jqx.dataAdapter(airports_source, {});

    $("#countries").jqxGrid(
    {
        width: "100%",
        height: 460,
        source: dataAdapterCountries,
        filterable: true,
        columns: [
          { text: 'Select country', datafield: 'eng_name'}
        ]
    });
    $("#cities").jqxGrid(
    {
        width: "100%",
        height: 460,
        source: [],
        filterable: true,
        columns: [
          { text: 'Select city', datafield: 'eng_name'}
        ]
    });
    $("#airports").jqxGrid(
    {
        width: "100%",
        height: 460,
        source: [],
        filterable: true,
        columns: [
          { text: 'Select airport', datafield: 'eng_name'}
        ]
    });
});