# Revisión completa de la memoria TFM con referencias UPM

Fecha: 2026-06-28

## Fuentes revisadas

- Skill actualizada: `/Users/jordi/.codex/skills/redactar-memoria-tfm/SKILL.md`.
- Nueva referencia de skill: `/Users/jordi/.codex/skills/redactar-memoria-tfm/references/upm-aerial-rl-reference-memories.md`.
- Guía UPM: `/Users/jordi/GitHub/TFM/referencias UPM/Guía_para_redacción_y_presentación_de_TFT.pdf`.
- Referencias UPM similares:
  - `/Users/jordi/GitHub/TFM/referencias UPM/TFM_JAVIER_MELERO_DEZA.pdf`.
  - `/Users/jordi/GitHub/TFM/referencias UPM/TFM_AITOR_LOPEZ_SANCHEZ.pdf`.
  - `/Users/jordi/GitHub/TFM/referencias UPM/TFG_ANASTASIA_MURAN_TRUS.pdf`.
- Memoria actual: `/Users/jordi/GitHub/TFM/TFM-Jordi`.
- Repositorio técnico: `/Users/jordi/GitHub/TFM/rl_uav_aerostack2`.
- Vault: `/Users/jordi/Documents/GitHub/obsdian-vault/Vault/01 - Projects/TFM - Implementation Log.md` y `/Users/jordi/Documents/GitHub/obsdian-vault/Vault/01 - Projects/TFM - RL Experiment Log.md`.
- Engram: memorias relevantes de `rl_uav_aerostack2`, especialmente Exp001-Exp007, reset por velocidad, recuperación de baja altitud y validación final del contrato de altura.

## Diagnóstico ejecutivo

La memoria ya tiene una base fuerte en los capítulos 1-4: el tono es académico, se evita prometer resultados no demostrados y el diseño del entorno está bastante bien orientado. Aun así, el documento todavía no está en estado de entrega. La estructura debe reordenarse como memoria híbrida de construcción de sistema + evaluación experimental, siguiendo el patrón de los TFM UPM de UAV/RL: introducción, estado del arte, diseño del entorno, implementación, pruebas, resultados experimentales, impacto si procede, conclusiones y anexos.

Los problemas principales son tres:

1. Hay capítulos todavía vacíos o con placeholders: resumen, pruebas, resultados, impacto, conclusiones y anexos.
2. La memoria no incorpora los cambios técnicos más recientes del repositorio y Engram: reward de progreso, `height_bounds`, `reset_ground_recovery_height`, recuperación de baja altitud, Exp006/Exp007 y el fallo controlado por reset.
3. El plan de figuras/tablas es insuficiente para una memoria UPM de este tipo: las referencias UPM usan diagramas, tablas de configuración, tablas de experimentos y curvas para sostener el argumento técnico.

## Estructura recomendada

La memoria debe tratarse como un trabajo híbrido:

- Tipo 1: construcción de un entorno software de aprendizaje por refuerzo integrado con ROS 2/Aerostack2.
- Tipo 2: evaluación experimental de la infraestructura y de los primeros entrenamientos PPO.

Estructura recomendada:

1. `Resumen / Abstract`.
2. `Introducción`.
3. `Trabajo relacionado y estado del arte`.
4. `Diseño del sistema`.
5. `Implementación`.
6. `Pruebas y validación`.
7. `Resultados experimentales y discusión`.
8. `Impacto del trabajo` si la plantilla/tutor lo exige.
9. `Conclusiones y líneas futuras`.
10. `Anexos`.

Eliminar o dejar fuera del documento principal:

- `/Users/jordi/GitHub/TFM/TFM-Jordi/secciones/03_Desarrollo.tex`: contiene plantilla residual.
- `/Users/jordi/GitHub/TFM/TFM-Jordi/secciones/08_Resultados.tex`: contiene plantilla residual y no está incluido en el main, pero conviene limpiarlo para evitar confusión.

## Revisión por capítulos

### 00_Resumen.tex

Estado: no redactado.

Acciones:

- Redactar resumen en español y abstract en inglés cuando el contenido de resultados esté estabilizado.
- Incluir problema, objetivo, solución implementada, validación y limitaciones.
- No afirmar que PPO aprende de forma robusta; la evidencia actual permite afirmar infraestructura funcional, primer éxito aislado en Exp005, y bloqueos de reset en Exp007.

### 01_Introduccion.tex

Estado: bastante avanzado, pero necesita ajuste fino.

Fortalezas:

- Sitúa bien UAV, RL, Aerostack2 y CVAR.
- Distingue infraestructura validada de comparación PID todavía no demostrada.
- Los objetivos están razonablemente alineados con la guía UPM.

Cambios necesarios:

