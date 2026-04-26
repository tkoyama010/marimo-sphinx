/**
 * marimo-sphinx: button and iframe control
 */

window.marimoShowIframe = function (buttonId, iframeSrc) {
  var button = document.getElementById(buttonId);
  if (!button) return;
  var container = button.closest(".marimo-sphinx-container");
  var iframe = container.querySelector(".marimo-sphinx-iframe");

  button.parentElement.classList.add("hidden");
  iframe.src = iframeSrc; // lazy-load: set src only on click
  iframe.classList.remove("hidden");
};
