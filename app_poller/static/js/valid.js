
// if (input1 == input2) {
//     document.getElementById("login-button").removeAttribute("disabled");
// }

do {
    let input1 = document.getElementById("InputPassword1").value;
    let input2 = document.getElementById("InputPassword2").value;
    const button = document.getElementById("login-button");
    button.disabled = true;
  } while (input1 != input2);
