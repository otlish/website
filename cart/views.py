from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer

# Get cart items for the logged-in user
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

# Add an item to the cart
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_name = request.data.get('product_name')
    size = request.data.get('size', "M")  # Get size from request, default to "M"
    price = request.data.get('price')
    quantity = request.data.get('quantity', 1)
    image= request.data.get('image')

    # Check if the same product & size already exists in cart
    existing_item = CartItem.objects.filter(user=user, product_name=product_name, size=size,image=image ).first()
    
    if existing_item:
        existing_item.quantity += int(quantity)
        existing_item.save()
        return Response({"message": "Quantity updated in cart"}, status=200)
    
    # Create new cart item
    new_cart_item = CartItem.objects.create(
        user=user, product_name=product_name, size=size, price=price, quantity=quantity,image=image
    )
    return Response({"message": "Item added to cart"}, status=201)

# Remove an item from the cart
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request ):
    item_id = request.data.get('id') 
    if not item_id:
        return Response({"error": "Item ID is required"}, status=400)
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)
