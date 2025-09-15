from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login
from .models import Task
from .forms import TaskForm, RegisterForm

def home(request):
    return render(request, "home.html")

def register_page(request):
    """Simple registration page (session-auth flow, not JWT)."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()          # hashes password, creates user
            login(request, user)        # log them in immediately (session cookie)
            messages.success(request, "Welcome! Your account was created.")
            return redirect("tasks_list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

@login_required
def tasks_list(request):
    """
    Show ONLY the logged-in user's tasks.
    Supports ?search=... and ?ordering=(created_at|updated_at|due_date or -prefix)
    Paginates with ?page=1,2,...
    """
    qs = Task.objects.filter(owner=request.user)  # only my tasks

    # Filter by search term (title or description contains)
    search = request.GET.get("search")
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    # Ordering whitelist
    ordering = request.GET.get("ordering")
    allowed = {"created_at", "-created_at", "updated_at", "-updated_at", "due_date", "-due_date"}
    if ordering in allowed:
        qs = qs.order_by(ordering)
    else:
        qs = qs.order_by("-created_at")  # default newest first

    # Paginate (10 per page)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")  # ex: /tasks/?page=2
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks_list.html", {
        "page_obj": page_obj,  # contains .object_list (the items) and pagination helpers
        "search": search or "",
        "ordering": ordering or "-created_at",
    })

@login_required
def task_create(request):
    """Create a new task for the current user."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # don't save yet, we need to set owner
            task.owner = request.user
            task.save()
            messages.success(request, "Task created.")
            return redirect("tasks_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form, "title": "Create Task"})

@login_required
def task_update(request, pk):
    """Edit an existing task (only if it belongs to the current user)."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect("tasks_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_form.html", {"form": form, "title": "Edit Task"})

@login_required
def task_delete(request, pk):
    """Confirm + delete a task (only if mine)."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.info(request, "Task deleted.")
        return redirect("tasks_list")
    return render(request, "confirm_delete.html", {"task": task})

@login_required
def task_toggle_complete(request, pk):
    """Quick toggle completed/uncompleted; use POST for safety (CSRF-protected)."""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
        messages.success(request, "Task status toggled.")
    return redirect("tasks_list")
