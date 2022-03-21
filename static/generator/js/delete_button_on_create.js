function delete_row_on_click(event){
    event.preventDefault();
    let btn = event.target;
    let parentDiv = btn.parentElement.parentElement;
    parentDiv.remove();
    total_forms = total_forms - 1;
    id_schema_row_form_TOTAL_FORMS.value = total_forms;
    rebuild_ids_and_names()
}