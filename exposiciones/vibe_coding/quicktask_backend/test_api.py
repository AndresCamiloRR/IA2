"""
test_api.py

Script de prueba para validar los endpoints de la API QuickTask.
Ejecutar: python test_api.py
(Requiere que el servidor FastAPI esté corriendo en http://localhost:8000)
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """
    Imprime el resultado de una solicitud HTTP de forma formateada.
    
    Args:
        title (str): Título del resultado.
        response (requests.Response): Respuesta HTTP.
    """
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_1_create_task():
    """Prueba 1: Crear una tarea."""
    print("\n[TEST 1] Crear una nueva tarea")
    
    payload = {
        "title": "Comprar leche",
        "description": "Leche entera de 1L en el supermercado",
        "priority": "high",
        "due_date": "2025-10-30"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Crear tarea)", response)
    
    return response.json() if response.status_code == 201 else None


def test_2_create_second_task():
    """Prueba 2: Crear una segunda tarea."""
    print("\n[TEST 2] Crear otra tarea (sin descripción)")
    
    payload = {
        "title": "Hacer ejercicio",
        "priority": "medium",
        "due_date": "2025-10-27"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Crear segunda tarea)", response)
    
    return response.json() if response.status_code == 201 else None


def test_3_create_third_task():
    """Prueba 3: Crear una tercera tarea."""
    print("\n[TEST 3] Crear tercera tarea (solo título)")
    
    payload = {
        "title": "Revisar correos"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Crear tercera tarea)", response)
    
    return response.json() if response.status_code == 201 else None


def test_4_list_all_tasks():
    """Prueba 4: Listar todas las tareas."""
    print("\n[TEST 4] Listar todas las tareas")
    
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("✓ GET /tasks (Listar todas)", response)


def test_5_get_single_task(task_id: int = 1):
    """Prueba 5: Obtener una tarea específica."""
    print(f"\n[TEST 5] Obtener tarea con ID {task_id}")
    
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(f"✓ GET /tasks/{task_id} (Obtener tarea específica)", response)


def test_6_update_task(task_id: int = 1):
    """Prueba 6: Actualizar una tarea."""
    print(f"\n[TEST 6] Actualizar tarea con ID {task_id}")
    
    payload = {
        "title": "Comprar leche de soya",
        "priority": "low",
        "due_date": "2025-11-05"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    print_response(f"✓ PUT /tasks/{task_id} (Actualizar tarea)", response)


def test_7_mark_completed(task_id: int = 2):
    """Prueba 7: Marcar una tarea como completada."""
    print(f"\n[TEST 7] Marcar tarea {task_id} como completada")
    
    payload = {
        "status": "completed"
    }
    
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=payload)
    print_response(f"✓ PATCH /tasks/{task_id} (Marcar completada)", response)


def test_8_filter_pending():
    """Prueba 8: Filtrar solo tareas pendientes."""
    print("\n[TEST 8] Filtrar tareas pendientes")
    
    response = requests.get(f"{BASE_URL}/tasks?status=pending")
    print_response("✓ GET /tasks?status=pending (Filtrar pendientes)", response)


def test_9_filter_completed():
    """Prueba 9: Filtrar solo tareas completadas."""
    print("\n[TEST 9] Filtrar tareas completadas")
    
    response = requests.get(f"{BASE_URL}/tasks?status=completed")
    print_response("✓ GET /tasks?status=completed (Filtrar completadas)", response)


def test_10_pagination():
    """Prueba 10: Paginación."""
    print("\n[TEST 10] Prueba de paginación")
    
    response = requests.get(f"{BASE_URL}/tasks?skip=0&limit=2")
    print_response("✓ GET /tasks?skip=0&limit=2 (Paginación)", response)


def test_11_delete_task(task_id: int = 3):
    """Prueba 11: Eliminar una tarea."""
    print(f"\n[TEST 11] Eliminar tarea con ID {task_id}")
    
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print_response(f"✓ DELETE /tasks/{task_id} (Eliminar tarea)", response)


def test_12_get_deleted_task(task_id: int = 3):
    """Prueba 12: Intentar obtener tarea eliminada."""
    print(f"\n[TEST 12] Intentar obtener tarea eliminada (ID {task_id})")
    
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(f"✓ GET /tasks/{task_id} (Tarea no encontrada)", response)


def test_13_restore_task(task_id: int = 3):
    """Prueba 13: Restaurar una tarea eliminada."""
    print(f"\n[TEST 13] Restaurar tarea con ID {task_id}")
    
    response = requests.post(f"{BASE_URL}/tasks/{task_id}/restore")
    print_response(f"✓ POST /tasks/{task_id}/restore (Restaurar tarea)", response)


def test_14_invalid_data():
    """Prueba 14: Enviar datos inválidos."""
    print("\n[TEST 14] Enviar título vacío (debe fallar)")
    
    payload = {
        "title": "",
        "priority": "high"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Validación fallida)", response)


def test_15_invalid_priority():
    """Prueba 15: Prioridad inválida."""
    print("\n[TEST 15] Enviar prioridad inválida (debe fallar)")
    
    payload = {
        "title": "Tarea de prueba",
        "priority": "urgent"  # Valor inválido
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Prioridad inválida)", response)


def test_16_invalid_date():
    """Prueba 16: Fecha inválida."""
    print("\n[TEST 16] Enviar fecha inválida (debe fallar)")
    
    payload = {
        "title": "Tarea de prueba",
        "due_date": "30-10-2025"  # Formato incorrecto
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print_response("✓ POST /tasks (Fecha inválida)", response)


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*60)
    print("  SUITE DE PRUEBAS - QuickTask API")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("="*60)
    
    try:
        # Pruebas de creación
        task1 = test_1_create_task()
        task2 = test_2_create_second_task()
        task3 = test_3_create_third_task()
        
        # Pruebas de lectura
        test_4_list_all_tasks()
        test_5_get_single_task(1)
        
        # Pruebas de actualización
        test_6_update_task(1)
        test_7_mark_completed(2)
        
        # Pruebas de filtrado
        test_8_filter_pending()
        test_9_filter_completed()
        test_10_pagination()
        
        # Pruebas de eliminación y restauración
        test_11_delete_task(3)
        test_12_get_deleted_task(3)
        test_13_restore_task(3)
        
        # Pruebas de validación
        test_14_invalid_data()
        test_15_invalid_priority()
        test_16_invalid_date()
        
        print("\n" + "="*60)
        print("  ✓ SUITE DE PRUEBAS COMPLETADA")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "!"*60)
        print("  ✗ ERROR: No se pudo conectar al servidor.")
        print("  Asegúrate de que FastAPI está corriendo en:")
        print(f"  {BASE_URL}")
        print("!"*60 + "\n")


if __name__ == "__main__":
    main()
