from django.shortcuts import render, get_object_or_404
from .models import *

from django.http import HttpResponse
from django.shortcuts import render

from marketplace.models import *


def index(request):
    cliente = Cliente.objects.get(nombre='Rafael Piedra')

    return render(request, 'home.html',
                  context={"productos": Producto.objects.all(), "categorias": Categoria.objects.all(),
                           "productos_destacados": cliente.obtener_productos_destacados_de_cliente()})


def metricas(request, vendedor_id):
    anio = 2023
    mes = 12

    vendedor = get_object_or_404(Vendedor, pk=vendedor_id)

    reporte = vendedor.generar_reporte(anio, mes)

    recomendaciones = reporte.obtener_recomendaciones()

    numero_ventas = reporte.obtener_metrica(TipoDeMetrica.NUMERO_DE_VENTAS).valor
    ingresos = reporte.obtener_metrica(TipoDeMetrica.INGRESOS).valor
    costos = reporte.obtener_metrica(TipoDeMetrica.COSTOS).valor
    beneficio_venta = reporte.obtener_metrica(TipoDeMetrica.BENEFICIO_POR_VENTA).valor

    nv_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.INGRESOS)
    cs_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.COSTOS)
    bv_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.INGRESOS)
    cs_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.COSTOS)
    bv_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.INGRESOS)
    cs_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.COSTOS)
    bv_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS).valor
    is_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.INGRESOS).valor
    cs_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.COSTOS).valor
    bv_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.BENEFICIO_POR_VENTA).valor

    context = {
        'recomendaciones': recomendaciones,
        'numero_ventas': numero_ventas,
        'ingresos': ingresos,
        'costos': costos,
        'beneficio_venta': beneficio_venta,
        'nv_porcentaje': nv_porcentaje,
        'is_porcentaje': is_porcentaje,
        'cs_porcentaje': cs_porcentaje,
        'bv_porcentaje': bv_porcentaje,
        'nv_comparacion_meta': nv_comparacion_meta,
        'is_comparacion_meta': is_comparacion_meta,
        'cs_comparacion_meta': cs_comparacion_meta,
        'bv_comparacion_meta': bv_comparacion_meta,
        'nv_comparacion_mes_anterior': nv_comparacion_mes_anterior,
        'is_comparacion_mes_anterior': is_comparacion_mes_anterior,
        'cs_comparacion_mes_anterior': cs_comparacion_mes_anterior,
        'bv_comparacion_mes_anterior': bv_comparacion_mes_anterior,
        'nv_valor_mes_anterior': nv_valor_mes_anterior,
        'is_valor_mes_anterior': is_valor_mes_anterior,
        'cs_valor_mes_anterior': cs_valor_mes_anterior,
        'bv_valor_mes_anterior': bv_valor_mes_anterior
    }

    return render(request, 'metrica.html', context)


def feedback(request):
    causas = dict()
    porcentajes_calculados = list()
    calificaciones_recibidas = list()
    estrellas = [1, 2, 3, 4, 5]
    num_estrella_calculada = 0
    if request.method == 'POST':
        if request.POST.get('opcion') == 'Servicio':
            servicio = Servicio.objects.filter(vendedor_id=1).first()
            calificaciones_recibidas = Calificacion.objects.filter(id_servicio_id=servicio.id)
            porcentajes_calculados = servicio.obtener_porcentajes_de_calificaciones()
            causas_dict = servicio.obtener_causas_de_cada_estrella(calificaciones_recibidas)
            causas = list(causas_dict.values())
            print(causas)
            num_estrella_calculada = servicio.obtener_promedio_general_del_servicio()
            return render(request, 'feedback.html', {
                'causas': causas,
                'porcentajes_calculados': porcentajes_calculados,
                'num_estrella_calculada': num_estrella_calculada,
                'estrellas': estrellas,
                'nombre': request.POST.get('opcion')
            })
        else:
            productos = Producto.objects.filter(vendedor_id=1).all()
            for producto in productos:
                if request.POST.get('nombre_producto') is not None and request.POST.get(
                        'nombre_producto') == producto.nombre:
                    producto = Producto.objects.filter(nombre=request.POST.get('nombre_producto')).first()
                    calificaciones_recibidas = Calificacion.objects.filter(id_producto_id=producto.id)
                    porcentajes_calculados = producto.obtener_porcentajes_de_calificaciones()
                    causas_dict = producto.obtener_causas_de_cada_estrella(calificaciones_recibidas)
                    causas = list(causas_dict.values())
                    print(causas)
                    num_estrella_calculada = producto.obtener_promedio_general_del_producto()
                    return render(request, 'feedback.html', {
                        'causas': causas,
                        'porcentajes_calculados': porcentajes_calculados,
                        'num_estrella_calculada': num_estrella_calculada,
                        'estrellas': estrellas,
                        'nombre': request.POST.get('nombre_producto')
                    })
    else:
        return render(request, 'feedback.html')


