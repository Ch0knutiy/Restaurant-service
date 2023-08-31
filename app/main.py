import uvicorn
from api import dish, menu, menu_to_file, submenu
from database import init_models
from fastapi import FastAPI

app = FastAPI()

app.include_router(menu_to_file.router, tags=['FileWriter'], prefix='/api/v1/menus')
app.include_router(menu.router, tags=['Menus'], prefix='/api/v1/menus')
app.include_router(submenu.router, tags=['Submenus'], prefix='/api/v1/menus')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus')


@app.on_event('startup')
async def startup():
    await init_models()


@app.get('/health', status_code=200)
async def root():
    return {'message': 'Ок'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
