# Guía de Contribución para Cinetica

¡Gracias por tu interés en contribuir a Cinetica! Agradecemos cualquier tipo de contribución, ya sea reportando bugs, sugiriendo nuevas características, mejorando la documentación o enviando código.

## Cómo Contribuir

### 1. Reportar Bugs

Si encuentras un bug, por favor, abre un "issue" en el repositorio de GitHub. Incluye la siguiente información:
- Una descripción clara y concisa del bug.
- Pasos para reproducir el comportamiento.
- El comportamiento esperado.
- El comportamiento actual.
- Cualquier mensaje de error o "stack trace" relevante.
- Tu sistema operativo y versión de Python.

### 2. Sugerir Nuevas Características

Si tienes una idea para una nueva característica, abre un "issue" en GitHub para discutirla. Esto nos permite asegurarnos de que la característica se alinea con los objetivos del proyecto y evitar trabajo duplicado.

### 3. Mejorar la Documentación

La documentación es crucial. Si encuentras errores tipográficos, secciones poco claras o tienes ideas para mejorarla, puedes:
- Abrir un "issue" describiendo la mejora.
- Enviar un "pull request" directamente con los cambios.

### 4. Contribuir Código

Si deseas contribuir con código, sigue estos pasos:

1.  **Haz un "fork" del repositorio:** Haz clic en el botón "Fork" en la parte superior derecha del repositorio de GitHub.
2.  **Clona tu "fork":**
    ```bash
    git clone https://github.com/TU_USUARIO/Cinetica.git
    cd Cinetica
    ```
3.  **Crea una nueva rama:**
    ```bash
    git checkout -b mi-nueva-caracteristica
    ```
    Usa un nombre descriptivo para tu rama (ej. `feat/nombre-caracteristica`, `fix/nombre-bug`).
4.  **Instala las dependencias de desarrollo:**
    ```bash
    pip install -e .
    pip install pytest pytest-cov
    ```
5.  **Realiza tus cambios:** Escribe tu código, asegurándote de seguir el estilo de codificación existente.
6.  **Escribe tests:** Si agregas nuevas características o corriges bugs, asegúrate de incluir tests unitarios que cubran tus cambios.
7.  **Ejecuta los tests:**
    ```bash
    python -m pytest
    ```
    Asegúrate de que todos los tests pasen.
8.  **Actualiza la documentación:** Si tus cambios afectan la funcionalidad o el uso de la librería, actualiza el `README.md` y el `CHANGELOG.md` según sea necesario.
9.  **Haz "commit" de tus cambios:**
    ```bash
    git add .
    git commit -m "feat: Descripción concisa de tu característica o arreglo"
    ```
    Usa un mensaje de commit claro y descriptivo.
10. **Haz "push" a tu "fork":**
    ```bash
    git push origin mi-nueva-caracteristica
    ```
11. **Abre un "Pull Request":** Ve a tu repositorio "forkeado" en GitHub y abre un "Pull Request" a la rama `master` del repositorio original. Describe tus cambios en detalle.

## Estilo de Código

- Sigue las convenciones de estilo de Python (PEP 8).
- Utiliza "docstrings" para documentar clases, métodos y funciones.

¡Gracias de nuevo por tu ayuda para mejorar Cinetica!
