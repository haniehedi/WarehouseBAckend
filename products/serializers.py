from rest_framework import serializers
from products.models import Ware, Warehouse, Factor

class WareSerializer(serializers.ModelSerializer):
    user_created = serializers.ReadOnlyField(source='user.id')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    class Meta:
        model = Ware
        fields = ['id', 'name', 'user_created', 'warehouse', 'warehouse_name', 'cost_method']
        read_only_fields = ('id',)


class WarehouseSerializer(serializers.ModelSerializer):
    wares = WareSerializer(many=True, read_only=True)
    user_created = serializers.ReadOnlyField(source='user.id')
    user_created_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Warehouse
        fields = ['id','name', 'user_created_name','wares' ,'user_created']

        read_only_fields = ('id',)

    def get_wares(self, obj):
        serializer = WareSerializer(obj.wares.all(), many=True)
        return serializer.data

class FactorSerializer(serializers.ModelSerializer):
    ware_cost_method = serializers.ReadOnlyField(source='ware.cost_method')
    class Meta:
        model = Factor
        fields = ['id', 'user', 'ware', 'quantity', 'purchase_price', 'created_at',
                  'type', 'total_cost', 'ware_cost_method']
