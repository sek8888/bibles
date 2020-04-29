let formSubmit = (event) => {
    const form = event.target
    const inputs = form.getElementsByTagName("input")
    const textarea = form.getElementsByTagName("textarea")
    const url = form.getAttribute("url")
    const type = form.querySelector("#type_id").value

    let data = {}
    for(i = 0; i < inputs.length; i++) {
        data[inputs[i].name] = inputs[i].value
    }
    for(i = 0; i < textarea.length; i++) {
        data[textarea[i].name] = textarea[i].value
    }

    // TODO: validate data
    postData(url, data).then(msg => {
        showStatusMessage(msg)
        closeModal()
        reload(type)
    })
    event.preventDefault()
}

let deleteForm = (type, id) => {
    if (window.confirm("Are you sure you want to delete?")) {
        postData(`/data/${type}/${id}/delete`).then(msg => {
            showStatusMessage(msg)
            reload('bibles')
        })
    }
}

let getForm = (contId, formId, type, itemId, data) => {
    cont = $id(contId)
    getData(`data/${type}/form`).then(form => {

    })
}

let getCreateForm = (type, itemId, data = {}) => {
    getData(`data/${type}/form`).then(form => {
        showModal()
        const cont = $id('modal-content')
        cont.innerHTML = ''
        cont.appendChild(createForm(
            type,
            'create',
            `${type}_form`,
            form,
            `data/${type}/create`,
            data
        ))
    })
}
let getEditForm = (type, itemId, data = {}) => {
    getData(`data/${type}/form`).then(fields => {
        getData(`/data/${type}/${itemId}`).then(data => {
            showModal()
            const cont = $id('modal-content')
            cont.innerHTML = ''
            cont.appendChild(createForm(
                type,
                'edit',
                `${type}_form`,
                fields,
                `/data/${type}/${itemId}/edit`,
                data
            ))
        })
    })
}

let createForm = (type, action, formId, formDescription, url, data = {}) => {
    console.log("----- ---")
    console.log(formId)
    console.log(formDescription)
    console.log(data)
    const form = $create("form")
    form.setAttribute("url", url)
    formId && form.setAttribute("id", formId)
    formSubmit && form.addEventListener('submit', formSubmit)
    form.appendChild(text("type_id", 'type', 'type', type, true, true))

    for (k in formDescription) {
        const field_type = formDescription[k]['type']
        readonly = ! formDescription[k][action]
        console.log(k, readonly)

        let val = null
        if (data.hasOwnProperty(k))
            { val = data[k] }

        if (field_type == 'textarea')
            form.appendChild(
                textarea(`${k}_id`, k, k, val, readonly, readonly)
            )
        else if ( field_type== 'number')
            form.appendChild(number(`${k}_id`, k, k, val, readonly, readonly))
        else
            form.appendChild(text(`${k}_id`, k, k, val, readonly, readonly))
    }

    const cont = $create("div")
    const submit = $create("input")
    submit.setAttribute("type", "submit")
    submit.setAttribute("value", "Submit")

    const cancel = $create("button")
    cancel.setAttribute("type", "reset")
    cancel.setAttribute("onclick", `closeModal(); reload('${type}')`)
    cancel.innerHTML = "Cancel"

    cont.appendChild(submit)
    cont.appendChild(cancel)
    form.appendChild(cont)
    form.classList.add('form')

    return form
}

const text = (id, name, title = null, value = null, readonly = false,
        hidden = false) => {
    const cont = $create("div")
    const input = $create("input")
    const label = $create("label")
    input.setAttribute("type", "text")
    id && input.setAttribute("id", id)
    name && input.setAttribute("name", name)
    value && input.setAttribute("value", value)
    readonly && input.setAttribute("readonly", false)
    label.innerHTML = title || name

    cont.appendChild(label)
    cont.appendChild($create("br"))
    cont.appendChild(input)
    cont.appendChild($create("br"))
    if (hidden)
        cont.style.display = "none"

    return cont
}

const number = (id, name, title = null, value = null, readonly = false,
        hidden = false) => {
    const cont = $create("div")
    const input = $create("input")
    const label = $create("label")
    input.setAttribute("type", "number")
    id && input.setAttribute("id", id)
    name && input.setAttribute("name", name)
    value && input.setAttribute("value", value)
    readonly && input.setAttribute("readonly", false)
    label.innerHTML = title || name

    cont.appendChild(label)
    cont.appendChild($create("br"))
    cont.appendChild(input)
    cont.appendChild($create("br"))
    if (hidden)
        cont.style.display = "none"

    return cont
}

const textarea = (id, name, title = null, value = null, readonly = false,
        hidden = false) => {
    const cont = $create("div")
    const text = $create("textarea")
    const label = $create("label")
    id && text.setAttribute("id", id)
    name && text.setAttribute("name", name)
    text.innerHTML = value
    readonly && text.setAttribute("readonly", false)
    label.innerHTML = title || name

    cont.appendChild(label)
    cont.appendChild($create("br"))
    cont.appendChild(text)
    cont.appendChild($create("br"))
    if (hidden)
        cont.style.display = "none"

    return cont
}
