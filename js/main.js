(function() {
    NodeList.prototype.forEach = Array.prototype.forEach;
    NodeList.prototype.reduce = Array.prototype.reduce;

    document.addEventListener('DOMContentLoaded', function() {
        var selects = document.form.querySelectorAll('.button-select');

        selects.forEach(function(button) {
            var input = button.querySelector('input[type=file]');

            button.onclick = function() {
                input.click();
            };

            input.onchange = function(event) {
                var file = input.files[0];
                if (file.type.match('image.*')) {
                    button.querySelector('span').innerHTML = file.name;
                    button.classList.add('button-active');
                } else {
                    return event.preventDefault();
                }
            }
        });

        var submit = document.form.querySelector('.button-submit');
        submit.onclick = function() {
            var picture = document.form.querySelector('[name="picture"]').files[0]
            var flag = document.form.querySelector('[name="flag"]').files[0];

            if (!picture || !flag || !picture.type.match('image.*') || !flag.type.match('image/.*')) {
                console.log('Wrong stuff');
                return;
            }

            var data = new FormData();
            data.append('picture', picture, picture.name);
            data.append('flag', flag, flag.name);

            var xhr = new XMLHttpRequest();
            xhr.withCredentials = true;
            xhr.open(document.form.method, document.form.action, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var result = document.querySelector('.result');
                    var cloned = result.cloneNode(false);
                    result.parentNode.replaceChild(cloned, result);

                    var data = JSON.parse(xhr.response);
                    var img = document.createElement('img');
                    img.src = data.url;

                    cloned.appendChild(img);
                }
            };
            xhr.send(data);

            return;
        };
    });
})();