def buscar_producto(request):
    productos = []
    if request.method == 'POST':
        producto_nombre = request.POST.get('producto', '')
        productos = Producto.objects.filter(nombre__icontains=producto_nombre).order_by('-promocion')
    return render(request, 'producto.html', {'productos': productos})


def seguimiento_interno(request):
    # Obtener todos los pedidos de la base de datos
    pedidos = Pedido.objects.all()

    # Iterar sobre cada pedido y llamar al método cambiar_estado
    for pedido in pedidos:
        pedido.cambiar_estado()

    # Total pedidos del vendedor 1
    total_pedidos_vendedor = Pedido.total_pedidos_vendedor(1)

    # Obtener los totales y conteos por etapa
    total_pedidos_precompra, precompra_atrasados, precompra_a_tiempo, precompra_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.PRECOMPRA, 1)
    total_pedidos_reserva, reserva_atrasados, reserva_a_tiempo, reserva_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.RESERVA, 1)
    total_pedidos_listo_para_entregar, listo_para_entregar_atrasados, listo_para_entregar_a_tiempo, listo_para_entregar_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.LISTO_PARA_ENTREGAR, 1)

    context = {
        'total_pedidos_vendedor': total_pedidos_vendedor,
        'total_pedidos_precompra': total_pedidos_precompra,
        'total_pedidos_reserva': total_pedidos_reserva,
        'total_pedidos_listo_para_entregar': total_pedidos_listo_para_entregar,
        'precompra_a_tiempo': precompra_a_tiempo,
        'precompra_atrasados': precompra_atrasados,
        'precompra_cancelados': precompra_cancelados,
        'reserva_a_tiempo': reserva_a_tiempo,
        'reserva_atrasados': reserva_atrasados,
        'reserva_cancelados': reserva_cancelados,
        'listo_para_entregar_a_tiempo': listo_para_entregar_a_tiempo,
        'listo_para_entregar_atrasados': listo_para_entregar_atrasados,
        'listo_para_entregar_cancelados': listo_para_entregar_cancelados
    }

    return render(request, 'seguimiento_interno.html', context)


