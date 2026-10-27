# SCF Agent Skills

## Estado y hoja de ruta

| Paso | Nombre | Skill | Estado |
|---|---|---|---|
| 1 | Preparación | `prep` | Disponible |
| 2 | Análisis y Diseño | `analysis` | Disponible |
| 3 | Propuesta de implementación | `impl-proposal` | Disponible |
| 4 | Implementación Agéntica | `impl` | En desarrollo |
| 5 | Auditoría | `audit` | Planificado |
| 6 | Tests | `test` | Planificado |
| 7 | Documentación | `docs` | Planificado |
| 8 | Integración | `integration` | Planificado |

No hay releases, pero es una buena idea en el futuro, cuando estén disponibles las 8 skills y vayan requiriendo mantenimiento

## Requisitos

- Un agente compatible con la especificación [Agent Skills](https://agentskills.io/specification). Las skills son agnósticas al agente. Hasta ahora se probaron con Claude.ai y Antigravity.
- Python 3.8+, standard lib. Lo usan los scripts de renderizado y validación de Dossiers.
- `bash`/`zsh` y `zip`, para empaquetar las skills.
- Acceso a ClickUp (opcional). Si el agente tiene una herramienta de ClickUp, `prep` puede leer la tarea directamente desde su ID o URL.

## Instalación y uso

1. Clonar el repositorio y entrar en él:

   ```bash
   git clone https://gitlab.com/midasconsultores/i-d-i/scf-skills/scf-skills.git
   cd scf-skills
   ```

2. Empaquetar las skills:

   ```bash
   ./package_skills.sh
   ```

3. Copiar los `.zip` generados en `export/` a la carpeta de skills de tu agente.
4. Las skills se invocan manualmente: `/prep`, `/analysis`, `/impl-proposal`, etc.

## Contribuir

Antes de crear o modificar una skill, leer [`CONVENTIONS.md`](CONVENTIONS.md). Todas las skills se rigen por ese estándar. Si el estándar cambia, las skills deben ser actualizadas para estar al día.

Las referencias compartidas (`grilling.md`, `impact-lenses.md`, `caveman.md` y los scripts de Dossier) se editan solo en `shared/`. `sync-refs.sh` luego los copia a cada skill.

### Flujo de ramas

Nos hemos esmerado por mantener un historial semilineal, que preserva siempre el historial de los cambios y su procedencia, sin contar que minimiza la necesidad de resolver merge conflicts.
- `develop` está protegida y solo cambia mediante *merge requests* aprobados.
- Las ramas de trabajo se actualizan siempre con *rebase*, nunca con *fast-forward* ni *merge*.
- De una rama pueden salir más, siempre manteniendo el historial semilineal (ver historial entre f22d4d1 y ac1e0142).

### Pruebas

## Buenas prácticas

- **Evitar ejecuciones iterativas.** Re-ejecutar una skill sobre su propia salida para "pulirla" es una principal causa de alucinaciones y otros problemas. Conviene corregir la entrada y ejecutar de nuevo desde cero.
- **No incluir información que cambió o va a cambiar.** Se contamina el contexto y el modelo no olvida los datos que le das aunque se lo pidas.
- **Reunir mucha información antes de recurrir a la IA.** Tener buena información de entrada reduce la cantidad de preguntas en cada sesión de *grilling*. Si no, puede ser bastante cansador.

## Créditos

- **Matías Campoy**: diseño del Systemic Context Framework.
- **Cristóbal González** y **Facundo Guiñazú**: desarrollo de todo lo realizado hasta la fecha.
- **JuliusBrussee**: skill *caveman*, adaptada e incluida en este repositorio.
- **Matt Pocock**: skill de *grilling*, adaptada e incluida en este repositorio.
