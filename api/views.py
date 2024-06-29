from django.shortcuts import render

from rest_framework.views import Response

from rest_framework.views import APIView

from api.serializers import UserSerializer,IncomeSerializer,ExpenseSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

from api.permissions import OwnerOnly

from budget.models import Income,Expense

from django.utils import timezone

from django.db.models import Sum

# Create your views here.

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class IncomeViewSet(ModelViewSet):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(user_object=request.user)

        serializer_instance=IncomeSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self,serializer):

        serializer.save(user_object=self.request.user)

class ExpenseViewSet(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Expense.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)  

    def perform_create(self,serializer):

        serializer.save(user_object=self.request.user) 

class IncomeSummaryView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_income=Income.objects.filter(
                     user_object=request.user,

                     created_date__month=current_month,

                     created_date__year=current_year
                   )
        
        income_total=all_income.values("amount").aggregate(total=Sum("amount"))["total"]

        category_summary=all_income.values("category").annotate(total=Sum("amount"))

        data={
            "income total":income_total,

            "catagory total":category_summary
        }

        return Response(data=data)
    
class ExpenseSummaryView(APIView):  

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expense=Expense.objects.filter(
                     user_object=request.user,

                     created_date__month=current_month,

                     created_date__year=current_year
                   )
        
        expense_total=all_expense.values("amount").aggregate(total=Sum("amount"))["total"]

        category_summary=all_expense.values("category").annotate(total=Sum("amount"))

        priority_summary=all_expense.values("priority").annotate(total=Sum("amount"))

        data={
            "expense total":expense_total,
            "category total":category_summary,
            "priority total":priority_summary
        }

        return Response(data=data)
      