def seguimiento_entrega(request, vendedor_id):
    vendedor = Vendedor.objects.get(id=vendedor_id)
    todos_los_pedidos = vendedor.listar_pedidos()

    for pedido in todos_los_pedidos:
        pedido.actualizar_estado_pedido(anios=0, meses=0, semanas=0, dias=0)

    numero_pedidos_totales = vendedor.total_pedidos_vendedor()
    numero_pedidos_totales_a_tiempo = vendedor.contar_pedidos_por_estado(Pedido.A_TIEMPO)
    numero_pedidos_totales_atrasado = vendedor.contar_pedidos_por_estado(Pedido.ATRASADO)
    numero_pedidos_totales_cliente_no_encotrado = vendedor.contar_pedidos_por_estado(Pedido.ATRASADO)

    numero_pedidos_listo_para_entregar_totales = vendedor.contar_pedidos_por_etapa(Pedido.LISTO_PARA_ENTREGAR)
    numero_pedidos_listo_para_entregar_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.LISTO_PARA_ENTREGAR, Pedido.A_TIEMPO)
    numero_pedidos_listo_para_entregar_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.LISTO_PARA_ENTREGAR, Pedido.ATRASADO)

    numero_pedidos_repartidor_asignado_totales = vendedor.contar_pedidos_por_etapa(Pedido.REPARTIDOR_ASIGNADO)
    numero_pedidos_repartidor_asignadio_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.REPARTIDOR_ASIGNADO, Pedido.A_TIEMPO)
    numero_pedidos_repartidor_asignadio_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.REPARTIDOR_ASIGNADO, Pedido.ATRASADO)

    numero_pedidos_embarcado_totales = vendedor.contar_pedidos_por_etapa(Pedido.EMBARCADO)
    numero_pedidos_embarcado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(Pedido.EMBARCADO, Pedido.A_TIEMPO)
    numero_pedidos_embarcado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(Pedido.EMBARCADO, Pedido.ATRASADO)

    numero_pedidos_paquete_no_entregado_totales = vendedor.contar_pedidos_por_etapa(Pedido.PAQUETE_NO_ENTREGADO)
    numero_pedidos_paquete_no_entregado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.A_TIEMPO)
    numero_pedidos_paquete_no_entregado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.ATRASADO)
    numero_pedidos_paquete_no_entregado_cliente_no_encontrado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.CLIENTE_NO_ENCONTRADO)

    numero_pedidos_paquete_entregado_totales = vendedor.contar_pedidos_por_etapa(Pedido.PAQUETE_ENTREGADO)
    numero_pedidos_paquete_entregado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_ENTREGADO, Pedido.A_TIEMPO)
    numero_pedidos_paquete_entregado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_ENTREGADO, Pedido.ATRASADO)

    context = {
        'numero_pedidos_totales': numero_pedidos_totales,
        'numero_pedidos_totales_a_tiempo': numero_pedidos_totales_a_tiempo,
        'numero_pedidos_totales_atrasado': numero_pedidos_totales_atrasado,
        'numero_pedidos_totales_cliente_no_encotrado': numero_pedidos_totales_cliente_no_encotrado,
        'numero_pedidos_listo_para_entregar_a_tiempo': numero_pedidos_listo_para_entregar_a_tiempo,
        'numero_pedidos_listo_para_entregar_atrasado': numero_pedidos_listo_para_entregar_atrasado,
        'numero_pedidos_listo_para_entregar_totales': numero_pedidos_listo_para_entregar_totales,
        'numero_pedidos_repartidor_asignado_totales': numero_pedidos_repartidor_asignado_totales,
        'numero_pedidos_repartidor_asignadio_a_tiempo': numero_pedidos_repartidor_asignadio_a_tiempo,
        'numero_pedidos_repartidor_asignadio_atrasado': numero_pedidos_repartidor_asignadio_atrasado,
        'numero_pedidos_embarcado_totales': numero_pedidos_embarcado_totales,
        'numero_pedidos_embarcado_a_tiempo': numero_pedidos_embarcado_a_tiempo,
        'numero_pedidos_embarcado_atrasado': numero_pedidos_embarcado_atrasado,
        'numero_pedidos_paquete_no_entregado_totales': numero_pedidos_paquete_no_entregado_totales,
        'numero_pedidos_paquete_no_entregado_a_tiempo': numero_pedidos_paquete_no_entregado_a_tiempo,
        'numero_pedidos_paquete_no_entregado_atrasado': numero_pedidos_paquete_no_entregado_atrasado,
        'numero_pedidos_paquete_no_entregado_cliente_no_encontrado': numero_pedidos_paquete_no_entregado_cliente_no_encontrado,
        'numero_pedidos_paquete_entregado_totales': numero_pedidos_paquete_entregado_totales,
        'numero_pedidos_paquete_entregado_a_tiempo': numero_pedidos_paquete_entregado_a_tiempo,
        'numero_pedidos_paquete_entregado_atrasado': numero_pedidos_paquete_entregado_atrasado
    }

    return render(request, 'seguimiento_entrega.html', context)
