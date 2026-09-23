# Reducción del inventario público de prueba

El commit `6abaf20` contiene el inventario inicial con tres identificadores
ficticios y una descripción de la función de cada uno. La versión actual
elimina las funciones y deja solamente tres identificadores ficticios, sin
IP, cuentas, rutas internas ni secretos.

Comparación reproducible:

```bash
git show 6abaf20:public-inventory.txt
cat public-inventory.txt
git diff 6abaf20 -- public-inventory.txt
```

Esto es una **reducción local de exposición de contenido**. Aún falta
verificar en el servidor autorizado que `/public-inventory.txt` entregue el
contenido reducido y que Nginx haya aplicado el hardening. No se atribuye al
ejercicio Red/Blue que todavía no se ejecuta.
