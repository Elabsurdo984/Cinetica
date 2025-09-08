# Reglas para la Asistencia en el Proyecto Cinetica

## Objetivo Principal
Asistir en el desarrollo de Cinetica, una biblioteca de física en Python, siguiendo las mejores prácticas de desarrollo de software y manteniendo altos estándares de calidad.

## Estándares de Código
1. **Formato**: Seguir las configuraciones de Black (longitud de línea 88) ya establecidas en el proyecto.
2. **Tipado**: Usar type hints en todo el código, siguiendo las configuraciones de MyPy.
3. **Documentación**: 
   - Docstrings en formato Google Style
   - Documentación clara de parámetros, retornos y excepciones
   - Comentarios explicativos para lógica compleja

## Estructura del Proyecto
- Mantener la estructura modular existente:
  - `cinetica/cinematica/` para módulos de cinemática
  - `cinetica/dinamica/` para módulos de dinámica
  - `tests/` para pruebas unitarias e integrales
  - `usage/` para ejemplos de uso

## Pruebas
1. Escribir pruebas unitarias para toda funcionalidad nueva
2. Mantener una cobertura de pruebas alta (>90%)
3. Usar naming descriptivo para los tests siguiendo el patrón: `test_<método>_<condición>_<resultado_esperado>`

## Documentación
1. Mantener actualizados:
   - README.md con instrucciones básicas de instalación y uso
   - DOCS.md con documentación detallada de la API
   - CHANGELOG.md siguiendo SemVer

## Flujo de Trabajo
1. **Análisis**: Discutir los requisitos antes de implementar
2. **Implementación**: Código limpio y bien documentado
3. **Pruebas**: Asegurar cobertura adecuada
4. **Revisión**: Revisar cambios antes de hacer commit
5. **Documentación**: Actualizar documentación según sea necesario

## Convenciones de Código
1. **Nombres descriptivos** para variables, funciones y clases
2. **Funciones pequeñas** con una sola responsabilidad
3. **Manejo de errores** adecuado con mensajes claros
4. **Uso de unidades** consistente con la biblioteca Pint

## Prioridades
1. **Corrección**: El código debe ser correcto ante todo
2. **Claridad**: Código legible y mantenible
3. **Eficiencia**: Optimizar solo cuando sea necesario y con pruebas que lo justifiquen

## Comunicación
- Ser claro y conciso en las explicaciones
- Proporcionar contexto cuando sea necesario
- Ofrecer alternativas cuando corresponda
- Explicar el razonamiento detrás de las soluciones propuestas
