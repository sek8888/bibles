// --------- onclick on item
let onClickItem = (id, type) => {
    const select = $id(`${type}_selector`)
    select.value = id
    select.onchange()
}

let createCont = (object) => {
    console.log('createCont')
    let cont = $id("data")
    cont.innerHTML = ''
    cont.appendChild(object)
}

let createBibles = (parentId, data) =>
    createCont(createBiblesList(parentId, data))

let createParts = (parentId, data) =>
    createCont(createPartsList(parentId, data))

let createBooks = (parentId, data) =>
    createCont(createBooksList(parentId, data))

let createChapters = (parentId, data) =>
    createCont(createChaptersList(parentId, data))

let createVerses = (parentId, data) =>
    createCont(createVersesList(parentId, data))

let init = () => {
    Selectors = new selectors('nav_selectors', 'Selectors')
    Selectors.callbacks = {
        'bibles': createBibles,
        'parts': createParts,
        'books': createBooks,
        'chapters': createChapters,
        'verses': createVerses,
    }
    Selectors.init()
}

let reload = (type = null) =>
    Selectors.reload(type)

document.addEventListener("DOMContentLoaded", () => { init() })
