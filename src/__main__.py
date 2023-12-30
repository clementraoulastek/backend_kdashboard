# Nom du Projet: Kamas Dashboard
# Auteur: RAOUL Clément
# Date de Création: 17-12-2023
# Description: Ce projet à pour unique but de visualer le cours d'une devise virtuelle
# Licence: MIT License

"""Entrypoint for the API."""

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.controllers import kamas_controller

app = FastAPI(title="API for kamas dashboard")
app.include_router(kamas_controller.router)

register_tortoise(
    app,
    db_url="sqlite://src/db/db.sqlite3",
    modules={"models": ["src.models.kamas_model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
