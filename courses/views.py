from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Article, PDFDocument, Coupon
from .forms import CouponForm,ArticleForm, PDFDocumentForm
from django.contrib.auth.models import User, Group


def home(request):
    articles = Article.objects.all().order_by('-created_at')[:5]  # Latest 5 articles
    pdfs = PDFDocument.objects.all().order_by('-created_at')[:5]  # Latest 5 PDFs
    if request.user.is_superuser:
        user_role = "Admin"
    # Check if user is an editor (by group)
    elif request.user.groups.filter(name='Editor').exists():
        user_role = "Editor"
    else:
        user_role = "User"
    
    data={
        'user_role':user_role,
        'articles': articles, 
        'pdfs': pdfs, 
    }

    return render(request, 'home.html', data)


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'courses/article_list.html', {'articles': articles})

def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'courses/pdf_list.html', {'pdfs': pdfs})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('home')


@login_required
def apply_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                request.user.userprofile.is_premium = True
                request.user.userprofile.save()
                messages.success(request, "Coupon applied! You now have premium access.")
                return redirect('home')
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid or expired coupon code.")
    else:
        form = CouponForm()
    return render(request, 'courses/apply_coupon.html', {'form': form})





def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_editor_or_admin(user):
    return user.groups.filter(name__in=['Admin', 'Editor']).exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def update_user_role(request, user_id, role):
    user = get_object_or_404(User, pk=user_id)
    user.groups.clear()
    group = Group.objects.get(name=role)
    user.groups.add(group)
    return redirect('manage_users')

@login_required
@user_passes_test(is_editor_or_admin)
def manage_articles(request):
    articles = Article.objects.all()
    return render(request, 'admin/manage_articles.html', {'articles': articles})

@login_required
@user_passes_test(is_editor_or_admin)
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_articles')
    else:
        form = ArticleForm()
    return render(request, 'admin/add_article.html', {'form': form})

@login_required
@user_passes_test(is_editor_or_admin)
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('manage_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'admin/edit_article.html', {'form': form})

@login_required
@user_passes_test(is_editor_or_admin)
def manage_pdfs(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'adimn/manage_pdfs.html', {'pdfs': pdfs})

@login_required
@user_passes_test(is_editor_or_admin)
def add_pdf(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_pdfs')
    else:
        form = PDFDocumentForm()
    return render(request, 'admin/add_pdf.html', {'form': form})

@login_required
@user_passes_test(is_editor_or_admin)
def edit_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, pk=pdf_id)
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            return redirect('manage_pdfs')
    else:
        form = PDFDocumentForm(instance=pdf)
    return render(request, 'admin/edit_pdf.html', {'form': form})


def view_article(request, article_id):
    # Retrieve the article by ID or 404 if not found
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'courses/view_article.html', {'article': article})


def pdf_view(request, pdf_id):
    current_host = 'http://'+request.get_host()
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    data={
        'pdf':pdf,
        'current_host':current_host,
    }
    return render(request, 'courses/pdf_viewer.html', data)
