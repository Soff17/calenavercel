from django.shortcuts import render
from .models import Producto, Categoria, Marca
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def home(request):
      productos = Producto.objects.all()[6:12]
      return render(request, 'CalenaApp/index.html', {'productos': productos})

def nosotros(request):
      return render(request, 'CalenaApp/nosotros.html')

from django.http import JsonResponse
from django.db.models import Count

def autocomplete(request):
    query = request.GET.get('query')
    if query:
        productos = Producto.objects.filter(
            Q(titulo_producto__icontains=query) | Q(codigo_producto__icontains=query)
        ).values('titulo_producto', 'codigo_producto')
        
        productos_distinct = {producto['titulo_producto']: producto for producto in productos}.values()

        resultados = [{'titulo': producto['titulo_producto'], 'codigo': producto['codigo_producto']} for producto in productos_distinct]
    else:
        resultados = []

    return JsonResponse(resultados, safe=False)


def catalogo(request):
    query = request.GET.get('buscar')
    productos_catalogo = Producto.objects.all()
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    # Filtro barra navegacion
    if query:
        productos_catalogo = productos_catalogo.filter(
            Q(titulo_producto__icontains=query) |
            Q(codigo_producto__icontains=query)
        )

    # Filtro categorias
    categorias_seleccionadas = request.GET.getlist('categorias') 

    # Filtro marcas
    marcas_seleccionadas = request.GET.getlist('marcas') 

    if categorias_seleccionadas:
        productos_catalogo = productos_catalogo.filter(categoria_producto_id__in=categorias_seleccionadas)

    if marcas_seleccionadas:
        productos_catalogo = productos_catalogo.filter(marca_producto_id__in=marcas_seleccionadas)

    context = {
        'categorias': categorias,
        'marcas': marcas,
        'query': query,
        'categorias_seleccionadas': categorias_seleccionadas,
        'marcas_seleccionadas': marcas_seleccionadas
    }

    paginator = Paginator(productos_catalogo, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Agregar el valor de búsqueda a los enlaces de paginación
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_params = query_params.urlencode()

    context['query_params'] = query_params

    return render(request, 'CalenaApp/catalogo.html', {'page_obj': page_obj, **context})

def contacto(request):
      return render(request, 'CalenaApp/contacto.html')

def proveedores(request):
      return render(request, 'CalenaApp/proveedores.html')

def agregar_favorito(request, id_producto):
    quantity = request.GET.get('quantity')
    if quantity is None:
        quantity = 1  # Establecer 1 como valor predeterminado si la cantidad es None
    else:
        try:
            quantity = int(quantity)  # Convertir la cantidad a un número entero
        except ValueError:
            quantity = 1  # Si no es un número válido, establecer 1 como valor predeterminado
    
    producto = Producto.objects.get(id_producto=id_producto)
    favoritos = request.COOKIES.get('favoritos', '')
    favoritos += str(id_producto) + ':' + str(quantity) + ','
    print(favoritos)
    response_data = {'message': 'Producto agregado a favoritos'}
    response = JsonResponse(response_data)
    response.set_cookie('favoritos', favoritos)
    return response

def ver_favoritos(request):
    favoritos = request.COOKIES.get('favoritos', '').split(',')[:-1]
    productos_favoritos = {}
    for fav in favoritos:
        id_producto, quantity = fav.split(':')
        productos_favoritos[int(id_producto)] = int(quantity)
    productos_favoritos = Producto.objects.filter(id_producto__in=productos_favoritos.keys())
    return render(request, 'CalenaApp/carrito.html', {'favoritos': productos_favoritos, 'quantities': productos_favoritos.values()})


def carrito(request):
    favoritos = request.COOKIES.get('favoritos', '').split(',')
    productos_favoritos = {}
    for fav in favoritos:
        fav_parts = fav.split(':')
        if len(fav_parts) == 2:
            id_producto, quantity = fav_parts
            productos_favoritos[int(id_producto)] = int(quantity)
    
    # Obtener los productos con sus respectivas cantidades del diccionario
    productos_con_cantidad = []
    for producto_id, cantidad in productos_favoritos.items():
        try:
            producto = Producto.objects.get(id_producto=producto_id)
            productos_con_cantidad.append({'producto': producto, 'cantidad': cantidad})
        except Producto.DoesNotExist:
            pass  # Manejar el caso en que el producto no exista, si es necesario

    return render(request, 'CalenaApp/carrito.html', {'productos_con_cantidad': productos_con_cantidad})


def eliminar_favorito(request, id_producto):
    favoritos = request.COOKIES.get('favoritos', '').split(',')
    nuevos_favoritos = [fav for fav in favoritos if not fav.startswith(str(id_producto) + ':')]
    nuevos_favoritos_str = ','.join(nuevos_favoritos)

    response_data = {'message': 'Producto eliminado de favoritos'}
    response = JsonResponse(response_data)
    response.set_cookie('favoritos', nuevos_favoritos_str)
    return response

def actualizar_cantidad(request, id_producto):
    nueva_cantidad = request.GET.get('quantity')
    favoritos = request.COOKIES.get('favoritos', '').split(',')
    nuevos_favoritos = []
    for fav in favoritos:
        fav_parts = fav.split(':')
        if len(fav_parts) == 2:
            fav_id, fav_cantidad = fav_parts
            if int(fav_id) == id_producto:
                nuevos_favoritos.append(f'{id_producto}:{nueva_cantidad}')
            else:
                nuevos_favoritos.append(fav)
    nuevos_favoritos_str = ','.join(nuevos_favoritos)

    response_data = {'message': 'Cantidad actualizada'}
    response = JsonResponse(response_data)
    response.set_cookie('favoritos', nuevos_favoritos_str)
    return response

def producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    context = {'producto': producto}
    return render(request, 'CalenaApp/producto.html', context)

def cotizacion(request):
    favoritos = request.COOKIES.get('favoritos', '').split(',')
    productos_favoritos = {}
    for fav in favoritos:
        fav_parts = fav.split(':')
        if len(fav_parts) == 2:
            id_producto, quantity = fav_parts
            productos_favoritos[int(id_producto)] = int(quantity)
    
    # Obtener los productos con sus respectivas cantidades del diccionario
    productos_con_cantidad = []
    for producto_id, cantidad in productos_favoritos.items():
        try:
            producto = Producto.objects.get(id_producto=producto_id)
            productos_con_cantidad.append({'producto': producto, 'cantidad': cantidad})
        except Producto.DoesNotExist:
            pass  # Manejar el caso en que el producto no exista, si es necesario

    return render(request, 'CalenaApp/cotizacion.html', {'productos_con_cantidad': productos_con_cantidad})

def navbar(request):
      return render(request, 'CalenaApp/navbar.html')

def footer(request):
      return render(request, 'CalenaApp/footer.html')