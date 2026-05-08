import csv
from datetime import timedelta
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import ExpenseForm, ProfileForm, SignUpForm
from .models import Achievement, Expense, UserProfile, monthly_total

PALETTE = ['#8CC8FF', '#A6D672', '#FFC6C6', '#9B8CFF', '#FFD166', '#80ED99', '#FF9F9F']


def splash(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'splash.html')


def onboarding(request):
    return render(request, 'onboarding.html')


def ensure_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if not profile.achievements.exists():
        Achievement.objects.bulk_create([
            Achievement(profile=profile, title='First Budget', description='Created your first monthly money plan.', icon='target'),
            Achievement(profile=profile, title='Streak Starter', description='Tracked expenses for a full week.', icon='flame'),
            Achievement(profile=profile, title='Smart Saver', description='Reached 40% of the savings goal.', icon='sparkles'),
        ])
    return profile


def seed_demo_expenses(user):
    if user.expenses.exists():
        return
    today = timezone.localdate()
    samples = [
        ('Pizza night', 620, 'Food', 0),
        ('Metro card recharge', 300, 'Travel', 1),
        ('Netflix subscription', 649, 'Entertainment', 3),
        ('Grocery basket', 1340, 'Food', 5),
        ('Course notebook', 480, 'Education', 8),
        ('Coffee meet', 260, 'Food', 12),
        ('Cab to office', 540, 'Travel', 15),
    ]
    Expense.objects.bulk_create([
        Expense(user=user, title=title, amount=amount, category=category, date=today - timedelta(days=days), notes='Demo transaction')
        for title, amount, category, days in samples
    ])


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            ensure_profile(user)
            seed_demo_expenses(user)
            login(request, user)
            messages.success(request, 'Welcome aboard. Your smart wallet is ready.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def chart_payload(user):
    category_rows = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount')).order_by('category')
    labels = [row['category'] for row in category_rows] or ['Food', 'Travel', 'Entertainment']
    values = [float(row['total']) for row in category_rows] or [620, 540, 649]
    today = timezone.localdate()
    line_labels = []
    line_values = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        line_labels.append(day.strftime('%d %b'))
        total = Expense.objects.filter(user=user, date=day).aggregate(total=Sum('amount'))['total'] or 0
        line_values.append(float(total))
    return {
        'category_labels': labels,
        'category_values': values,
        'line_labels': line_labels,
        'line_values': line_values,
        'palette': PALETTE,
    }


@login_required
def dashboard(request):
    profile = ensure_profile(request.user)
    seed_demo_expenses(request.user)
    total = monthly_total(request.user)
    budget_progress = min(100, round((float(total) / float(profile.monthly_budget)) * 100)) if profile.monthly_budget else 0
    expenses = Expense.objects.filter(user=request.user)[:5]
    context = {
        'profile': profile,
        'total_expense': total,
        'budget_progress': budget_progress,
        'recent_expenses': expenses,
        'charts': chart_payload(request.user),
    }
    return render(request, 'dashboard.html', context)


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses.html', {'expenses': expenses, 'form': ExpenseForm()})


@login_required
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Expense added with smart category tracking.')
        return redirect('expenses')
    return render(request, 'expense_form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Expense updated.')
        return redirect('expenses')
    return render(request, 'expense_form.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted.')
    return redirect('expenses')


@login_required
def analytics(request):
    return render(request, 'analytics.html', {'charts': chart_payload(request.user)})


@login_required
def gamification(request):
    profile = ensure_profile(request.user)
    return render(request, 'gamification.html', {'profile': profile, 'achievements': profile.achievements.all()})


@login_required
def reports(request):
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'reports.html', {'expenses': expenses[:10], 'total': total})


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="smart-expense-report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Notes'])
    for expense in Expense.objects.filter(user=request.user):
        writer.writerow([expense.title, expense.amount, expense.category, expense.date, expense.notes])
    return response


@login_required
def export_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = [
        Paragraph('Smart Expense Tracker Report', styles['Title']),
        Spacer(1, 16),
        Paragraph(f'Generated for {request.user.username} on {timezone.localdate().strftime("%d %b %Y")}', styles['BodyText']),
        Spacer(1, 18),
    ]
    data = [['Title', 'Amount', 'Category', 'Date']]
    for expense in Expense.objects.filter(user=request.user)[:35]:
        data.append([expense.title, f'Rs. {expense.amount}', expense.category, expense.date.strftime('%d %b %Y')])
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8CC8FF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1B1B1B')),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#DDDDDD')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F6F2')]),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='smart-expense-report.pdf')


@login_required
def profile(request):
    profile_obj = ensure_profile(request.user)
    form = ProfileForm(request.POST or None, instance=profile_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile preferences saved.')
        return redirect('profile')
    return render(request, 'profile.html', {'form': form, 'profile': profile_obj, 'achievements': profile_obj.achievements.all()})
