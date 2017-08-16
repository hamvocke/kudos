const options = document.querySelectorAll('.box.option');

const selectOption = (event) => {
  const selectedTarget = document.querySelectorAll(".selected-options")[0];
  selectedTarget.insertBefore(event.target, selectedTarget.firstChild);
  event.target.removeEventListener('click', selectOption);
  event.target.addEventListener('click', removeOption);
}

const removeOption = (event) => {
  const optionsTarget = document.querySelectorAll(".options")[0];
  optionsTarget.insertBefore(event.target, optionsTarget.firstChild);
  event.target.removeEventListener('click', removeOption);
  event.target.addEventListener('click', selectOption);
};

for (option of options) {
  option.addEventListener('click', selectOption);
}
