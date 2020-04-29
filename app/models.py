from app.lib.model_view import ModelView


class Bibles(ModelView):
    """ Model class for bibles

    """
    __slots__ = 'parent', 'form_fields', 'child'

    def __init__(self):
        self.table_name = 'bibles'
        self.fields = {
            'id': {'rdonly': True},
            'text': None,
            'description': None,
        }
        self.parent = None
        self.child = 'parts'
        self.form_fields = {
            'id': {'edit': False, 'create': False},
            'text': {'edit': True, 'create': True},
            'description': {'edit': True, 'create': True, 'type': 'textarea'},
        }
        super().__init__()


class Parts(ModelView):
    """ Model class for parts

    """
    __slots__ = 'parent', 'form_fields', 'child'

    def __init__(self):
        self.table_name = 'parts'
        self.fields = {
            'id': {'rdonly': True},
            'bible_id': None,
            'number': None,
            'text': None,
        }
        self.parent = 'bibles'
        self.child = 'books'
        self.form_fields = {
            'id': {'edit': False, 'create': False},
            'bible_id': {'edit': False, 'create': False},
            'number': {'edit': True, 'create': True, 'type': 'number'},
            'text': {'edit': True, 'create': True, 'type': 'textarea'},
        }
        super().__init__()


class Books(ModelView):
    """ Model class for books

    """
    __slots__ = 'parent', 'form_fields', 'child'

    def __init__(self):
        self.table_name = 'books'
        self.fields = {
            'id': {'rdonly': True},
            'part_id': None,
            'number': None,
            'text': None,
        }
        self.parent = 'parts'
        self.child = 'chapters'
        self.form_fields = {
            'id': {'edit': False, 'create': False},
            'part_id': {'edit': False, 'create': False},
            'number': {'edit': True, 'create': True, 'type': 'number'},
            'text': {'edit': True, 'create': True, 'type': 'textarea'},
        }
        super().__init__()


class Chapters(ModelView):
    """ Model class for chapters

    """
    __slots__ = 'parent', 'form_fields', 'child'

    def __init__(self):
        self.table_name = 'chapters'
        self.fields = {
            'id': {'rdonly': True},
            'book_id': None,
            'number': None,
            'text': None,
        }
        self.parent = 'books'
        self.child = 'verses'
        self.form_fields = {
            'id': {'edit': False, 'create': False},
            'book_id': {'edit': False, 'create': False},
            'number': {'edit': True, 'create': True, 'type': 'number'},
            'text': {'edit': True, 'create': True, 'type': 'textarea'},
        }
        super().__init__()


class Verses(ModelView):
    """ Model class for verses

    """
    __slots__ = 'parent', 'form_fields', 'child'

    def __init__(self):
        self.table_name = 'verses'
        self.fields = {
            'id': {'rdonly': True},
            'chapter_id': None,
            'number': None,
            'text': None,
        }
        self.parent = 'chapters'
        self.child = None
        self.form_fields = {
            'id': {'edit': False, 'create': False},
            'chapter_id': {'edit': False, 'create': False},
            'number': {'edit': True, 'create': True, 'type': 'number'},
            'text': {'edit': True, 'create': True, 'type': 'textarea'},
        }
        super().__init__()
