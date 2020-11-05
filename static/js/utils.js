function togglePasswordVisibility(labelSelector, targetPasswordSelector) {
  const passwordInput = document.querySelector(targetPasswordSelector);
  const labelShowPassword = document.querySelector(labelSelector);

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    labelShowPassword.innerText = "Hide";
  } else {
    passwordInput.type = "password";
    labelShowPassword.innerText = "Show";
  }
}

function addShowPassword(targetPasswordSelector) {
  const selectorName = `${targetPasswordSelector}`
    .replace("#", "")
    .replace(".", "");
  const labelId = `label-${selectorName}`;

  const div = document.createElement("div");
  div.classList.add("show-password");

  const input = document.createElement("input");
  input.setAttribute("type", "checkbox");
  input.setAttribute("name", `name-${selectorName}`);
  input.setAttribute("id", `id-${selectorName}`);
  input.setAttribute(
    "onclick",
    `togglePasswordVisibility("#${labelId}", "${targetPasswordSelector}")`
  );
  input.classList.add("hide");

  const label = document.createElement("label");
  label.setAttribute("id", labelId);
  label.setAttribute("for", `id-${selectorName}`);
  label.classList.add("show-password");
  label.classList.add("cursor-pointer");
  label.classList.add("ml-1");
  label.innerText = "Show";

  div.appendChild(input);
  div.appendChild(label);

  const passwordInput = document.querySelector(targetPasswordSelector);
  passwordInput.parentNode.appendChild(div);
}

function isFormHtml5Valid(form, formSelectorStrings) {
  for (var el of form.querySelectorAll(formSelectorStrings)) {
    if (!el.checkValidity()) return false;
  }
  return true;
}
