from project_manager import ProjectManager


print("=" * 50)
print("TEST 1 - Guardar proyecto")
print("=" * 50)

sound_files = {

    "navigation":
    "navigation.mp3",

    "home_intro":
    "home_intro.mp3",

    "background_music":
    "background_music.opus"
}

success = ProjectManager.save_project(
    "test.tsbp",
    "Test Project",
    sound_files
)

print(
    f"Guardado correcto: {success}"
)

print()


print("=" * 50)
print("TEST 2 - Cargar proyecto")
print("=" * 50)

project = ProjectManager.load_project(
    "test.tsbp"
)

print(project)

print()


print("=" * 50)
print("TEST 3 - Validar estructura")
print("=" * 50)

valid = ProjectManager.validate_project(
    project
)

print(
    f"Estructura válida: {valid}"
)

print()


print("=" * 50)
print("TEST 4 - Validar versión")
print("=" * 50)

supported = (
    ProjectManager.is_supported_version(
        project
    )
)

print(
    f"Versión soportada: {supported}"
)

print()


print("=" * 50)
print("TEST 5 - Validar existencia de archivos")
print("=" * 50)

validation = (
    ProjectManager.validate_files(
        project["files"] # type: ignore
    )
)

for sound_name, exists in validation.items():

    print(
        f"{sound_name}: {exists}"
    )

print()


print("=" * 50)
print("TEST 6 - Archivos faltantes")
print("=" * 50)

missing = (
    ProjectManager.get_missing_files(
        project["files"] # type: ignore
    )
)

print(
    f"Archivos faltantes: {missing}"
)

print()


print("=" * 50)
print("TEST 7 - Proyecto existe")
print("=" * 50)

exists = (
    ProjectManager.project_exists(
        "test.tsbp"
    )
)

print(
    f"Proyecto encontrado: {exists}"
)

print()


print("=" * 50)
print("TEST 8 - Archivo corrupto")
print("=" * 50)

broken_project = {

    "project_name":
    "Broken Project"
}

valid = (
    ProjectManager.validate_project(
        broken_project
    )
)

print(
    f"Proyecto válido: {valid}"
)

print()


print("=" * 50)
print("TEST 9 - Versión no soportada")
print("=" * 50)

future_project = {

    "version":
    "2.5"
}

supported = (
    ProjectManager.is_supported_version(
        future_project
    )
)

print(
    f"Versión soportada: {supported}"
)

print()


print("=" * 50)
print("TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 50)