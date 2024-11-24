from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Organization, CustomUser, Role
from .forms import OrganizationForm, CustomUserForm, RoleAssignmentForm,CustomUserCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        organization_id = request.POST.get('organization')

        if not username or not email or not password or not password_confirmation or not organization_id:
            messages.error(request, 'All fields are required.')
            return redirect('signup')  # Redirect to signup page if any field is missing

        # Password validation
        if password != password_confirmation:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        try:
            # Get the selected organization, handle case when organization is not found
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            messages.error(request, 'Organization not found.')
            return redirect('signup')

        # Create the user and assign the organization
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.organization = organization
        user.save()

        # Automatically log the user in after successful signup
        login(request,user)
        return redirect('login')  # Redirect to the organizations list page after signup

    # GET request: Get all organizations to pass them to the template
    organizations = Organization.objects.all()
    return render(request, 'organization/signup.html', {'organizations': organizations})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate if both fields are provided
        if not username or not password:
            messages.error(request, 'Both fields are required.')
            return redirect('login')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)  # Correct usage of the login function
            return redirect('organization_list')  # Redirect after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'organization/login.html', {'error': 'Invalid credentials'})

    return render(request, 'organization/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def organization_list(request):
    """List all sub-organizations (for main organization admin)."""
    organizations = Organization.objects.filter(is_main=False)
    return render(request, 'organization/organization_list.html', {'organizations': organizations})

@login_required
def organization_create(request):
    """Create a new organization (main admin only)."""
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'organization/organization_form.html', {'form': form, 'form_title': 'Create Organization'})

@login_required
def organization_update(request, pk):
    """Update an organization."""
    organization = get_object_or_404(Organization, pk=pk, is_main=False)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm(instance=organization)
    return render(request, 'organization/organization_form.html', {'form': form, 'form_title': 'Edit Organization'})

@login_required
def organization_delete(request, pk):
    """Delete an organization."""
    organization = get_object_or_404(Organization, pk=pk, is_main=False)
    if request.method == 'POST':
        organization.delete()
        return redirect('organization_list')
    return render(request, 'organization/organization_confirm_delete.html', {'organization': organization})

@login_required
def organization_detail(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    users = organization.get_users()
    return render(request, 'organization/organization_detail.html', {
        'organization': organization,
        'users': users,
    })
@login_required
def user_list(request):
    """List all users in the current user's organization."""
    users = CustomUser.objects.filter(organization=request.user.organization).select_related('organization', 'role')
    return render(request, 'organization/user_list.html', {'users': users})


@login_required
def user_create(request):
    """Create a new user in the current organization."""
    if not request.user.is_superuser and request.user.organization.is_main:
        return HttpResponseForbidden("You are not allowed to add users.")

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization
            user.save()
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'organization/user_form.html', {'form': form, 'form_title': 'Add User'})

@login_required
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, organization=request.user.organization)    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)
    
    return render(request, 'organization/user_form.html', {'form': form})



@login_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, organization=request.user.organization)

    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'organization/user_confirm_delete.html', {'user': user})

@login_required
def assign_role(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, organization=request.user.organization)

    if request.method == 'POST':
        form = RoleAssignmentForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('organization_detail', pk=user.organization.id)
    else:
        form = RoleAssignmentForm(instance=user)

    return render(request, 'organization/assign_role.html', {'form': form})

