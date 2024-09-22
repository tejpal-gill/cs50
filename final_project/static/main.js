// Function to make password visible or hidden

function passView() {
    var x = document.getElementById("InputPass");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

