from app.models import (
    Bibles,
    Parts,
    Books,
    Chapters,
    Verses
)


class Controller:
    def __init__(self):
        self.table_classes = {
            "bibles": Bibles,
            "parts": Parts,
            "books": Books,
            "chapters": Chapters,
            "verses": Verses,
        }

    def list_table(self, table_name, parent_id) -> list:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return []

        table = table_class()
        where = ["1"]
        values = {}
        # left join table
        if parent_id:
            values.update({"parent_id": parent_id})
            where.append(f"{table.parent[:-1]}_id = :parent_id")
            table.join(
                table.parent,
                f"{table_name}.{table.parent[:-1]}_id = {table.parent}.id",
                []
            )

        cur = table.select(" AND ".join(where), values)
        lines = []
        for row in cur:
            lines.append(row._asdict())

        return lines

    def get_record(self, table_name, id) -> dict:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return {}

        rec = table_class().get(id=id)

        return rec._asdict() if rec else {}

    def get_fields(self, table_name) -> dict:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return {}

        return table_class().form_fields

    def delete_record(self, table_name, id) -> dict:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return {"status": 1, "message": "---"}

        table = table_class()
        if table.child:
            # check child record
            result = self.table_classes[table.child]().find(
                f"{table_name[:-1]}_id = :parent_id",
                {"parent_id": id}
            )
            if result:
                return {
                    "status": 1,
                    "message": f"Can't remove this item, as it has a child"
                }

        count = table.delete_by_id(id)

        return {"status": 0, "message": "Deleted"} \
            if count else {"status": 1, "message": "---"}

    def edit_record(self, table_name, id, form) -> dict:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return {"status": 1, "message": "---"}

        # TODO: validate form
        count = table_class().edit(id, form)

        return {"status": 0, "message": "Edited"} \
            if count else {"status": 1, "message": "---"}

    def create_record(self, table_name, form) -> dict:
        table_class = self.table_classes.get(table_name)
        if not table_class:
            return {"status": 1, "message": "Invalid type"}

        # TODO: validate form
        status = 0
        try:
            rec_id = table_class().add(form)
            message = f"record id: {rec_id}"
        except Exception as ex:
            status = 1
            message = str(ex)
            print(message)

        return {"status": status, "message": message}
