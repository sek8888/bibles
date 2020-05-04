// --------- create list
let createBiblesList = (parentId, data) => {
    const ol = $create("ol")
    const title = $create("strong")
    title.innerHTML = 'Bibles'
    $id('title').innerHTML = title.outerHTML

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        const pgph = $create("p")
        const headLink = $create("a")

        head.appendChild(headLink)
        artc.appendChild(head)
        artc.appendChild(pgph)

        headLink.innerHTML = data[i].text
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'bibles')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        pgph.innerHTML = data[i].description

        li.appendChild(artc)
        ol.appendChild(li)
    }
    return ol
}

let createPartsList = (parentId, data) => {
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Parts'
    $id('title').innerHTML = title.outerHTML

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        //const pgph = $create("p")
        const headLink = $create("a")

        head.appendChild(headLink)
        artc.appendChild(head)
        //artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'parts')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        //pgph.innerHTML = data[i].text

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createBooksList = (parentId, data) => {
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Books'
    $id('title').innerHTML = title.outerHTML

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        // const pgph = $create("p")
        const headLink = $create("a")

        head.appendChild(headLink)
        artc.appendChild(head)
        // artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'books')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        // pgph.innerHTML = data[i].text

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createChaptersList = (parentId, data) => {
    const ul = $create("ul")
    const title = $create("strong")
    title.innerHTML = 'Chapters'
    $id('title').innerHTML = title.outerHTML

    for (i in data) {
        const li = $create("li")
        const artc = $create("article")
        const head = $create("h3")
        const pgph = $create("p")
        const headLink = $create("a")

        head.appendChild(headLink)
        artc.appendChild(head)
        artc.appendChild(pgph)

        headLink.innerHTML = `${data[i].number}. ${data[i].text}`
        headLink.setAttribute(
            'onclick', `onClickItem(${data[i].id}, 'chapters')`
        )
        headLink.setAttribute('href', "Javascript: void(0)")
        pgph.innerHTML = data[i].description

        li.appendChild(artc)
        ul.appendChild(li)
    }
    return ul
}

let createVersesList = (parentId, data) => {
    const cont = $create("div")
    const title = $create("strong")
    title.innerHTML = 'Verses'
    $id('title').innerHTML = title.outerHTML

    for (i in data) {
        const number = $create("strong")
        const pgph = $create("p")

        pgph.appendChild(number)
        pgph.appendChild($createTxt(`${data[i].text} `))

        number.innerHTML = `${data[i].number} `
        cont.appendChild(pgph)
    }
    return cont
}
