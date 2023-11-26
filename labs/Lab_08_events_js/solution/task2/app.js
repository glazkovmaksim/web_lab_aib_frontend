function updateColor() {
  var red = document.getElementById("red").value || 0;
  var green = document.getElementById("green").value || 0;
  var blue = document.getElementById("blue").value || 0;

  red = validateInput(red);
  green = validateInput(green);
  blue = validateInput(blue);

  var colorDisplay = document.getElementById("color-display");
  colorDisplay.style.backgroundColor = "rgb(" + red + "," + green + "," + blue + ")";
}

function validateInput(value) {
  if (isNaN(value)) {
      return 0;
  }
  return Math.max(0, Math.min(value, 255));
}