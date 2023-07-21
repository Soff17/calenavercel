from django.urls import path

from . import views

urlpatterns = [
    path("index.html", views.home, name="home"),
    path("nosotros.html", views.nosotros, name="nosotros"),
    path("catalogo.html", views.catalogo, name="catalogo"),
    path("contacto.html", views.contacto, name="contacto"),
    path("proveedores.html", views.proveedores, name="proveedores"),
    path('agregar_favorito/<int:id_producto>/', views.agregar_favorito, name='agregar_favorito'),
    path("carrito.html", views.carrito, name="carrito"),
    path('eliminar_favorito/<int:id_producto>/', views.eliminar_favorito, name='eliminar_favorito'),
    path('actualizar_cantidad/<int:id_producto>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('producto/<str:id_producto>/', views.producto, name='producto'),
    path("cotizacion.html", views.cotizacion, name="cotizacion"),
    path("navbar.html", views.navbar, name="navbar"),
    path("footer.html", views.footer, name="footer"),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
]