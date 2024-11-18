from fastapi import APIRouter

from app.shema import CategoryShema

from fixtures import categories as fixture_categories

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)

@router.get('/all', response_model=list[CategoryShema])
async def get_all_categories():
    return fixture_categories


@router.post('/', response_model=CategoryShema)
async def create_category(category: CategoryShema):
    fixture_categories.append(dict(category))
    return category


@router.patch('/{category_id}', response_model=CategoryShema)
async def update_categories(category_id: int, name: str):
    for category in fixture_categories:
        print(category)
        if category['id'] == category_id:
            category['name'] = name
            return category


