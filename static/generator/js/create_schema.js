'use strict';


let total_forms = 1;
let id_schema_row_form_TOTAL_FORMS = document.getElementById("id_schema_row_form-TOTAL_FORMS");
let schema_row_forms_div = document.getElementById("schema_row_forms");
let data_type = document.getElementById("id_schema_row_form-0-data_type");
let copy_data_type =  data_type.cloneNode(true);
let add_column = document.getElementById("add_column");
let has_range_data_type_list = ["4","5"];
let delete_btn_list = document.getElementsByClassName('delete_btn');
let select_list = document.getElementsByClassName('data_type_select');



function rebuild_ids_and_names(){
    // rebuild ids and names to make them from 0 to total_form -1
    //this needed for proper work of formset that handle multiform in django
    var schema_row_from_list = document.getElementsByClassName('schema_row_from');
    var len = schema_row_from_list.length;
    var iteration_num = 0;
    [...schema_row_from_list].forEach(function(schema_row_from, iteration_num){
       var inputs = [...schema_row_from.getElementsByClassName('wrap_input')];
       inputs.forEach(function(input_wrap){
            var input = input_wrap.firstElementChild;
            input.id = input.id.replace(/[0-9]/g, iteration_num);
            input.name = input.name.replace(/[0-9]/g, iteration_num);
       })

       iteration_num = iteration_num +1;
    })
}

function handle_data_type_change(event){
    if (has_range_data_type_list.includes(event.target.value)){
        event.target.parentElement.nextElementSibling.classList.remove("hidden");
        event.target.parentElement.nextElementSibling.nextElementSibling.classList.remove("hidden");
    }
    else{
        event.target.parentElement.nextElementSibling.firstElementChild.value = null;
        event.target.parentElement.nextElementSibling.classList.add("hidden");
        event.target.parentElement.nextElementSibling.nextElementSibling.firstElementChild.value = null;
        event.target.parentElement.nextElementSibling.nextElementSibling.classList.add("hidden");
    }
}

function delete_row_on_click(event){
    event.preventDefault();
    let btn = event.target;
    let parentDiv = btn.parentElement.parentElement;
    parentDiv.remove();
    total_forms = total_forms - 1;
    id_schema_row_form_TOTAL_FORMS.value = total_forms;
    rebuild_ids_and_names()
}

function add_row_inputs(event){
    var input_div = document.createElement("div");
    input_div.classList.add("row", "g-3", "schema_row_from", "mt-1")

    var wrap_div =  document.createElement("div");
    wrap_div.classList.add("wrap_input")

    // name input
    let new_name = document.createElement("input");
        new_name.type = "text";
        new_name.name = "schema_row_form-${total_forms}-name".replace("${total_forms}", total_forms);
        new_name.id = "id_schema_row_form-${total_forms}-name".replace("${total_forms}", total_forms);
        new_name.maxlength = "100";
        new_name.classList.add("form-control");
        new_name.required = true;

    let new_name_wrap_div = wrap_div.cloneNode(true);
        new_name_wrap_div.innerText = "Column name"
        new_name_wrap_div.classList.add("col-lg-3");
        new_name_wrap_div.appendChild(new_name);

    input_div.appendChild(new_name_wrap_div);


    // data type input is copied to new node every time to hav always actual options
    let new_data_type =  copy_data_type.cloneNode(true);
        new_data_type.id = "id_schema_row_form-${total_forms}-data_type".replace("${total_forms}", total_forms);
        new_data_type.name = "schema_row_form-${total_forms}-data_type".replace("${total_forms}", total_forms);
        new_data_type.addEventListener('change', handle_data_type_change, false);

    let new_data_type_wrap_div = wrap_div.cloneNode(true);
        new_data_type_wrap_div.classList.add("col-lg-2")
        new_data_type_wrap_div.innerText = "Type"
        new_data_type_wrap_div.appendChild(new_data_type);

    input_div.appendChild(new_data_type_wrap_div);

    // range start input, hidden by default
    let new_range_start = document.createElement("input");
        new_range_start.type = "number"
        new_range_start.name = "schema_row_form-${total_forms}-range_start".replace("${total_forms}", total_forms);
        new_range_start.id = "id_schema_row_form-${total_forms}-range_start".replace("${total_forms}", total_forms);
        new_range_start.classList.add("form-control", "col-lg-1")

    let new_range_start_wrap_div = wrap_div.cloneNode(true);
        new_range_start_wrap_div.classList.add("col-lg-1", "hidden")
        new_range_start_wrap_div.innerText = "From"
        new_range_start_wrap_div.appendChild(new_range_start);

    input_div.appendChild(new_range_start_wrap_div);


    // range end input, hidden by default
    let new_range_end = document.createElement("input");
        new_range_end.type = "number"
        new_range_end.name = "schema_row_form-${total_forms}-range_end".replace("${total_forms}", total_forms);
        new_range_end.id = "id_schema_row_form-${total_forms}-range_end".replace("${total_forms}", total_forms);
        new_range_end.classList.add("form-control")

    let new_range_end_wrap_div = wrap_div.cloneNode(true);
        new_range_end_wrap_div.classList.add("col-lg-1", "hidden")
        new_range_end_wrap_div.innerText = "To"
        new_range_end_wrap_div.appendChild(new_range_end);

    input_div.appendChild(new_range_end_wrap_div);


    // order input
    let new_order = document.createElement("input");
        new_order.type = "number"
        new_order.name = "schema_row_form-${total_forms}-order".replace("${total_forms}", total_forms);
        new_order.id = "id_schema_row_form-${total_forms}-order".replace("${total_forms}", total_forms);
        new_order.value = total_forms;
        new_order.classList.add("form-control")

    let new_order_wrap_div = wrap_div.cloneNode(true);
        new_order_wrap_div.classList.add("col-lg-2")
        new_order_wrap_div.innerText = "Order"
        new_order_wrap_div.appendChild(new_order);

    input_div.appendChild(new_order_wrap_div);

    total_forms = total_forms + 1

    // del btn
    let new_del_button = document.createElement("button");
        new_del_button.innerText = "Delete"
        new_del_button.classList.add("btn", "btn-link", "delete_btn")

    let new_del_button_wrap_div = wrap_div.cloneNode(true);
        new_del_button_wrap_div.appendChild(new_del_button);
        new_del_button_wrap_div.classList.add("col-lg-2", "position-relative")

    input_div.appendChild(new_del_button_wrap_div);
    new_del_button_wrap_div.addEventListener('click', delete_row_on_click, false);

    // change total_forms value in management form
    id_schema_row_form_TOTAL_FORMS.value = total_forms

   // append row to DOM
    schema_row_forms_div.appendChild(input_div);

    new_name.focus()
}


document.getElementById("id_schema_form-name").focus();

add_column.addEventListener('click', add_row_inputs, false);

// add click event on all existing Delete buttons
[...delete_btn_list].forEach(function(element) {
	element.addEventListener('click', function(del_btn) {
		delete_row_on_click(del_btn)
	});
});

// add click event on all existing data type selcts
[...select_list].forEach(function(element) {
	element.addEventListener('change', function(event) {
            handle_data_type_change(event)
	});
});

