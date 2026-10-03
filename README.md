# cxg-dog-photos

Solo contiene fotos y la lista de razas: ningún código, ninguna clave.

La colección de razas CXG que enseña la tienda de [cxg_companion](https://github.com/xG-Shop/cxg_companion). Cada servidor la lee desde aquí. Las razas que tiene instaladas se pueden adoptar y las demás salen bloqueadas, con su foto. Cuando se publica una raza nueva, aparece en todos los servidores sin que actualicen nada.

## Contenido

- `catalog.json`: la lista de razas.
- `photos/<familia>.webp`: la foto de cada raza (el adulto), cuadrada y con fondo transparente o neutro.
- `tools/build_catalog.py`: regenera los dos a partir de los perros hechos con DOGS MAKER.

## Formato de `catalog.json`

```json
{
  "version": 1,
  "store": "https://tu-tienda/cxg",
  "breeds": [
    {
      "family": "cxg_doberman",
      "label": "Dóberman",
      "ages": ["puppy", "juvenile", "adult"],
      "withers_cm": 68.0,
      "photo": "https://raw.githubusercontent.com/xG-Shop/cxg-dog-photos/main/photos/cxg_doberman.webp"
    }
  ]
}
```

- `family` es el nombre del recurso del adulto. El companion lo compara con las razas instaladas.
- `photo` tiene que ser una dirección `https://`. Si no hay foto, la tablet muestra una silueta.
- `store` (opcional) es dónde comprar las razas bloqueadas.

## Añadir una raza

1. Genera el perro con DOGS MAKER: adulto y, si quieres, `_juvenile` y `_puppy`. Debe escribir `<familia>_photo.webp` en el recurso del adulto.
2. Ejecuta el script:

   ```
   python tools/build_catalog.py --pets "E:/[PRODIGY 4.0 ASSETS]/prodigy-insanity-assets/[PETS]" --bundle "E:/[PRODIGY 4.0 ASSETS]/prodigy-insanity-assets/[PETS]/cxg_companion"
   ```

   Con `--bundle` también se actualiza la copia que va dentro de cxg_companion, que sirve cuando no hay conexión.
3. Haz commit y push de `catalog.json` y `photos/`.

## En el servidor

En `cxg_companion/shared/genetics.lua`:

```lua
Config.Catalog.Url = 'https://raw.githubusercontent.com/xG-Shop/cxg-dog-photos/main/catalog.json'
```

El companion lo vuelve a leer cada `Config.Catalog.RefreshMinutes`. Si la descarga falla, usa la copia incluida.