- Reducir la carga técnica del contexto: detalles como `AS2TestEnv-v0`, observación exacta, reward y scripts pertenecen mejor al diseño/implementación.
- Ajustar el objetivo de comparación con PID: si no existe evaluación real, formularlo como base de evaluación prevista, no como objetivo ya cerrado.
- Incorporar explícitamente que el trabajo construye una infraestructura experimental para Fase 1: llegar a un punto con comandos de velocidad.

### 02_TrabajoArte.tex

Estado: buen punto de partida.

Fortalezas:

- Evita un volcado genérico de teoría.
- Posiciona Aerostack2, Gym/SB3 y simuladores.
- Conecta con literatura de UAV/RL.

Cambios necesarios:

- Añadir una subsección breve de trabajos UPM relacionados, usando los TFM/TFG de referencia como contexto académico local, sin copiarlos.
- Separar mejor tres planos: teoría RL/PPO, herramientas de entrenamiento, e integración robótica con ROS 2/Aerostack2.
- Concluir con una tabla de síntesis: enfoque, simulador/stack, tipo de acción, métrica, limitación y relación con este trabajo.

### 03_Diseno.tex

Estado: capítulo más sólido, pero desactualizado frente al repo.

Fortalezas:

- Tiene arquitectura, formulación del problema, contrato Gymnasium y reward matemático.
- Usa figuras y tablas, alineado con las referencias UPM.

Cambios necesarios:

- Actualizar la función de recompensa: el código actual incluye `progress_reward_weight * (previous_distance - current_distance)`, pero la memoria solo explica distancia + path-facing + terminales.
- Añadir la separación conceptual entre límites terminales (`height_bounds[0]`) y recuperación de reset (`reset_ground_recovery_height`). Esto es CRÍTICO porque fue una decisión técnica reciente y afecta a la validez experimental.
- Añadir una subsección de diseño del reset: fixed start, reset en vuelo, recuperación de baja altitud, rechazo de `go_to` como fallback bloqueante y fallo acotado.
- Revisar vectorización: dejar claro que la prioridad actual es single-drone estable; la vectorización está implementada/validada como infraestructura, no como aceleración experimental demostrada.

### 04_Implementacion.tex

Estado: avanzado, pero necesita sincronización con cambios recientes.

Fortalezas:

- Organización del software clara.
- Integración ROS 2/Aerostack2 bien explicada.
- Se distingue entorno, configuración, entrenamiento y validación.

Cambios necesarios:

- Añadir `configs/train_ppo_phase1_exp002.yaml` a `exp007`, no solo `train_ppo.yaml`, como evolución experimental.
- Documentar `monitor_info_keywords`, target marker RViz, checkpoints, TensorBoard y `VecMonitor` porque sostienen las métricas de resultados.
- Incorporar `scripts/validate_low_altitude_reset_real.py` y los tests de propagación/configuración como parte de la evidencia de implementación.
- Actualizar el cierre/reset con el aprendizaje reciente: AS2 puede quedar en estados como LANDING/RUNNING y el reset debe fallar de forma acotada antes que bloquear.

### 05_Pruebas.tex

Estado: solo esqueleto. Debe rehacerse completo.

Contenido recomendado:

- Estrategia de pruebas por niveles:
  - pruebas locales con mocks (`scripts/test_vectorization.py`);
  - propagación de configuración PPO (`scripts/test_ppo_config_propagation.py`);
  - validaciones reales AS2 (`validate_real_vectorized_sim.py`, `validate_randomized_hover_start_real.py`, `validate_low_altitude_reset_real.py`);
  - pruebas de entrenamiento PPO por experimentos.
- Entorno experimental: SO, conda env `rl_uav`, ROS 2, Aerostack2, AS2 Multirotor Simulator, SB3, Gymnasium, hardware si se conoce.
- Tabla de casos de prueba: objetivo, comando/script, criterio de aceptación y resultado.
- Métricas: success_rate, final_distance, terminal_reason, is_out_of_bounds, ep_len_mean, ep_rew_mean, fps, checkpoints/model_final.

### 06_Resultados.tex

Estado: solo esqueleto. Debe convertirse en capítulo central.

Contenido recomendado:

- Tabla de experimentos Exp001-Exp007:
  - objetivo/hypothesis;
  - config;
  - timesteps;
  - resultado;
  - interpretación.
- Narrativa honesta:
  - Exp001 fue trivial por target inicial.
  - Exp002 evitó éxito trivial pero reveló OOB/reset.
  - Exp003 validó fixed start.
  - Exp004 añadió target marker y métricas VecMonitor; sin éxito.
  - Exp005 obtuvo el primer éxito real (`success_rate` final ~0.0833, un episodio exitoso con `final_distance=0.1819 m`).
  - Exp006 completó 5000 timesteps pero no mejoró (`success_rate=0.0`).
  - Exp007 validó fallo acotado de reset, pero siguió bloqueado por recuperación de baja altitud.
