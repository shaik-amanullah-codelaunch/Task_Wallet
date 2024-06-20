from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, user_details

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        # Capture form data using request.POST.get()
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(f"Signup attempt with email: {email} name: {username} password: {password} confirm_password: {confirm_password}")

        # Validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            # Create user in Django ORM
            user = user_details.objects.create(username=username, email=email, password=password)
            return redirect('login_page')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'signup.html')
    
    # For GET request, just render the signup page
    return render(request, 'signup.html')
 

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                # Check if user exists
                user = user_details.objects.get(email=email)
                print(f"User found: {user}")

                # Authenticate user using Django's authenticate function
                user = authenticate(request, username=email, password=password)

                if user:
                    # If user is authenticated, log them in using login function
                    login(request, user)
                    print(f"User {user.username} logged in successfully.")

                    # Redirect to the home page or another page
                    return redirect('tasks')  # Replace 'tasks' with your post-login URL

                else:
                    messages.error(request, 'Invalid email or password.')
                    print("Authentication failed: Invalid email or password.")

            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                print("User not found.")

            except Exception as e:
                messages.error(request, f"An error occurred during login: {e}")
                print("Exception:", e)

        else:
            messages.error(request, 'Both email and password are required.')

    # Render the login page for GET request
    return render(request, 'login_page.html')


@login_required
def list_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('deadline', 'amount')
    return render(request, 'list_tasks.html', {'tasks': tasks})

@login_required
def mark_task_done(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('tasks')

@login_required
def abort_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('tasks')



@login_required
def create_task(request):
    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        deadline = request.POST['deadline']
        
        task = Task(
            user=request.user,
            description=description,
            amount=amount,
            deadline=deadline
        )
        task.save()
        return redirect('tasks')
    
    return render(request, 'create_task.html')
