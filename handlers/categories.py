from fastapi import APIRouter

from shema.categories import Category

from fixtures import categories as fixture_categories

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)

@router.get('/all', response_model=list[Category])
async def get_all_categories():
    return fixture_categories


@router.post('/', response_model=Category)
async def create_category(category: Category):
    fixture_categories.append(dict(category))
    return category


@router.patch('/{category_id}', response_model=Category)
async def update_categories(category_id: int, name: str):
    for category in fixture_categories:
        print(category)
        if category['id'] == category_id:
            category['name'] = name
            return category


