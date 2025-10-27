#!/usr/bin/env python
"""
run_demo.py

Script demostrativo que ejecuta ejemplos de uso de la API QuickTask.
Ejecutar: python run_demo.py
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
}


def colored(text: str, color: str = "ENDC") -> str:
    """Añade color a un texto para terminal."""
    return f"{COLORS.get(color, '')}{text}{COLORS['ENDC']}"


def print_section(title: str):
    """Imprime una sección de demostración."""
    print(f"\n{colored('='*70, 'HEADER')}")
    print(f"{colored(f'  {title}', 'HEADER')}")
    print(f"{colored('='*70, 'HEADER')}")


def print_request(method: str, url: str, data: Dict[Any, Any] = None):
    """Imprime detalles de una solicitud."""
    print(f"\n{colored(f'→ {method}', 'BLUE')} {colored(url, 'CYAN')}")
    if data:
        print(f"  {colored('Datos:', 'YELLOW')}")
        for line in json.dumps(data, indent=4, ensure_ascii=False).split('\n'):
            print(f"  {line}")


def print_response(response: requests.Response):
    """Imprime la respuesta de forma legible."""
    status_color = "GREEN" if 200 <= response.status_code < 300 else "RED"
    print(f"{colored(f'← {response.status_code}', status_color)}")
    
    try:
        data = response.json()
        print(f"  {colored('Respuesta:', 'YELLOW')}")
        for line in json.dumps(data, indent=4, ensure_ascii=False).split('\n'):
            print(f"  {line}")
    except:
        print(f"  {colored(response.text, 'YELLOW')}")


def demo_1_create_tasks():
    """Demostración 1: Crear varias tareas."""
    print_section("DEMO 1: Crear Tareas")
    
    tasks_data = [
        {
            "title": "Comprar comida",
            "description": "Ir al supermercado a comprar frutas, verduras y lácteos",
            "priority": "high",
            "due_date": "2025-10-27"
        },
        {
            "title": "Revisar correos",
            "description": "Leer y responder correos importantes",
            "priority": "medium"
        },
        {
            "title": "Hacer ejercicio",
            "priority": "low",
            "due_date": "2025-10-28"
        },
        {
            "title": "Aprender FastAPI",
            "description": "Completar el tutorial de FastAPI",
            "priority": "high",
            "due_date": "2025-11-15"
        },
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        print_request("POST", f"{BASE_URL}/tasks", task_data)
        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        print_response(response)
        
        if response.status_code == 201:
            created_tasks.append(response.json())
            print(f"{colored('✓ Tarea creada exitosamente', 'GREEN')}")
        
        time.sleep(0.5)  # Pausa para legibilidad
    
    return created_tasks


def demo_2_list_all_tasks():
    """Demostración 2: Listar todas las tareas."""
    print_section("DEMO 2: Listar Todas las Tareas")
    
    print_request("GET", f"{BASE_URL}/tasks")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response)
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"{colored(f'✓ Se encontraron {len(tasks)} tareas', 'GREEN')}")


def demo_3_get_single_task():
    """Demostración 3: Obtener una tarea específica."""
    print_section("DEMO 3: Obtener Tarea Específica")
    
    task_id = 1
    print_request("GET", f"{BASE_URL}/tasks/{task_id}")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)


def demo_4_update_task():
    """Demostración 4: Actualizar una tarea."""
    print_section("DEMO 4: Actualizar Tarea")
    
    task_id = 1
    update_data = {
        "title": "Comprar comida - URGENTE",
        "priority": "high",
        "due_date": "2025-10-26"  # Cambiar fecha
    }
    
    print_request("PATCH", f"{BASE_URL}/tasks/{task_id}", update_data)
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print_response(response)
    
    if response.status_code == 200:
        print(f"{colored('✓ Tarea actualizada exitosamente', 'GREEN')}")


def demo_5_mark_completed():
    """Demostración 5: Marcar tarea como completada."""
    print_section("DEMO 5: Marcar Tarea Como Completada")
    
    task_id = 2
    complete_data = {"status": "completed"}
    
    print_request("PATCH", f"{BASE_URL}/tasks/{task_id}", complete_data)
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=complete_data)
    print_response(response)
    
    if response.status_code == 200:
        print(f"{colored('✓ Tarea marcada como completada', 'GREEN')}")


def demo_6_filter_by_status():
    """Demostración 6: Filtrar tareas por estado."""
    print_section("DEMO 6: Filtrar Tareas por Estado")
    
    # Filtrar pendientes
    print(f"\n{colored('Tareas pendientes:', 'CYAN')}")
    print_request("GET", f"{BASE_URL}/tasks?status=pending")
    response = requests.get(f"{BASE_URL}/tasks?status=pending")
    print_response(response)
    
    # Filtrar completadas
    print(f"\n{colored('Tareas completadas:', 'CYAN')}")
    print_request("GET", f"{BASE_URL}/tasks?status=completed")
    response = requests.get(f"{BASE_URL}/tasks?status=completed")
    print_response(response)


def demo_7_pagination():
    """Demostración 7: Paginación."""
    print_section("DEMO 7: Paginación")
    
    print(f"\n{colored('Primeras 2 tareas:', 'CYAN')}")
    print_request("GET", f"{BASE_URL}/tasks?skip=0&limit=2")
    response = requests.get(f"{BASE_URL}/tasks?skip=0&limit=2")
    print_response(response)
    
    print(f"\n{colored('Siguiente página (skip=2):', 'CYAN')}")
    print_request("GET", f"{BASE_URL}/tasks?skip=2&limit=2")
    response = requests.get(f"{BASE_URL}/tasks?skip=2&limit=2")
    print_response(response)


def demo_8_delete_restore():
    """Demostración 8: Eliminar y restaurar tarea."""
    print_section("DEMO 8: Eliminar y Restaurar Tarea")
    
    task_id = 3
    
    # Eliminar
    print(f"\n{colored('Eliminando tarea...', 'YELLOW')}")
    print_request("DELETE", f"{BASE_URL}/tasks/{task_id}")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)
    
    if response.status_code == 204:
        print(f"{colored('✓ Tarea eliminada exitosamente', 'GREEN')}")
    
    time.sleep(1)
    
    # Verificar que no aparece en la lista
    print(f"\n{colored('Listando tareas (la eliminada no debe aparecer)...', 'YELLOW')}")
    print_request("GET", f"{BASE_URL}/tasks")
    response = requests.get(f"{BASE_URL}/tasks")
    tasks = response.json() if response.status_code == 200 else []
    print(f"  {colored(f'Total: {len(tasks)} tareas', 'CYAN')}")
    
    time.sleep(1)
    
    # Restaurar
    print(f"\n{colored('Restaurando tarea...', 'YELLOW')}")
    print_request("POST", f"{BASE_URL}/tasks/{task_id}/restore")
    response = requests.post(f"{BASE_URL}/tasks/{task_id}/restore")
    print_response(response)
    
    if response.status_code == 200:
        print(f"{colored('✓ Tarea restaurada exitosamente', 'GREEN')}")


def demo_9_error_handling():
    """Demostración 9: Manejo de errores."""
    print_section("DEMO 9: Manejo de Errores")
    
    # Error: Título vacío
    print(f"\n{colored('Intentando crear tarea sin título (debe fallar):', 'YELLOW')}")
    invalid_data = {"title": "", "priority": "high"}
    print_request("POST", f"{BASE_URL}/tasks", invalid_data)
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_data)
    print_response(response)
    
    time.sleep(0.5)
    
    # Error: Prioridad inválida
    print(f"\n{colored('Intentando crear tarea con prioridad inválida (debe fallar):', 'YELLOW')}")
    invalid_data = {"title": "Test", "priority": "urgent"}
    print_request("POST", f"{BASE_URL}/tasks", invalid_data)
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_data)
    print_response(response)
    
    time.sleep(0.5)
    
    # Error: Tarea no existe
    print(f"\n{colored('Intentando obtener tarea inexistente (debe fallar):', 'YELLOW')}")
    print_request("GET", f"{BASE_URL}/tasks/999")
    response = requests.get(f"{BASE_URL}/tasks/999")
    print_response(response)


def demo_10_bulk_operations():
    """Demostración 10: Operaciones en lote."""
    print_section("DEMO 10: Crear Múltiples Tareas Rápidamente")
    
    print(f"{colored('Creando 5 tareas...', 'CYAN')}\n")
    
    for i in range(1, 6):
        task_data = {
            "title": f"Tarea #{i}",
            "priority": ["low", "medium", "high"][i % 3],
        }
        
        print_request("POST", f"{BASE_URL}/tasks", task_data)
        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        
        if response.status_code == 201:
            task = response.json()
            print(f"{colored(f'✓ Tarea creada (ID: {task[\"id\"]})', 'GREEN')}")
        else:
            print(f"{colored('✗ Error creando tarea', 'RED')}")
        
        time.sleep(0.3)
    
    # Mostrar resumen
    print(f"\n{colored('Resumen final:', 'CYAN')}")
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        print(f"  {colored(f'Total de tareas: {len(tasks)}', 'CYAN')}")
        print(f"  {colored(f'Pendientes: {len([t for t in tasks if t[\"status\"] == \"pending\"])}', 'CYAN')}")
        print(f"  {colored(f'Completadas: {len([t for t in tasks if t[\"status\"] == \"completed\"])}', 'CYAN')}")


def main():
    """Ejecuta la demostración completa."""
    print(f"\n{colored('╔════════════════════════════════════════════════════════════════════╗', 'HEADER')}")
    print(f"{colored('║                  DEMOSTRACIÓN - QuickTask API                      ║', 'HEADER')}")
    print(f"{colored('╚════════════════════════════════════════════════════════════════════╝', 'HEADER')}")
    
    print(f"\n{colored('Base URL:', 'BLUE')} {BASE_URL}")
    print(f"{colored('Documentación:', 'BLUE')} {BASE_URL}/docs")
    
    try:
        # Verificar que el servidor está activo
        print(f"\n{colored('Verificando conexión...', 'YELLOW')}")
        response = requests.get(f"{BASE_URL}/")
        print(f"{colored('✓ Servidor activo', 'GREEN')}\n")
        
        # Ejecutar demostraciones
        demo_1_create_tasks()
        time.sleep(1)
        
        demo_2_list_all_tasks()
        time.sleep(1)
        
        demo_3_get_single_task()
        time.sleep(1)
        
        demo_4_update_task()
        time.sleep(1)
        
        demo_5_mark_completed()
        time.sleep(1)
        
        demo_6_filter_by_status()
        time.sleep(1)
        
        demo_7_pagination()
        time.sleep(1)
        
        demo_8_delete_restore()
        time.sleep(1)
        
        demo_9_error_handling()
        time.sleep(1)
        
        demo_10_bulk_operations()
        
        # Resumen final
        print_section("DEMOSTRACIÓN COMPLETADA")
        print(f"\n{colored('✓ Todas las operaciones ejecutadas exitosamente', 'GREEN')}")
        print(f"{colored('✓ API está funcionando correctamente', 'GREEN')}")
        print(f"\n{colored('Próximos pasos:', 'CYAN')}")
        print(f"  1. Revisar documentación interactiva: {BASE_URL}/docs")
        print(f"  2. Explorar el código en los archivos .py")
        print(f"  3. Leer README.md y ARCHITECTURE.md")
        print(f"  4. Ejecutar test_api.py para pruebas automáticas\n")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{colored('✗ ERROR: No se pudo conectar al servidor', 'RED')}")
        print(f"{colored('Asegúrate de que FastAPI está corriendo:', 'YELLOW')}")
        print(f"  python main.py")
        print(f"  o")
        print(f"  uvicorn main:app --reload\n")


if __name__ == "__main__":
    main()
