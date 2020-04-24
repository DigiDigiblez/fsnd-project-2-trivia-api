from .models import Category


#  Helper function to find the category type.
def find_category_type(id: int):
    categories: [] = Category.query.all()
    category_found = None

    for category in categories:
        if category.id == id:
            category_found = category.type

    return category_found
