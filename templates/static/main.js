function toggleTheme() {
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    }
    else {
        document.documentElement.classList.remove('dark');
    }
    var sun = document.getElementById('sun');
    var moon = document.getElementById('moon');
    if (localStorage.getItem('color-theme') === 'dark') {
        sun.classList.remove('hidden');
        moon.classList.add('hidden');
    }
    else {
        sun.classList.add('hidden');
        moon.classList.remove('hidden');
    }
}
function AddMetaImage() {
    var url = window.location.href;
    var xhr = new XMLHttpRequest();
    var data = JSON.stringify({ url: url });
    xhr.open('POST', '/api/v1/screenshot', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var tag = document.querySelector('meta[property="og:image"]');
                var twitterTag = document.querySelector('meta[pproperty="twitter:image:src"]');
                if (tag) {
                    tag.setAttribute('content', response.url);
                    twitterTag.setAttribute('content', response.url);
                    return;
                }
                else {
                    var meta = document.createElement('meta');
                    var twitterMeta = document.createElement('meta');
                    twitterMeta.setAttribute('name', 'twitter:image:src');
                    twitterMeta.setAttribute('content', response.url);
                    meta.setAttribute('property', 'og:image');
                    meta.setAttribute('content', response.url);
                    document.getElementsByTagName('head')[0].appendChild(meta);
                    document.getElementsByTagName('head')[0].appendChild(twitterMeta);
                }
            }
        }
    };
}
window.addEventListener("load", function () {
    AddMetaImage();
    toggleTheme();
    toggleMarkdownTheme();
});
function toggleMarkdownTheme() {
    var articles = document.querySelectorAll('article');
    var theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    if (theme === 'dark') {
        articles.forEach(function (article) {
            article.classList.remove('markdown-body-light');
            article.classList.add('markdown-body-dark');
        });
    }
    else {
        articles.forEach(function (article) {
            article.classList.remove('markdown-body-dark');
            article.classList.add('markdown-body-light');
        });
    }
}
function toggleThemeMode() {
    var toggler = document.getElementById('theme-toggle');
    var sun = document.getElementById('sun');
    var moon = document.getElementById('moon');
    if (localStorage.getItem('color-theme') === 'dark') {
        localStorage.setItem('color-theme', 'light');
        document.documentElement.classList.remove('dark');
        if (!toggler.checked) {
            sun.classList.remove('hidden', 'left-1');
            moon.classList.add('hidden');
            sun.classList.add('right-1');
        }
        else {
            sun.classList.remove('hidden', 'right-1');
            moon.classList.add('hidden');
            sun.classList.add('left-1');
        }
    }
    else {
        localStorage.setItem('color-theme', 'dark');
        document.documentElement.classList.add('dark');
        if (!toggler.checked) {
            sun.classList.add('hidden');
            moon.classList.remove('hidden', 'left-1');
            moon.classList.add('right-1');
        }
        else {
            sun.classList.add('hidden');
            moon.classList.remove('hidden', 'right-1');
            moon.classList.add('left-1');
        }
    }
    toggleMarkdownTheme();
}
function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function submitForm() {
    var email = document.getElementById('email');
    var subject = document.getElementById('subject');
    var message = document.getElementById('message');
    var submit = document.getElementById('submit');
    submit.disabled = true;
    submit.classList.add('cursor-not-allowed');
    submit.children[0].classList.add('hidden');
    submit.children[1].classList.remove('hidden');
    var emailError = document.getElementById('alert-1');
    var subjectError = document.getElementById('alert-2');
    var messageError = document.getElementById('alert-3');
    var popup = document.getElementById('popup-modal');
    var popup_error = document.getElementById('popup-modal-error');
    if (email.value === '' || !validateEmail(email.value)) {
        emailError.classList.remove('hidden');
    }
    if (subject.value === '') {
        subjectError.classList.remove('hidden');
    }
    if (message.value === '') {
        messageError.classList.remove('hidden');
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/feedback', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var data = JSON.stringify({ message: message.value, email: email.value, subject: subject.value });
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                popup.classList.remove('hidden');
            }
            else {
                popup_error.classList.remove('hidden');
            }
            email.value = "";
            message.value = "";
            subject.value = "";
            submit.children[0].classList.remove('hidden');
            submit.children[1].classList.add('hidden');
            submit.disabled = false;
        }
    };
}
function closePopup() {
    var popup = document.getElementById('popup-modal');
    popup.classList.add('hidden');
}
function closePopupError() {
    var popup = document.getElementById('popup-modal-error');
    popup.classList.add('hidden');
}
function getImagefromTitle(id) {
    var title = document.getElementById("title_" + id);
    var image = document.getElementById("image_" + id);
    var xhr = new XMLHttpRequest();
    var data = JSON.stringify({ query: title.innerText });
    xhr.open('POST', '/api/v1/image', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                image.style.backgroundImage = "url(" + response.url + ")";
                image.classList.remove("animate-pulse");
            }
        }
    };
}
