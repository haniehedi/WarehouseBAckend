from attr import Factory
# from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from products.models import Ware, Warehouse, Factor
from products.serializers import WarehouseSerializer, WareSerializer, FactorSerializer
from rest_framework import status
from rest_framework.response import Response
from .permissions import WarehousePermissions

class WareModelViewSet(ModelViewSet):
    serializer_class = WareSerializer
    permission_classes = [IsAuthenticated, WarehousePermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Ware.objects.all()
        elif self.request.user.role == 'staff':
            return Ware.objects.filter(user=self.request.user)
        return Ware.objects.none()

class WarehouseModelViewSet(ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Warehouse.objects.all()
        elif self.request.user.role == 'staff':
            return Warehouse.objects.filter(user=self.request.user)
        return Warehouse.objects.none()

class FactorModelViewSet(ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = FactorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['type'] == 'input':
            quantity = serializer.validated_data['quantity']
            purchase_price = serializer.validated_data['purchase_price']

            factor = Factor(
                user=serializer.validated_data.get('user'),
                ware=serializer.validated_data['ware'],
                quantity=quantity,
                purchase_price=purchase_price,
                total_cost=quantity * purchase_price,
                type='input'
            )

            try:
                factor.save()
                return Response(FactorSerializer(factor).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        elif serializer.validated_data['type'] == 'output':
            ware = serializer.validated_data['ware']
            req_quantity = int(request.data['quantity'])
            total_cost = 0
            factors_to_update = []
            if ware.cost_method == Ware.fifo:
                factors = Factor.objects.filter(ware=ware, type='input').order_by('created_at')
                for factor in factors:
                    if factor.quantity > 0:
                        if factor.quantity >= req_quantity:
                            total_cost += req_quantity * factor.purchase_price
                            factor.quantity -= req_quantity
                            factors_to_update.append(factor)
                            req_quantity = 0
                        else:
                            total_cost += factor.quantity * factor.purchase_price
                            req_quantity -= factor.quantity
                            factor.quantity = 0
                            factors_to_update.append(factor)

            elif ware.cost_method == 'weighted_mean':
                total_quantity = sum(f.quantity for f in Factor.objects.filter(ware=ware, type='input'))
                total_value = sum(f.quantity * f.purchase_price for f in Factor.objects.filter(ware=ware, type='input'))
                if total_quantity > 0:
                    average_cost = total_value / total_quantity
                else:
                    average_cost = 0
                total_cost = req_quantity * average_cost

                factors = Factor.objects.filter(ware=ware, type='input').order_by('created_at')
                for factor in factors:
                    if factor.quantity > 0:
                        if factor.quantity >= req_quantity:
                            factor.quantity -= req_quantity
                            factors_to_update.append(factor)
                            req_quantity = 0
                        else:
                            req_quantity -= factor.quantity
                            factor.quantity = 0
                            factors_to_update.append(factor)
            for factor in factors_to_update:
                factor.save()

            factor_data = {
                'ware': ware.id,
                'quantity': int(request.data['quantity']),
                'type': 'output',
                'total_cost': total_cost,
                'purchase_price': 0,
                'user': request.user.id
            }

            output_serializer = FactorSerializer(data=factor_data)
            output_serializer.is_valid(raise_exception=True)
            self.perform_create(output_serializer)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)


        return Response({'detail': 'Invalid factor type.'}, status=status.HTTP_400_BAD_REQUEST)
