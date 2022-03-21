//add hidden input delete for model_formset delete
function delete_row_on_click(event){
    event.preventDefault();
    let btn = event.target;
    let parentDiv = btn.parentElement.parentElement;
    parentDiv.style.display = "none";
    let del_input = document.createElement("input");
    del_input.type = "hidden"
    del_input.name = parentDiv.firstElementChild.id.slice(3,-3) + "-DELETE";
    del_input.value = "on";
    parentDiv.appendChild(del_input);
}