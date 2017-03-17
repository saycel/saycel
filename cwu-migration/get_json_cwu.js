var fs = require('fs');
var csv = require("fast-csv");
var json = []

csv.fromPath("cwurates.csv").on("data", function(data){
     var ext = data[0].split(';')[0]
     var new_cost = parseFloat(data[0].split(';')[2]) + .05
     var rounded = Math.round(100*new_cost)/100
     json.push({
         "ext": ext,
         "cost":rounded
     })
      
 }).on("end", function(){
    require('fs').writeFile(
        './cwu.json',
        JSON.stringify(json),
        function (err) {
            if (err) {
                console.error('Crap happens');
            }
        }
    );
 });
