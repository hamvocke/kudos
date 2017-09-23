const optionsTarget = document.querySelectorAll(".options")[0];
const selectedTarget = document.querySelectorAll(".selected-options")[0];
const selectElement = document.querySelectorAll(".option-select")[0];

const toggle = (text) => {
  const options = Array.from(selectElement.getElementsByTagName('option'));
  options
    .filter((option) => option.innerHTML === text)
    .map((option) => option.selected = !option.selected)
}

const selectOption = (event) => {
  selectedTarget.insertBefore(event.target, selectedTarget.firstChild);
  event.target.removeEventListener('click', selectOption);
  event.target.addEventListener('click', removeOption);

  toggle(event.target.innerHTML);
};

const removeOption = (event) => {
  optionsTarget.insertBefore(event.target, optionsTarget.firstChild);
  event.target.removeEventListener('click', removeOption);
  event.target.addEventListener('click', selectOption);

  toggle(event.target.innerHTML);
};

export default function init() {
  const options = document.querySelectorAll('.box.option');
  for (option of options) {
    option.addEventListener('click', selectOption);
  };
}
