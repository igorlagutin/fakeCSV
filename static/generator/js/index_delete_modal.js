var deleteModal = document.getElementById('deleteModal')
deleteModal.addEventListener('show.bs.modal', function (event) {
  var button = event.relatedTarget
  var schema_id = button.getAttribute('data-bs-id')
  var target_url = button.getAttribute('data-bs-url')
  var modalTitle = deleteModal.querySelector('.modal-title')
  var modalBodyForm = deleteModal.querySelector('.del_form')
  modalTitle.textContent = 'Are you really want to delete schema #' + schema_id
  modalBodyForm.action = target_url
})