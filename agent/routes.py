from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from agent import agent
from models import user_data, agent_tasks
from datetime import datetime

# Decorator to check if the current user is an agent
def agent_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.profession != 'Agent':
            flash('Access denied: You must be logged in as an Agent to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__  # Preserve original function name
    return decorated_function

@agent.route('/dashboard')
@agent_required
def dashboard():
    """Agent dashboard showing assigned tasks."""
    # Get user name from user_data dictionary
    user_info = user_data.get(current_user.id, {})
    
    # Get agent's district (used to filter tasks)
    agent_district = user_info.get('district', '')
    
    # Get agent's tasks
    tasks = agent_tasks.get(current_user.id, [])
    if not tasks:
        # For demo: Generate some example tasks if none exist
        example_tasks = [
            {
                'task_id': f'TASK-{datetime.now().strftime("%Y%m%d")}-001',
                'insurance_id': 'INS-12345',
                'location': agent_district or 'District A',
                'farmer_name': 'Test Farmer 1',
                'phone_no': '9876543210',
                'status': 'pending',
                'created_at': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'task_id': f'TASK-{datetime.now().strftime("%Y%m%d")}-002',
                'insurance_id': 'INS-67890',
                'location': agent_district or 'District A',
                'farmer_name': 'Test Farmer 2',
                'phone_no': '9876543211',
                'status': 'pending',
                'created_at': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        agent_tasks[current_user.id] = example_tasks
        tasks = example_tasks
    
    return render_template('agent/dashboard.html', 
                          user_name=user_info.get('name', 'Agent'),
                          tasks=tasks,
                          title='Agent Dashboard')

@agent.route('/submit-task/<task_id>', methods=['POST'])
@agent_required
def submit_task(task_id):
    """Submit a completed task with uploaded images."""
    tasks = agent_tasks.get(current_user.id, [])
    
    # Find the task by ID
    task_index = None
    for i, task in enumerate(tasks):
        if task['task_id'] == task_id:
            task_index = i
            break
    
    if task_index is None:
        return jsonify({'success': False, 'error': 'Task not found'})
    
    # Check if images were uploaded
    if 'crop_images' not in request.files:
        return jsonify({'success': False, 'error': 'No images uploaded'})
    
    files = request.files.getlist('crop_images')
    if not files or files[0].filename == '':
        return jsonify({'success': False, 'error': 'No images selected'})
    
    # Process the uploaded files (placeholder)
    upload_folder = f'uploads/tasks/{task_id}'
    # os.makedirs(upload_folder, exist_ok=True)
    
    # For demo: Just update the task status
    tasks[task_index]['status'] = 'completed'
    tasks[task_index]['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({'success': True, 'message': 'Task submitted successfully'})

@agent.route('/verify-claim/<claim_id>')
@agent_required
def verify_claim(claim_id):
    """View and verify an insurance claim."""
    # Placeholder for claim verification functionality
    return render_template('agent/verify_claim.html',
                          claim_id=claim_id,
                          title='Verify Claim')

@agent.route('/completed-tasks')
@agent_required
def completed_tasks():
    """View history of completed tasks."""
    tasks = agent_tasks.get(current_user.id, [])
    completed = [task for task in tasks if task.get('status') == 'completed']
    
    return render_template('agent/completed_tasks.html',
                          tasks=completed,
                          title='Completed Tasks')