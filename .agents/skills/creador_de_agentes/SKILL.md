---
name: creador_de_agentes
description: >-
  Use this skill to design, define, and register custom hierarchical multi-agent teams
  using Antigravity's subagent configuration interfaces. It guides the creation of
  mainAgent and subagent systems, tools allocation, and autonomous execution policies.
---

# Creador de Agentes - Guía de Configuración Agéntica Universal

Esta habilidad proporciona el runbook oficial para estructurar y orquestar equipos de agentes y subagentes personalizados en el ecosistema Antigravity.

## Arquitectura Jerárquica de Subagentes

El sistema permite configurar agentes especializados y organizarlos bajo una jerarquía estricta.

### Configuración del Director General (mainAgent)
*   **Rol**: Orquestador principal y único punto de contacto con el usuario.
*   **Función**: Planifica flujos de trabajo, delega tareas, consolida resultados y valida las entregas.
*   **Políticas**:
    1.  Delegar tareas de bajo nivel a los especialistas.
    2.  Implementar flujos estructurados: Investigación -> Arquitectura -> Construcción -> Auditoría.
    3.  Validar y firmar entregas mediante el agente auditor antes de presentar resultados al usuario.

### Registro de Subagentes Especializados
Los subagentes se registran utilizando la herramienta `define_subagent` con sus roles, prompts de sistema y herramientas específicas:

1.  **agente-investigador**: Especialista en lectura, búsqueda y diagnósticos sin modificación de archivos.
2.  **agente-arquitecto**: Diseña planes de ejecución estructurados y lógica de negocio.
3.  **agente-constructor**: Escribe código limpio, procesa datos en masa y ejecuta comandos.
4.  **agente-auditor**: Inspector de calidad, seguridad y cumplimiento sintáctico. Rechaza o aprueba entregas.

## Uso del Creador de Agentes

Para desplegar un sistema agéntico, se deben seguir los siguientes pasos:
1.  **Definición**: Declarar los prompts del sistema y asignación de herramientas en formato estructurado.
2.  **Registro**: Invocar `define_subagent` para persistir el subagent en la sesión.
3.  **Invocación**: Utilizar `invoke_subagent` para lanzar tareas en paralelo y `send_message` para la comunicación del flujo.
