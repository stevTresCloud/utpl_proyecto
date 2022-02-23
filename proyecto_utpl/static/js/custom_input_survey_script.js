odoo.define('proyecto_utpl.custom_js', function (require) {
"use strict";
document.addEventListener("DOMContentLoaded", function(event) {
    jQuery("video#arjs-video").detach().appendTo('#camera_div');
});
});