from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery import chain
from ..celery.tasks import (
    simple_task,
    long_running_task,
    error_task,
    periodic_task,
    chain_task
)

class TaskDemoView(APIView):
    """
    API View to demonstrate different types of Celery tasks
    """
    def get(self, request):
        """
        Execute different types of tasks and return their task IDs
        """
        # Execute a simple task
        simple_task_result = simple_task.delay()
        
        # Execute a long running task
        long_task_result = long_running_task.delay(5)
        
        # Execute a task that will raise an error
        error_task_result = error_task.delay()
        
        # Execute a periodic task
        periodic_task_result = periodic_task.delay()
        
        # Execute a chain of tasks
        chain_result = chain(
            chain_task.s(2),
            chain_task.s(),
            chain_task.s()
        ).delay()
        
        return Response({
            'simple_task_id': simple_task_result.id,
            'long_task_id': long_task_result.id,
            'error_task_id': error_task_result.id,
            'periodic_task_id': periodic_task_result.id,
            'chain_task_id': chain_result.id,
            'message': 'All tasks have been queued'
        }, status=status.HTTP_202_ACCEPTED) 