- Incorporar la última evidencia de Engram: después del fallo de Exp007 se corrigió la separación entre OOB terminal (`height_bounds[0]`) y recuperación de reset (`reset_ground_recovery_height`), con tests que cubren z=0.2 como válido durante episodio pero recuperable antes de reset por velocidad.
- Quitar o posponer la comparación PID si no hay datos equivalentes. No se puede prometer una comparación que no existe.

### 07_Impacto.tex

Estado: esqueleto.

Contenido recomendado:

- Impacto técnico: entorno reproducible, puente Gymnasium-Aerostack2, trazabilidad de experimentos y base para futuras políticas.
- Impacto académico: facilita estudiar RL en UAV con stack robótico realista.
- Impacto social/industrial: mencionar aplicaciones solo como potenciales, sin sobredimensionar.
- Ética/seguridad: simulación antes de vuelo real, supervisión humana, límites de transferencia sim-to-real, riesgos de políticas aprendidas.
- ODS: usar pocos y justificados; evitar lista decorativa.

### 08_Conclusiones.tex

Estado: esqueleto.

Contenido recomendado:

- Revisar objetivos uno a uno, pero en prosa.
- Concluir con evidencia:
  - entorno Gymnasium/Aerostack2 implementado;
  - observación/acción/reward definidos;
  - infraestructura PPO y logging disponibles;
  - validaciones funcionales ejecutadas;
  - resultados de aprendizaje todavía limitados;
  - reset y estabilidad como principal bloqueo técnico.
- Líneas futuras:
  - estabilizar reset y recuperación de baja altitud;
  - reejecutar Exp007 tras fix;
  - evaluación PPO más larga y controlada;
  - comparación con PID solo cuando haya escenarios y métricas equivalentes;
  - vectorización tras single-drone estable;
  - posible sim-to-real progresivo.

### 09_Anexos.tex

Estado: placeholder.

Contenido recomendado:

- Tabla completa de experimentos.
- Configuraciones YAML relevantes.
- Comandos de ejecución.
- Detalles de tests/validaciones.
- Capturas RViz/TensorBoard si hay figuras demasiado extensas para el cuerpo.

## Plan de figuras y tablas recomendado

Figuras mínimas:

1. Arquitectura global PPO-Gymnasium-AS2-ROS2-simulador.
2. Diagrama de `reset()` y `step()`.
3. Geometría de observación relativa y path-facing.
4. Ciclo de reset en vuelo y recuperación de baja altitud.
5. Captura RViz con target marker.
6. Curvas TensorBoard/Monitor de Exp005 o comparativa Exp004-Exp006.

Tablas mínimas:

1. Comparativa de trabajos relacionados y herramientas.
2. Espacio de observación y acción.
3. Componentes de recompensa actualizados, incluyendo progreso.
4. Condiciones terminales y de truncado.
5. Scripts de validación y criterios de aceptación.
6. Matriz Exp001-Exp007 con resultado e interpretación.

## Orden de edición recomendado

1. Reescribir `03_Diseno.tex` para sincronizar reward, reset y altura con el repo actual.
2. Reescribir `05_Pruebas.tex` con tests reales/mocks y criterios de aceptación.
3. Reescribir `06_Resultados.tex` usando vault + Engram como fuente principal.
4. Actualizar `04_Implementacion.tex` con cambios recientes y scripts nuevos.
5. Ajustar `01_Introduccion.tex` y `02_TrabajoArte.tex` para no adelantar detalles ni prometer comparación PID.
6. Redactar `08_Conclusiones.tex` y `07_Impacto.tex`.
7. Redactar `00_Resumen.tex` y `Abstract` al final.
8. Completar anexos con configuraciones y comandos reproducibles.

## Riesgos si se entrega como está

- Capítulos 5-8 están vacíos o casi vacíos: esto incumple claramente la guía UPM.
- La función de recompensa descrita no coincide con el código actual porque falta el término de progreso.
- Falta incorporar la decisión técnica más importante de los últimos cambios: separar altura terminal de altura de recuperación de reset.
- Se menciona comparación con PID sin evidencia suficiente.
- El documento no explota todavía el material experimental disponible en el vault.
- El resumen y abstract siguen con placeholders.

## Conclusión de revisión

La dirección es buena, pero ahora hay que dejar de “rellenar capítulos” y construir el argumento de ingeniería: qué problema se formula, qué entorno se diseña, cómo se implementa, cómo se valida y qué dicen realmente los experimentos. Las referencias UPM muestran que una memoria de este tipo se sostiene con estructura, diagramas, tablas y discusión de resultados; no con teoría genérica. El siguiente paso recomendable es reescribir primero Diseño, Pruebas y Resultados porque son los capítulos que más cambian con la evidencia nueva.
