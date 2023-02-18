let prevScrollpos = window.scrollY;


function responsive() {
    if (window.outerWidth > 1000) {
        document.getElementById("menu").style.display = "none";
        document.getElementById("mobile-menu").style.display = "none";
    } else {
        document.getElementById("menu").style.display = "block";
        document.getElementById("menu").style.float = "right";
    }
}


window.addEventListener("resize", function () {
    responsive();
});


window.addEventListener("scroll", function () {
    sticky();
});


function sticky() {
    let navbar = document.getElementById("Navbar");
    if (navbar === null) {
        return;
    }
    const currentScrollPos = window.scrollY;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("Navbar").style.top = "0";
    } else {
        document.getElementById("Navbar").style.top = "-80px";
    }
    prevScrollpos = currentScrollPos;
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
            let response = JSON.parse(xhr.responseText);
            alert(response.message);
        }
    }
}


function topNav() {
    const topNav = document.getElementById("mobile-menu");
    topNav.style.display = topNav.style.display === "flex" ? "none" : "flex";
    const menuBtn = document.getElementById("menu-btn");
    menuBtn.className = menuBtn.className === "fa-solid fa-bars" ? "fa-solid fa-xmark" : "fa-solid fa-bars";
}

document.addEventListener('DOMContentLoaded', function () {
    particleground(document.getElementById('particles'), {
        dotColor: '#fff293',
        lineColor: '#fff293'
    });
    const intro = document.getElementById('intro');
    intro.style.marginTop = -intro.offsetHeight / 2 + 'px';
}, false);


