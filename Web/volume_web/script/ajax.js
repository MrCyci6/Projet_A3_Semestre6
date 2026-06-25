'use strict';

const ajaxRequest = (type, url, callback, data = null) => {
    const xhr = new XMLHttpRequest();
    xhr.open(type, url);    
    xhr.onload = () => {
        switch(xhr.status) {
            case 200:
            case 201:
                callback(JSON.parse(xhr.responseText));
                break;
            default:
                httpErrors(xhr.status);
        }
    };
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(data);
}