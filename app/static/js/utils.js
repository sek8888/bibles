const formEncodedBody = obj => Object.keys(obj)
    .filter(k => obj.hasOwnProperty(k))
    .map(k =>
        encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])
    ).join('&');

async function postData(url = '', data = {}) {
    const request = {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: formEncodedBody(data)
    }
    const response = await fetch(url, request);
    return await response.json()
}

async function getData(url = '') {
    const request = {
        credentials: 'same-origin',
    }
    const response = await fetch(url, request);
    return await response.json()
}

let showStatusMessage = (obj) => {
    if ( obj.status == "0" )
        showMessage(obj.message, "lime")
    else
        showMessage(obj.message, "red")
}

let showMessage = (text, color = null) => {
    const msgs = $id('msgs')
    const msg = $create("div")
    msg.setAttribute("id", Date.now())
    msg.style.backgroundColor = color
    msg.textContent = text
    msgs.appendChild(msg)

    setTimeout(() => msgs.removeChild(msg), 5000)
}


let setLoader = () => {
    const ldr = $create("div")
    ldr.setAttribute("id", "loader")
    ldr.classList.add("loader", "loader-default", "is-active")

    document.body.appendChild(ldr)
}
let rmLoader = () => { 
    const ldr = $id('loader')
    ldr && ldr.remove()
}

let showModal = (node = null) => {
    const cont = $create("div")
    const content = $create("div")
    const close = $create("div")
    const nodeCont = $create("div")

    nodeCont.setAttribute("id", "modal-content")
    cont.setAttribute("id", "modal")
    cont.classList.add("modal")
    content.classList.add("modal-content")
    close.classList.add("close")
    close.appendChild($createTxt("×"))
    close.onclick = closeModal

    node && nodeCont.appendChild(node)
    content.appendChild(close)
    content.appendChild(nodeCont)
    cont.appendChild(content)
    cont.style.display = "block";

    document.body.appendChild(cont)
}

let closeModal = () => {
    const mdl = $id('modal')
    mdl && mdl.remove()
}

let toggleColor = () => {
    if (document.body.style.backgroundColor == "black") {
        document.body.style.color = "black"
        document.body.style.backgroundColor = "white";
    }
    else {
        document.body.style.backgroundColor = "black";
        document.body.style.color = "white"
    }
}

let $id = (itemId) => document.querySelector(`#${itemId}`)
let $create = (type) => document.createElement(type)
let $createTxt = (text) => document.createTextNode(text)
