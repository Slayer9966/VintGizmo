from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.address import Address

@login_required
def user_addresses(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    return render(request, 'Store/Address.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        street_address = request.POST.get('street_address')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        address_type = request.POST.get('address_type')
        is_default = request.POST.get('is_default', False)

        if is_default == 'True':
            is_default = True

        new_address = Address(
            user=request.user,
            name=name,
            phone_number=phone_number,
            city=city,
            state=state,
            street_address=street_address,
            postal_code=postal_code,
            address_type=address_type,
            is_default=is_default
        )
        new_address.save()

        return redirect('AddressPage')

    return redirect('AddressPage')

@login_required
def address_detail(request, id):
    if request.method == 'GET':
        try:
            address = Address.objects.get(id=id)
            data = {
                'id': address.id,
                'name': address.name,
                'phone_number': address.phone_number,
                'street_address': address.street_address,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
            }
            return JsonResponse(data)
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Address not found'}, status=404)

@login_required
def update_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        address = get_object_or_404(Address, id=address_id)
        
        address.name = request.POST.get('name')
        address.phone_number = request.POST.get('phone_number')
        address.street_address = request.POST.get('street_address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.postal_code = request.POST.get('postal_code')
        address.save()
        
        return redirect('AddressPage')

@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect('AddressPage')