;(function (window, document) {
    "use strict";
    const pluginName = 'particleground';

    function extend(out) {
        out = out || {};
        for (let i = 1; i < arguments.length; i++) {
            const obj = arguments[i];
            if (!obj) continue;
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    if (typeof obj[key] === 'object')
                        deepExtend(out[key], obj[key]);
                    else
                        out[key] = obj[key];
                }
            }
        }
        return out;
    }

    const $ = window.jQuery;

    function Plugin(element, options) {
        const canvasSupport = !!document.createElement('canvas').getContext;
        let canvas;
        let ctx;
        const particles = [];
        let raf;
        let mouseX = 0;
        let mouseY = 0;
        let winW;
        let winH;
        const desktop = !navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry|BB10|mobi|tablet|opera mini|nexus 7)/i);
        const orientationSupport = !!window.DeviceOrientationEvent;
        let tiltX = 0;
        let pointerX;
        let pointerY;
        let tiltY = 0;
        let paused = false;

        options = extend({}, window[pluginName].defaults, options);

        function init() {
            if (!canvasSupport) {
                return;
            }

            //Create canvas
            canvas = document.createElement('canvas');
            canvas.className = 'pg-canvas';
            canvas.style.display = 'block';
            element.insertBefore(canvas, element.firstChild);
            ctx = canvas.getContext('2d');
            styleCanvas();

            // Create particles
            const numParticles = Math.round((canvas.width * canvas.height) / options.density);
            for (let i = 0; i < numParticles; i++) {
                const p = new Particle();
                p.setStackPos(i);
                particles.push(p);
            }


            window.addEventListener('resize', function () {
                resizeHandler();
            }, false);

            document.addEventListener('mousemove', function (e) {
                mouseX = e.pageX;
                mouseY = e.pageY;
            }, false);

            if (orientationSupport && !desktop) {
                window.addEventListener('deviceorientation', function () {
                    // Contrain tilt range to [-30,30]
                    tiltY = Math.min(Math.max(-event.beta, -30), 30);
                    tiltX = Math.min(Math.max(-event.gamma, -30), 30);
                }, true);
            }

            draw();
            hook('onInit');
        }

        /**
         * Style the canvas
         */
        function styleCanvas() {
            canvas.width = element.offsetWidth;
            canvas.height = element.offsetHeight;
            ctx.fillStyle = options.dotColor;
            ctx.strokeStyle = options.lineColor;
            ctx.lineWidth = options.lineWidth;
        }

        /**
         * Draw particles
         */
        function draw() {
            let i;
            if (!canvasSupport) {
                return;
            }

            winW = window.innerWidth;
            winH = window.innerHeight;

            // Wipe canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Update particle positions
            for (i = 0; i < particles.length; i++) {
                particles[i].updatePosition();
            }

            // Draw particles
            for (i = 0; i < particles.length; i++) {
                particles[i].draw();
            }


            // Call this function next time screen is redrawn
            if (!paused) {
                raf = requestAnimationFrame(draw);
            }
        }

        /**
         * Add/remove particles.
         */
        function resizeHandler() {
            let i;
// Resize the canvas
            styleCanvas();

            const elWidth = element.offsetWidth;
            const elHeight = element.offsetHeight;

            // Remove particles that are outside the canvas
            for (i = particles.length - 1; i >= 0; i--) {
                if (particles[i].position.x > elWidth || particles[i].position.y > elHeight) {
                    particles.splice(i, 1);
                }
            }


            // Adjust particle density
            const numParticles = Math.round((canvas.width * canvas.height) / options.density);
            if (numParticles > particles.length) {
                while (numParticles > particles.length) {
                    const p = new Particle();
                    particles.push(p);
                }
            } else if (numParticles < particles.length) {
                particles.splice(numParticles);
            }

            // Re-index particles
            for (i = particles.length - 1; i >= 0; i--) {
                particles[i].setStackPos(i);
            }

        }

        /**
         * Pause particle system
         */
        function pause() {
            paused = true;
        }

        /**
         * Start particle system
         */
        function start() {
            paused = false;
            draw();
        }

        /**
         * Particle
         */
        function Particle() {
            this.active = true;
            this.layer = Math.ceil(Math.random() * 3);
            this.parallaxOffsetX = 0;
            this.parallaxOffsetY = 0;
            // Initial particle position
            this.position = {
                x: Math.ceil(Math.random() * canvas.width),
                y: Math.ceil(Math.random() * canvas.height)
            }
            // Random particle speed, within min and max values
            this.speed = {}
            switch (options.directionX) {
                case 'left':
                    this.speed.x = +(-options.maxSpeedX + (Math.random() * options.maxSpeedX) - options.minSpeedX).toFixed(2);
                    break;
                case 'right':
                    this.speed.x = +((Math.random() * options.maxSpeedX) + options.minSpeedX).toFixed(2);
                    break;
                default:
                    this.speed.x = +((-options.maxSpeedX / 2) + (Math.random() * options.maxSpeedX)).toFixed(2);
                    this.speed.x += this.speed.x > 0 ? options.minSpeedX : -options.minSpeedX;
                    break;
            }
            switch (options.directionY) {
                case 'up':
                    this.speed.y = +(-options.maxSpeedY + (Math.random() * options.maxSpeedY) - options.minSpeedY).toFixed(2);
                    break;
                case 'down':
                    this.speed.y = +((Math.random() * options.maxSpeedY) + options.minSpeedY).toFixed(2);
                    break;
                default:
                    this.speed.y = +((-options.maxSpeedY / 2) + (Math.random() * options.maxSpeedY)).toFixed(2);
                    this.speed.x += this.speed.y > 0 ? options.minSpeedY : -options.minSpeedY;
                    break;
            }
        }

        /**
         * Draw particle
         */
        Particle.prototype.draw = function () {
            // Draw circle
            ctx.beginPath();
            ctx.arc(this.position.x + this.parallaxOffsetX, this.position.y + this.parallaxOffsetY, options.particleRadius / 2, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.fill();

            // Draw lines
            ctx.beginPath();
            // Iterate over all particles which are higher in the stack than this one
            for (let i = particles.length - 1; i > this.stackPos; i--) {
                const p2 = particles[i];

                // Pythagorus theorum to get distance between two points
                const a = this.position.x - p2.position.x;
                const b = this.position.y - p2.position.y;
                const dist = Math.sqrt((a * a) + (b * b)).toFixed(2);

                // If the two particles are in proximity, join them
                if (dist < options.proximity) {
                    ctx.moveTo(this.position.x + this.parallaxOffsetX, this.position.y + this.parallaxOffsetY);
                    if (options.curvedLines) {
                        ctx.quadraticCurveTo(Math.max(p2.position.x, p2.position.x), Math.min(p2.position.y, p2.position.y), p2.position.x + p2.parallaxOffsetX, p2.position.y + p2.parallaxOffsetY);
                    } else {
                        ctx.lineTo(p2.position.x + p2.parallaxOffsetX, p2.position.y + p2.parallaxOffsetY);
                    }
                }
            }
            ctx.stroke();
            ctx.closePath();
        }

        /**
         * update particle position
         */
        Particle.prototype.updatePosition = function () {
            if (options.parallax) {
                if (orientationSupport && !desktop) {
                    // Map tiltX range [-30,30] to range [0,winW]
                    const ratioX = (winW - 0) / (30 - -30);
                    pointerX = (tiltX - -30) * ratioX;
                    // Map tiltY range [-30,30] to range [0,winH]
                    const ratioY = (winH - 0) / (30 - -30);
                    pointerY = (tiltY - -30) * ratioY;
                } else {
                    pointerX = mouseX;
                    pointerY = mouseY;
                }
                // Calculate parallax offsets
                this.parallaxTargX = (pointerX - (winW / 2)) / (options.parallaxMultiplier * this.layer);
                this.parallaxOffsetX += (this.parallaxTargX - this.parallaxOffsetX) / 10; // Easing equation
                this.parallaxTargY = (pointerY - (winH / 2)) / (options.parallaxMultiplier * this.layer);
                this.parallaxOffsetY += (this.parallaxTargY - this.parallaxOffsetY) / 10; // Easing equation
            }

            const elWidth = element.offsetWidth;
            const elHeight = element.offsetHeight;

            switch (options.directionX) {
                case 'left':
                    if (this.position.x + this.speed.x + this.parallaxOffsetX < 0) {
                        this.position.x = elWidth - this.parallaxOffsetX;
                    }
                    break;
                case 'right':
                    if (this.position.x + this.speed.x + this.parallaxOffsetX > elWidth) {
                        this.position.x = 0 - this.parallaxOffsetX;
                    }
                    break;
                default:
                    // If particle has reached edge of canvas, reverse its direction
                    if (this.position.x + this.speed.x + this.parallaxOffsetX > elWidth || this.position.x + this.speed.x + this.parallaxOffsetX < 0) {
                        this.speed.x = -this.speed.x;
                    }
                    break;
            }

            switch (options.directionY) {
                case 'up':
                    if (this.position.y + this.speed.y + this.parallaxOffsetY < 0) {
                        this.position.y = elHeight - this.parallaxOffsetY;
                    }
                    break;
                case 'down':
                    if (this.position.y + this.speed.y + this.parallaxOffsetY > elHeight) {
                        this.position.y = 0 - this.parallaxOffsetY;
                    }
                    break;
                default:
                    // If particle has reached edge of canvas, reverse its direction
                    if (this.position.y + this.speed.y + this.parallaxOffsetY > elHeight || this.position.y + this.speed.y + this.parallaxOffsetY < 0) {
                        this.speed.y = -this.speed.y;
                    }
                    break;
            }

            // Move particle
            this.position.x += this.speed.x;
            this.position.y += this.speed.y;
        }

        /**
         * Setter: particle stacking position
         */
        Particle.prototype.setStackPos = function (i) {
            this.stackPos = i;
        }

        function option(key, val) {
            if (val) {
                options[key] = val;
            } else {
                return options[key];
            }
        }

        function destroy() {
            console.log('destroy');
            canvas.parentNode.removeChild(canvas);
            hook('onDestroy');
            if ($) {
                $(element).removeData('plugin_' + pluginName);
            }
        }

        function hook(hookName) {
            if (options[hookName] !== undefined) {
                options[hookName].call(element);
            }
        }

        init();

        return {
            option: option,
            destroy: destroy,
            start: start,
            pause: pause
        };
    }

    window[pluginName] = function (elem, options) {
        return new Plugin(elem, options);
    };

    window[pluginName].defaults = {
        minSpeedX: 0.1,
        maxSpeedX: 0.7,
        minSpeedY: 0.1,
        maxSpeedY: 0.7,
        directionX: 'center', // 'center', 'left' or 'right'. 'center' = dots bounce off edges
        directionY: 'center', // 'center', 'up' or 'down'. 'center' = dots bounce off edges
        density: 10000, // How many particles will be generated: one particle every n pixels
        dotColor: '#666666',
        lineColor: '#666666',
        particleRadius: 3, // Dot size
        lineWidth: 1.2,
        curvedLines: false,
        proximity: 80, // How close two dots need to be before they join
        parallax: true,
        parallaxMultiplier: 8, // The lower the number, the more extreme the parallax effect
        onInit: function () {
        },
        onDestroy: function () {
        }
    };

    // nothing wrong with hooking into jQuery if it's there...
    if ($) {
        $.fn[pluginName] = function (options) {
            if (typeof arguments[0] === 'string') {
                let methodName = arguments[0];
                let args = Array.prototype.slice.call(arguments, 1);
                let returnVal;
                this.each(function () {
                    if ($.data(this, 'plugin_' + pluginName) && typeof $.data(this, 'plugin_' + pluginName)[methodName] === 'function') {
                        returnVal = $.data(this, 'plugin_' + pluginName)[methodName].apply(this, args);
                    }
                });
                if (returnVal !== undefined) {
                    return returnVal;
                } else {
                    return this;
                }
            } else if (typeof options === "object" || !options) {
                return this.each(function () {
                    if (!$.data(this, 'plugin_' + pluginName)) {
                        $.data(this, 'plugin_' + pluginName, new Plugin(this, options));
                    }
                });
            }
        };
    }

})(window, document);

(function () {
    let lastTime = 0;
    let vendors = ['ms', 'moz', 'webkit', 'o'];
    for (let x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame']
            || window[vendors[x] + 'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function (callback, element) {
            let currTime = new Date().getTime();
            let timeToCall = Math.max(0, 16 - (currTime - lastTime));
            let id = window.setTimeout(function () {
                    callback(currTime + timeToCall);
                },
                timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function (id) {
            clearTimeout(id);
        };
}());
