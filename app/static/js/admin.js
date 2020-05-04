// --------- manipulate types
let createBible = () => getCreateForm('bibles')
let editBible = (id) => getEditForm('bibles', id)
let deleteBible = (id) => deleteForm('bibles', id)

let createPart = (id) => getCreateForm('parts', null, {bible_id: id})
let editPart = (id) => getEditForm('parts', id)
let deletePart = (id) => deleteForm('parts', id)

let createBook = (id) => getCreateForm('books', null, {part_id: id})
let editBook = (id) => getEditForm('books', id)
let deleteBook = (id) => deleteForm('books', id)

let createChapter = (id) => getCreateForm('chapters', null, {book_id: id})
let editChapter = (id) => getEditForm('chapters', id)
let deleteChapter = (id) => deleteForm('chapters', id)

let createVerse = (id) => getCreateForm('verses', null, {chapter_id: id})
let editVerse = (id) => getEditForm('verses', id)
let deleteVerse = (id) => deleteForm('verses', id)

// --------- create by data
let createType = (onClick, type) => {
    const cont = $id("create")
    const link = $create("a")
    onClick && link.setAttribute('onclick', onClick)
    link.setAttribute('href', "Javascript: void(0)")
    link.innerHTML = " create "// + type
    cont.innerHTML = ""
    cont.appendChild(link)
}

// --------- create list
let createBiblesList = (parentId, data) => {
    createType("createBible()", 'Bible')
    const ol = $create("ol")
    const title = $create("strong")
    title.innerHTML = 'Bibles'
    $id('create').insertAdjacentElement('afterbegin', title)
    //ol.appendChild(title)

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        const pgph = $create("p")
        const headLink = $create("a")
        const editLink = $create("a")
        const delLink = $create("a")

        head.appendChild(headLink)
        head.appendChild(editLink)
        head.appendChild(delLink)
        artc.appendChild(head)
        artc.appendChild(pgph)

        headLink.innerHTML = data[i].text
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'bibles')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        editLink.innerHTML = " ✎ "
        editLink.setAttribute(
            'onclick', "editBible(" + data[i].id + ")"
        )
        editLink.setAttribute('href', "Javascript: void(0)")
        delLink.innerHTML = " ❌ "
        delLink.setAttribute(
            'onclick', "deleteBible(" + data[i].id + ")"
        )
        delLink.setAttribute('href', "Javascript: void(0)")
        pgph.innerHTML = data[i].description

        li.appendChild(artc)
        ol.appendChild(li)
    }
    return ol
}

let createPartsList = (parentId, data) => {
    createType('createPart(' + parentId + ')', 'Part')
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Parts'
    $id('create').insertAdjacentElement('afterbegin', title)
    //ul.appendChild(title)

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        // const pgph = $create("p")
        const headLink = $create("a")
        const editLink = $create("a")
        const delLink = $create("a")

        head.appendChild(headLink)
        head.appendChild(editLink)
        head.appendChild(delLink)
        artc.appendChild(head)
        // artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'parts')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        editLink.innerHTML = " ✎ "
        editLink.setAttribute(
            'onclick', "editPart(" + data[i].id + ")"
        )
        editLink.setAttribute('href', "Javascript: void(0)")
        delLink.innerHTML = " ❌ "
        delLink.setAttribute(
            'onclick', "deletePart(" + data[i].id + ")"
        )
        delLink.setAttribute('href', "Javascript: void(0)")
        // pgph.innerHTML = data[i].text

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createBooksList = (parentId, data) => {
    createType('createBook(' + parentId + ')', 'Book')
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Books'
    $id('create').insertAdjacentElement('afterbegin', title)
    //ul.appendChild(title)

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        // const pgph = $create("p")
        const headLink = $create("a")
        const editLink = $create("a")
        const delLink = $create("a")

        head.appendChild(headLink)
        head.appendChild(editLink)
        head.appendChild(delLink)
        artc.appendChild(head)
        // artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'books')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        editLink.innerHTML = " ✎ "
        editLink.setAttribute(
            'onclick', "editBook(" + data[i].id + ")"
        )
        editLink.setAttribute('href', "Javascript: void(0)")
        delLink.innerHTML = " ❌ "
        delLink.setAttribute(
            'onclick', "deleteBook(" + data[i].id + ")"
        )
        delLink.setAttribute('href', "Javascript: void(0)")
        // pgph.innerHTML = data[i].text

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createChaptersList = (parentId, data) => {
    createType('createChapter(' + parentId + ')', 'Chapter')
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Chapters'
    $id('create').insertAdjacentElement('afterbegin', title)
    //ul.appendChild(title)

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        const pgph = $create("p")
        const headLink = $create("a")
        const editLink = $create("a")
        const delLink = $create("a")

        head.appendChild(headLink)
        head.appendChild(editLink)
        head.appendChild(delLink)
        artc.appendChild(head)
        artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'chapters')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        editLink.innerHTML = " ✎ "
        editLink.setAttribute(
            'onclick', "editChapter(" + data[i].id + ")"
        )
        editLink.setAttribute('href', "Javascript: void(0)")
        delLink.innerHTML = " ❌ "
        delLink.setAttribute(
            'onclick', "deleteChapter(" + data[i].id + ")"
        )
        delLink.setAttribute('href', "Javascript: void(0)")
        pgph.innerHTML = data[i].description

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createVersesList = (parentId, data) => {
    createType('createVerse(' + parentId + ')', 'Verse')
    const cont = $create("div")
    const title = $create("strong")
    title.innerHTML = 'Verses'
    $id('create').insertAdjacentElement('afterbegin', title)
    //cont.appendChild(title)

    for (i in data) {
        const number = $create("strong")
        const pgph = $create("p")
        const editLink = $create("a")
        const delLink = $create("a")

        pgph.appendChild(number)
        pgph.appendChild($createTxt(`${data[i].text} `))
        pgph.appendChild(editLink)

        number.innerHTML = `${data[i].number} `
        editLink.innerHTML = " ✎ "
        editLink.setAttribute(
            'onclick', `editVerse(${data[i].id})`
        )
        editLink.setAttribute('href', "Javascript: void(0)")
        if (i == data.length - 1 ) {
            delLink.innerHTML = " ❌ "
            delLink.setAttribute('onclick', `deleteVerse(${data[i].id})`)
            pgph.appendChild(delLink)
        }
        delLink.setAttribute('href', "Javascript: void(0)")
        cont.appendChild(pgph)
    }
    return cont
}
