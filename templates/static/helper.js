window.onscroll = function () {
    sticky()
};


window.addEventListener("resize", function () {
    if (window.outerWidth > 1000) {
        document.getElementById("menu").style.display = "none";
        document.getElementById("mobile-menu").style.display = "none";
    } else {
        document.getElementById("menu").style.display = "block";
        document.getElementById("menu").style.float = "right";
    }
});

function sticky() {
    let navbar = document.getElementById("Navbar");
    if (navbar === null) {
        return;
    }
    let offset = navbar.offsetTop || 0;
    if (window.scrollY >= offset) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function get_ip() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "https://api.ipify.org?format=json", false);
    xhr.send();
    return JSON.parse(xhr.responseText).ip;
}

function addFeedback() {
    let feedback = document.getElementById("feedback").value;
    let xhr = new XMLHttpRequest();
    let ip = get_ip();
    xhr.open("POST", "/api/v1/feedback", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ip: ip, feedback: feedback}));
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            alert(xhr.responseText);
        }
    }
}


function topNav() {
    const topNav = document.getElementById("mobile-menu");
    topNav.style.display = topNav.style.display === "flex" ? "none" : "flex";
}