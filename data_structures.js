
function head_tail(arr){
    return [arr[0], arr.slice(1, arr.length)]
};

debug = false;
function optional_arg(obj, name, default_arg){
    if (debug){
        console.log(JSON.stringify(obj));
        console.log(name);
        console.log(default_arg);
    }
    return (name in obj) ? obj[name] : default_arg
};


function col_names(csv_string, delims){
    // TODO better optional args ??
    // Show how it works //
    rd = '\n';
    head = head_tail(csv_string.split(rd))[0];
    fd = ',';
    if (head.indexOf(fd)==-1) 
        fd = /\s\s*/;
    if (typeof delims == 'object'){
        if ('field_delim' in delims) 
            fd = delims['field_delim'];
        if ('record_delim' in delims) 
            rd = delims['record_delim'];
    };
    return head.split(fd);
};

function ob_array_get(ob_array, name){
    /*  
 *      For each object in ob_array push object[name] onto an
 *      array and
 *          return.
 *              */
    var res = []; 
    for (var i=0; i<ob_array.length; i++){
        res.push(ob_array[i][name]);
    };  
    return (res);
};

function unique_in(arr){
    /*
 *     Return an array of the unique things in arr.
 *         In other words the *set* of things in arr.
 *             unique_in([1,2,3,3,2,4])
 *                 [1,2,3,4])
 *                     */
    var obj = {}; 
    arr.map(function(thing){obj[thing]=true});
    return $.map(obj, function(value, key) {
      return key;
      }); 
};

function zip(arr1, arr2){
    /*
 *     zip two arrays together ala python.
 *         */
    var res = []; 
    for (var i=0; i<arr1.length; i++){
        res.push([arr1[i],arr2[i]]);
    };  
    return (res);
};



function objectify(name, value){
    /*
 *     Given two arrays (name and value), zip them together and
 *     return an
 *         object with those names and values.
 *             objectify(['head', 'tail'], ['front', 'rear'])
 *                 Object {head: "front", tail: "rear"}
 *                     */
    var res = {};
    for (var i=0; i<name.length; i++) {
        res[name[i]] = value[i];}
    return (res);
};



function csv2obarray(csv_string){
    /*
    *  Convert a csv string *with header row* to an array of
    *  objects with names/properties from the header row.
    */
    var csv_array = csv_string.split('\n');
    // get head tail
    var head = csv_array[0];
    var fd = ',';
    if (head.indexOf(fd)==-1) 
        fd = /\s\s*/;
 
    var names = head.split(fd);
    var table = [];
    for (var i=1; i<csv_array.length; i++){
        var row = csv_array[i].split(fd);
        table.push(objectify(names, row));
    };
    return(table);
};



function ob2csv(obj, names){
    /*
 *     Transform an object into a csv_string, ordered by names.
 *         names: properties of obj.
 *             ob2csv({head: "front", tail: "rear"}, ['tail',
 *             'head'])
 *                 "rear,front"
 *                     */
    var cs = '';
    var a = [];
    for (var i=0; i<names.length; i++){
        var msg = names[i] + ':' +  obj[names[i]]
        a.push(obj[names[i]]);
//        console.log(msg);
    }
    return a.join(',')
};




function ob_array2csv(ob_array, names){
    /*
    Transform an array of objects into a csv string.
    names: properties of the objects in ob_array.
    The resulting csv_string is ordered by names.
    obs2csv([{head: "front", tail: "rear"}, 
            {head: "cabeza", tail: "nalgas"}], ['tail', 'head'])
    "rear,front"
    "nalgas,cabeza"
    */
    var res = [];
    for (var i=0; i<ob_array.length; i++){
        res.push( ob2csv(ob_array[i], names))
    }
    return res.join('\n')
};



