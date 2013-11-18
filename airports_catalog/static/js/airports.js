var link_country = '<strong>&gt Select country</strong>';
var link_city = link_country.replace('Select country', '<a id="link_tab_country">COUNTRY</a> &gt Select city ');
var link_airport = link_city.replace('Select city', '<a id="link_tab_city">CITY</a> &gt Select airport');
var link_all = link_airport.replace('Select airport', '<a id="link_tab_airport">AIRPORT</a>');
var link_search = '<strong>&gt Select </strong>';
var actual_country = '',
    actual_city = '',
    actual_airport = '',
    actual_link = '';

    var source =
    {
        datatype: "json",
        datafields: [
            { name: "id" },
            { name: "eng_name" }
        ],
        id: "id",
        data: {},
        url: "http://127.0.0.1:8000/get_rows"
    };

$(document).ready(function () {
    upload_link(link_country)
    $("#myLabel")[0].innerHTML = actual_link

    var data_grid = {"model":"Country"};
    create_data_grid(data_grid, "countries", "country", "Country")
    $("#total_search").click(search)
    $("#country_btn").click(select_country)
    $("#city_btn").click(select_city)

    bind_row_select("countries", "Country", "country_");
    bind_row_select("cities", "City", "city_");
    bind_row_select("airports", "Airport", "airport_");
    $("#airports").bind("rowselect", function (event){
        actual_airport = event.args.row.eng_name;
        window.setTimeout(function (){
            upload_link(link_all);
            $("#myLabel")[0].innerHTML = actual_link;
            bind_click_show_tab('country')
            bind_click_show_tab('city')
            bind_click_show_tab('airport')
        }, 500);
    });

});

function get_row(args, id, model, prefix, update_link){
    $.ajax({
        url: "http://127.0.0.1:8000/get_row",
        dataType : "json",
        data: {"id": id, "model": model},
        success: function (data, textStatus) {
            $.each( data, function( key, val ) {
                if ($("#"+prefix+key)[0]){
                    $("#"+prefix+key)[0].value = val;
                    if (key=="eng_name" && update_link){
                        if (model=="Country"){
                            actual_country = val
                        } else if (model=="City"){
                            actual_city = val
                        };
                    };
                }
                if (key=="city_id"){
                    get_row(args, val, "City", "city_", true)
                } else if (key=="country_id") {
                    get_row(args, val, "Country", "country_", true)
                };
            });
            if ($("#"+prefix+"btn")[0]){
                $("#"+prefix+"btn").removeAttr("disabled")
            }
        }
    });
};

function select_country(args){
    var country_id = $("#country_iso_code").val();
    actual_country=$("#country_eng_name").val()
    upload_link(link_city);
    $("#myLabel")[0].innerHTML = actual_link;


    $("#city_tab_select").attr("class", "");
    $('#myTab a[href="#city-tab"]').tab("show");
    $("#airport_tab_select").attr("class", "hide");

    var data_grid = {"model": "City", "filter": '{"country":"ID"}'.replace("ID", country_id)};
    create_data_grid(data_grid, "cities", "city", "City")
    $("#cities").jqxGrid('unselectrow')

    bind_click_show_tab('country')
};

function select_city(args){
    var city_id = $("#cities").jqxGrid('getrowid', $("#cities").jqxGrid('getselectedrowindex'));

    actual_city=$("#city_eng_name").val()
    upload_link(link_airport);
    $("#myLabel")[0].innerHTML = actual_link;

    $("#airport_tab_select").attr("class", "");
    $('#myTab a[href="#airport-tab"]').tab("show");

    var data_grid = {"model": "Airport", "filter": '{"city":"ID"}'.replace("ID", city_id)};
    create_data_grid(data_grid, "airports", "airport", "Airport")
    $("#airports").jqxGrid('unselectrow')

    bind_click_show_tab('country')
    bind_click_show_tab('city')
};

function search(args){
    var filter_str = $("#total_filter").val()
    if (filter_str){
        var countries_data_grid = {"model":"Country", "query_filter": filter_str},
            cities_data_grid = {"model": "City", "query_filter": filter_str},
            airports_data_grid = {"model": "Airport", "query_filter": filter_str};
        actual_country='';
        actual_city='';
        actual_airport='';

        upload_link(link_search)
        $("#myLabel")[0].innerHTML = actual_link;

        create_data_grid(countries_data_grid, "countries", "country", "Country")
        create_data_grid(cities_data_grid, "cities", "city", "City")
        create_data_grid(airports_data_grid, "airports", "airport", "Airport")
        $("#city_tab_select").attr("class", "");
        $("#airport_tab_select").attr("class", "");
        $('#myTab a[href="#airport-tab"]').tab("show");

        $("#countries").jqxGrid('unselectrow')
        $("#cities").jqxGrid('unselectrow')
        $("#airports").jqxGrid('unselectrow')
    }
    else{
        $("#city_tab_select").attr("class", "hide");
        $("#airport_tab_select").attr("class", "hide");
        $('#myTab a[href="#country-tab"]').tab("show");

        upload_link(link_country);
        $("#myLabel")[0].innerHTML = actual_link;

        var data_grid = {"model":"Country"};
        create_data_grid(data_grid, "countries", "country", "Country");
        $("#countries").jqxGrid('unselectrow')
        $("#cities").jqxGrid('unselectrow')
        $("#airports").jqxGrid('unselectrow')
    }
}

function bind_click_show_tab(mod){
    $("#link_tab_"+mod).click(function(){
        $('#myTab a[href="#'+mod+'-tab"]').tab("show");
    });
};

function create_data_grid(source_data, name_id, column_name){
    source.data = source_data
    var dataAdapter = new $.jqx.dataAdapter(source, {});
    $("#"+name_id).jqxGrid(
    {
        width: "100%",
        height: 460,
        source: dataAdapter,
        filterable: true,
        keyboardnavigation: false,
        columns: [
          { text: "<b>Select "+column_name+"</b>", datafield: "eng_name"}
        ]
    });

};

function bind_row_select(name_grid, model, prefix){
    $("#"+name_grid).bind("rowselect", function (event)
    {
        var id = event.args.row.id;
        get_row(args, id, model, prefix)
    });
};

function upload_link(link){
    actual_link = link.replace("COUNTRY", actual_country).replace("CITY", actual_city).replace("AIRPORT", actual_airport)
}