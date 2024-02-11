from django.shortcuts import render
from payment.models import InvestmentPlan, Interest

def dashboard_view(request):
    # Retrieve all investments for the current user
    user_investments = Interest.objects.filter(investment_plan__user=request.user)

    # Additional details from the InvestmentPlan model for user's investments
    investment_details = []
    for investment in user_investments:
        investment_plan = investment.investment_plan
        details = {
            'plan_type': investment_plan.get_plan_type_display(),
            'roi_percentage': investment_plan.roi_percentage,
            'affine_space_duration': investment_plan.affine_space_duration,
            'investment_duration': investment_plan.investment_duration,
            'amount': investment_plan.amount,
            'start_date': investment.start_date,
            'end_date': investment.end_date,
            'percentage_return': investment.percentage_return,
            'monetary_return': investment.monetary_return,
            'total_amount': investment.total_amount,
        }
        investment_details.append(details)

    # Retrieve all InvestmentPlan details for the current user
    all_investment_plans = InvestmentPlan.objects.filter(user=request.user)
    
    # Additional details from the InvestmentPlan model for all plans
    all_investment_details = []
    for plan in all_investment_plans:
        plan_details = {
            'plan_type': plan.get_plan_type_display(),
            'roi_percentage': plan.roi_percentage,
            'affine_space_duration': plan.affine_space_duration,
            'investment_duration': plan.investment_duration,
            'amount': plan.amount,
            # Add more fields as needed
        }
        all_investment_details.append(plan_details)

    context = {
        'investment_details': investment_details,
        'all_investment_details': all_investment_details,
    }
    return render(request, 'dashboard/dashboard.html', context)


def investment_view(request):
    # Retrieve all investments for the current user
    user_investments = Interest.objects.filter(investment_plan__user=request.user)

    # Additional details from the InvestmentPlan model
    investment_details = []
    for investment in user_investments:
        investment_plan = investment.investment_plan
        details = {
            'plan_type': investment_plan.get_plan_type_display(),
            'roi_percentage': investment_plan.roi_percentage,
            'affine_space_duration': investment_plan.affine_space_duration,
            'investment_duration': investment_plan.investment_duration,
            'amount': investment_plan.amount,
            'start_date': investment.start_date,
            'end_date': investment.end_date,
            'percentage_return': investment.percentage_return,
            'monetary_return': investment.monetary_return,
            'total_amount': investment.total_amount,
        }
        investment_details.append(details)

    context = {
        'investment_details': investment_details,
    }

    return render(request, 'dashboard/investments.html', context)
