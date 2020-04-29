class selectors {
    constructor(contId, instance_name) {
        this.contId = contId
        this.inst_name = instance_name
        this.types = ['bibles', 'parts', 'books', 'chapters', 'verses']
        this.states = this.getMemoryStates()
        this.callbacks = {
            'bibles': null,
            'parts': null,
            'books': null,
            'chapters': null,
            'verses': null,
        }
        console.log('first', this.states)
    }

    init() {
        this.create()

        setLoader()
        this.loadData('bibles')
    }

    // ------- generic methods start
    getStateIndex(type) { return this.types.indexOf(type)}

    getStateType(index) { return this.types[index]}

    getState(type) {return this.states[this.getStateIndex(type)]}

    getParentState(type)
        { return this.states[this.getStateIndex(type) - 1] || '0' }

    getNextType(type) { return this.types[this.types.indexOf(type) + 1] }

    setMemory(key, val) { localStorage.setItem(key, JSON.stringify(val)) }

    getMemory(key) { return JSON.parse(localStorage.getItem(key)) }

    getMemoryStates(type) {
        let states = this.getMemory('states')
        if (states)
            return states

        // load zeroes for default value
        states = []
        for (let i = 0; i < this.types.length; i++)
            states.push('0')

        this.setMemory('states', states)

        return states
    }

    getLastCallType() {
        let last_idx = null
        for (let i in this.states) {
            last_idx = i
            if (this.states[i] == '0')
                break
        }

        return this.types[last_idx]
    }
    // ------- generic methods end

    create() {
        const cont = $id(this.contId)
        cont.appendChild(new selector('bibles_selector').create(
            'bibles',
            'Bibles',
            {onchange: `${this.inst_name}.onSelect(this)`}
        ))

        cont.appendChild(new selector('parts_selector').create(
            'parts',
            'Parts',
            {onchange: `${this.inst_name}.onSelect(this)`}
        ))

        cont.appendChild(new selector('books_selector').create(
            'books',
            'Books',
            {onchange: `${this.inst_name}.onSelect(this)`}
        ))

        cont.appendChild(new selector('chapters_selector').create(
            'chapters',
            'Chapters',
            {onchange: `${this.inst_name}.onSelect(this)`}
        ))
    }

    reload(type = null) {
        type = type || 'bibles'
        setLoader()
        this.loadData(type)
        //this.loadCascade(type)
    }

    /*
    loadCascade(type = null) {
        console.log('-- loadCascade', type)
        const nextType = this.getNextType(type)
        const loadType = nextType || type || 'bibles'
        console.log('-- loadCascade', loadType)

        setLoader()
        this.loadData(loadType)
    }
    */

    onSelect(selector) {
        const type = selector.name
        console.log('--- --- --- onSelect', type, selector.value)
        let i = this.getStateIndex(type)
        let sel = null
        this.states[i] = selector.value

        // clean child selectors and child selectors states
        for (i += 1; i < this.types.length; i++) {
            this.states[i] = '0'
            //console.log('------update -> 0 ----', this.types[i])
            // clean selectors
            sel = $id(`${this.types[i]}_selector`)
            if (sel)
                 { sel.innerHTML = '' }
        }

        this.setMemory('states', this.states)
        console.log(this.states)

        setLoader()
        this.loadData(type)
    }

    // ------- Load data
    loadData(type) {
        console.log('--- loadData', type)
        const value = this.getState(type)
        const parentValue = this.getParentState(type)
        const callback = this.callbacks[type]
        const nextType = this.getNextType(type)
        const lastCallType = this.getLastCallType()
        console.log('value', value)
        console.log('parentValue', parentValue)
        console.log('lastCallType', lastCallType)
        console.log('nextType', nextType)

        getData(`/data/${parentValue}/${type}/list`).then(data => {
            nextType && new selector(`${type}_selector`).update(
                data.map(d => ({[d.id]: d.text})),
                value
            )

            // call last type's callback
            lastCallType == type && callback && callback(parentValue, data)
            lastCallType == type && rmLoader()

            nextType && value != '0' && this.loadData(nextType)
        })
    }
}


class selector {
    constructor(id) {
        this.id = id
    }

    create(name, label, events = {}) {
        const cont = $create("div")
        const lbl = $create("label")
        const select = $create("select")

        select.setAttribute('id', this.id)
        select.setAttribute('name', name)
        lbl.innerHTML = label

        for (let e in events)
            select.setAttribute(e, events[e])

        cont.appendChild(lbl)
        cont.appendChild(select)

        return cont
    }

    update(data, value = null, empty = 1) {
        const select = $id(this.id)
        select.innerHTML = ''

        if ( data.length > 0 ) {
            if ( empty ) {
                const optEmpty = $create("option")
                optEmpty.setAttribute('value', '0')
                select.appendChild(optEmpty)
            }
            for (let i in data) {
                for (let k in data[i]) {
                    const opt = $create("option")
                    opt.setAttribute('value', k)
                    opt.innerHTML = data[i][k]
                    select.appendChild(opt)
                }
            }
        }
        select.value = value
        return select
    }
}
