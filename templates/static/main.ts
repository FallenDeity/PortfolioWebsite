function toggleTheme() {
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark')
    }
    const sun = document.getElementById('sun');
    const moon = document.getElementById('moon');
    if (localStorage.getItem('color-theme') === 'dark') {
        sun.classList.remove('hidden');
        moon.classList.add('hidden');
    } else {
        sun.classList.add('hidden');
        moon.classList.remove('hidden');
    }
}


function AddMetaImage() {
    let url = window.location.href;
    let xhr = new XMLHttpRequest();
    let data = JSON.stringify({url: url});
    xhr.open('POST', '/api/v1/screenshot', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                let meta = document.querySelector('meta[property="og:image"]');
                if (meta) {
                    meta.setAttribute('content', response.url);
                }
            }
        }
    }
}


window.addEventListener("load", () => {
    toggleMarkdownTheme();
});


function toggleMarkdownTheme() {
    const articles = document.querySelectorAll('article');
    const theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    if (theme === 'dark') {
        articles.forEach(article => {
            article.classList.remove('markdown-body-light');
            article.classList.add('markdown-body-dark');
        });
    } else {
        articles.forEach(article => {
            article.classList.remove('markdown-body-dark');
            article.classList.add('markdown-body-light');
        });
    }
}


function toggleThemeMode() {
    const toggler = document.getElementById('theme-toggle') as HTMLInputElement;
    const sun = document.getElementById('sun');
    const moon = document.getElementById('moon');
    if (localStorage.getItem('color-theme') === 'dark') {
        localStorage.setItem('color-theme', 'light');
        document.documentElement.classList.remove('dark');
        if (!toggler.checked) {
            sun.classList.remove('hidden', 'left-1');
            moon.classList.add('hidden');
            sun.classList.add('right-1');
        } else {
            sun.classList.remove('hidden', 'right-1');
            moon.classList.add('hidden');
            sun.classList.add('left-1');
        }
    } else {
        localStorage.setItem('color-theme', 'dark');
        document.documentElement.classList.add('dark');
        if (!toggler.checked) {
            sun.classList.add('hidden');
            moon.classList.remove('hidden', 'left-1');
            moon.classList.add('right-1');
        } else {
            sun.classList.add('hidden');
            moon.classList.remove('hidden', 'right-1');
            moon.classList.add('left-1');
        }
    }
    toggleMarkdownTheme();
}


function validateEmail(email: string) {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
}


function submitForm() {
    const email = document.getElementById('email') as HTMLInputElement;
    const subject = document.getElementById('subject') as HTMLInputElement;
    const message = document.getElementById('message') as HTMLTextAreaElement;
    const submit = document.getElementById('submit') as HTMLInputElement;
    submit.disabled = true;
    submit.classList.add('cursor-not-allowed');
    submit.children[0].classList.add('hidden');
    submit.children[1].classList.remove('hidden');
    const emailError = document.getElementById('alert-1');
    const subjectError = document.getElementById('alert-2');
    const messageError = document.getElementById('alert-3');
    const popup = document.getElementById('popup-modal');
    const popup_error = document.getElementById('popup-modal-error');
    if (email.value === '' || !validateEmail(email.value)) {
        emailError.classList.remove('hidden');
    }
    if (subject.value === '') {
        subjectError.classList.remove('hidden');
    }
    if (message.value === '') {
        messageError.classList.remove('hidden');
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/feedback', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    let data = JSON.stringify({message: message.value, email: email.value, subject: subject.value});
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                popup.classList.remove('hidden');

            } else {
                popup_error.classList.remove('hidden');
            }
            email.value = "";
            message.value = "";
            subject.value = "";
            submit.children[0].classList.remove('hidden');
            submit.children[1].classList.add('hidden');
            submit.disabled = false;
        }
    }
}


function closePopup() {
    const popup = document.getElementById('popup-modal');
    popup.classList.add('hidden');
}


function closePopupError() {
    const popup = document.getElementById('popup-modal-error');
    popup.classList.add('hidden');
}


function getImagefromTitle (id: string) {
    let title = document.getElementById("title_" + id);
    let image = document.getElementById("image_" + id) as HTMLDivElement;
    let xhr = new XMLHttpRequest();
    let data = JSON.stringify({query: title.innerText});
    xhr.open('POST', '/api/v1/image', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                image.style.backgroundImage = "url(" + response.url + ")";
                image.classList.remove("animate-pulse");
            }
        }
    }
}
