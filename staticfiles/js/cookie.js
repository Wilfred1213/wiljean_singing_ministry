document.addEventListener('DOMContentLoaded', function() {
    var cookieConsent = document.getElementById('cookie-consent');

    if (!getCookie('cookie_consent')) {
        cookieConsent.style.display = 'block';
    }

    var acceptButton = document.getElementById('accept-cookies');
    acceptButton.addEventListener('click', function() {
        setCookie('cookie_consent', 'accepted', 365);
        cookieConsent.style.display = 'none';
    });

    var declineButton = document.getElementById('decline-cookies');
    declineButton.addEventListener('click', function() {
        setCookie('cookie_consent', null, -1); // Remove the cookie
        cookieConsent.style.display = 'none';
    });
});

function setCookie(name, value, days) {
    var expires = '';
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

function getCookie(name) {
    var nameEQ = name + '=';
    var cookies = document.cookie.split(';');
    for(var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) == 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }
    return null;
}



