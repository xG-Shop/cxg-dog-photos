# Botón «Publicar fotos» de DOGS MAKER

Encargo para quien mantiene DOGS MAKER (C3DClothTool, `DogsMaker/`). El repo de fotos ya existe en
`C:\[TOOL]\cxg-dog-photos` (remoto `xG-Shop/cxg-dog-photos`, público). El script que regenera el catálogo
ya está hecho: `tools/build_catalog.py`.

## Lo que hace el botón

Un botón en la pestaña DOGS MAKER, «Publicar fotos en GitHub», que:

1. **Renderiza las fotos en Blender** de cada perro generado (adulto, `_juvenile` y `_puppy`), si faltan o
   si el modelo es más nuevo que la foto:
   - `<modelo>_photo.webp` con el aspecto de macho (`looks.male`, drawable 0 de la cabeza) y
     `<modelo>_photo_female.webp` con el de hembra (`looks.female`).
   - 512×512, fondo transparente, vista 3/4 desde delante y un poco desde arriba, luz de estudio, Eevee
     (no Workbench), con su textura. El mismo encuadre para todos: la cámara se ajusta a los límites del
     modelo, así que un shiba y un dóberman llenan la foto igual.
   - Se guardan en la raíz del recurso y se añaden a `files { }` de su `fxmanifest.lua` (el companion
     las carga como `nui://<modelo>/<modelo>_photo.webp`).
2. **Regenera el catálogo**:
   `python tools/build_catalog.py --pets <carpeta de recursos> [--bundle <cxg_companion>]`.
   Copia la foto de cada adulto a `photos/<familia>.webp` y escribe `catalog.json`.
3. **Publica**: en `C:\[TOOL]\cxg-dog-photos`, `git add catalog.json photos` → commit «Fotos: <razas>»
   → `git push`. Si no hay cambios, lo dice y no hace commit.
4. Muestra el resultado en la tool (razas publicadas, cuáles no tienen foto, error de push si lo hay).

## Configuración (`Engine/config.json`)

```json
"photos_repo": "C:/[TOOL]/cxg-dog-photos",
"companion_folder": "E:/[PRODIGY 4.0 ASSETS]/prodigy-insanity-assets/[PETS]/cxg_companion"
```

`companion_folder` es opcional: si existe, también se actualiza la copia que va dentro del companion.

## Seguridad

- El repo solo puede contener `catalog.json`, `photos/`, `tools/`, `docs/` y `README.md`. El botón solo
  añade `catalog.json` y `photos/`: nunca `git add -A`.
- Para subir usa la sesión de git o `gh` que ya hay en el PC. **Nunca** guardes un token en `config.json`
  ni en el repo.
