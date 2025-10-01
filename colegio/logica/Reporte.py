# colegio/logica/Reporte.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from ..models import Visita, Reserva, Pagos, Unidad


class Reporte:
    """
    Clase completa para centralizar todos los reportes del dashboard.
    """

    # ==================== MÉTODOS ORIGINALES ====================

    @staticmethod
    @api_view(['GET'])
    def dashboard_stats(request):
        """
        Retorna estadísticas generales del condominio
        """
        total_visitas = Visita.objects.count()
        total_reservas = Reserva.objects.count()

        hoy = timezone.now().date()
        reservas_hoy = Reserva.objects.filter(fecha=hoy).count()
        visitas_hoy = Visita.objects.filter(fecha_ingreso=hoy).count()

        data = {
            "total_visitas": total_visitas,
            "total_reservas": total_reservas,
            "visitas_hoy": visitas_hoy,
            "reservas_hoy": reservas_hoy,
        }
        return Response(data)

    @staticmethod
    @api_view(['GET'])
    def ultimas_visitas(request):
        """
        Retorna las últimas 10 visitas registradas
        """
        visitas = Visita.objects.select_related("autorizado", "unidad", "area_social") \
            .order_by("-fecha_ingreso", "-hora_ingreso")[:10]

        data = []
        for v in visitas:
            data.append({
                "id": v.id,
                "fecha": v.fecha_ingreso.isoformat() if v.fecha_ingreso else None,
                "hora": v.hora_ingreso.isoformat() if v.hora_ingreso else None,
                "visitante": f"{v.nombre_visitante} {v.apellido_paterno} {v.apellido_materno or ''}".strip(),
                "telefono": v.telefono,
                "motivo": v.motivo or "N/A",
                "unidad": str(v.unidad) if v.unidad else "N/A",
                "area_social": str(v.area_social) if v.area_social else "N/A",
                "autorizado_por": str(v.autorizado) if v.autorizado else "No especificado",
            })

        return Response(data)

    @staticmethod
    @api_view(['GET'])
    def proximas_reservas(request):
        """
        Retorna las próximas 10 reservas
        """
        hoy = timezone.now().date()

        reservas = Reserva.objects.select_related("area_social", "persona") \
            .filter(fecha__gte=hoy) \
            .order_by("fecha", "horario_inicio")[:10]

        data = []
        for r in reservas:
            data.append({
                "id": r.id,
                "fecha": r.fecha.isoformat() if r.fecha else None,
                "hora_inicio": r.horario_inicio.isoformat() if r.horario_inicio else None,
                "hora_fin": r.horario_fin.isoformat() if r.horario_fin else None,
                "area_social": str(r.area_social) if r.area_social else "N/A",
                "persona": str(r.persona) if r.persona else "No especificado",
                "estado": r.estado,
            })

        return Response(data)

    # ==================== MÉTODOS FINANCIEROS CORREGIDOS ====================

    @staticmethod
    @api_view(['GET'])
    def metricas_financieras(request):
        """
        Retorna métricas financieras clave del condominio
        """
        from django.db.models import Sum
        
        hoy = timezone.now().date()
        mes_actual = hoy.replace(day=1)
        
        # Cálculo preciso del mes anterior
        if mes_actual.month == 1:
            mes_anterior = mes_actual.replace(year=mes_actual.year-1, month=12)
        else:
            mes_anterior = mes_actual.replace(month=mes_actual.month-1)
        
        # Cálculo de métricas principales
        ingresos_mes_actual = Pagos.objects.filter(
            fecha__year=mes_actual.year, 
            fecha__month=mes_actual.month
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        ingresos_mes_anterior = Pagos.objects.filter(
            fecha__year=mes_anterior.year, 
            fecha__month=mes_anterior.month
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # Calcular variación porcentual
        variacion_ingresos = 0
        if ingresos_mes_anterior > 0:
            variacion_ingresos = ((ingresos_mes_actual - ingresos_mes_anterior) / ingresos_mes_anterior) * 100
        
        total_unidades = Unidad.objects.count()
        unidades_ocupadas = Unidad.objects.filter(estado='ocupado').count()
        tasa_ocupacion = (unidades_ocupadas / total_unidades * 100) if total_unidades > 0 else 0
        
        # Ingresos proyectados (basado en valor mensual de unidades ocupadas)
        ingresos_proyectados = Unidad.objects.filter(estado='ocupado').aggregate(
            total=Sum('valor_mensual')
        )['total'] or 0
        
        # Ingresos anuales
        ingresos_anuales = Pagos.objects.filter(
            fecha__year=hoy.year
        ).aggregate(total=Sum('monto'))['total'] or 0

        data = {
            "ingresos_mes_actual": float(ingresos_mes_actual),
            "ingresos_mes_anterior": float(ingresos_mes_anterior),
            "variacion_ingresos": round(variacion_ingresos, 2),
            "tasa_ocupacion": round(tasa_ocupacion, 2),
            "ingresos_proyectados": float(ingresos_proyectados),
            "unidades_ocupadas": unidades_ocupadas,
            "total_unidades": total_unidades,
            "ingresos_anuales": float(ingresos_anuales)
        }
        return Response(data)

    @staticmethod
    @api_view(['GET'])
    def ingresos_por_mes(request):
        """
        Retorna ingresos de los últimos 12 meses para gráfico
        """
        from django.db.models import Sum
        
        hoy = timezone.now().date()
        data = []
        
        for i in range(11, -1, -1):
            mes_fecha = hoy.replace(day=1) - relativedelta(months=i)
            ingresos = Pagos.objects.filter(
                fecha__year=mes_fecha.year,
                fecha__month=mes_fecha.month
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            data.append({
                "mes": mes_fecha.strftime("%Y-%m"),
                "mes_nombre": mes_fecha.strftime("%b %Y"),
                "ingresos": float(ingresos)
            })
        
        return Response(data)

    @staticmethod
    @api_view(['GET'])
    def pagos_pendientes(request):
        """
        Retorna pagos pendientes con cálculo REAL de días de mora
        """
        from django.db.models import Subquery, OuterRef, Exists
        from datetime import timedelta
        
        hoy = timezone.now().date()
        dia_vencimiento = 10  # Día del mes en que vence el pago
        
        # Calcular fecha de vencimiento para el mes actual
        if hoy.day <= dia_vencimiento:
            # Si estamos antes del día de vencimiento, la fecha de vencimiento es del mes anterior
            fecha_vencimiento = (hoy.replace(day=1) - timedelta(days=1)).replace(day=dia_vencimiento)
        else:
            # Si estamos después del día de vencimiento, la fecha de vencimiento es de este mes
            fecha_vencimiento = hoy.replace(day=dia_vencimiento)
        
        # Subconsulta para verificar si la unidad tiene pagos recientes
        pagos_recientes = Pagos.objects.filter(
            unidad=OuterRef('pk'),
            fecha__gte=fecha_vencimiento
        )
        
        # Unidades ocupadas SIN pagos recientes
        pagos_pendientes = Unidad.objects.filter(
            estado='ocupado'
        ).annotate(
            tiene_pago_reciente=Exists(pagos_recientes)
        ).filter(
            tiene_pago_reciente=False
        ).select_related('propietario')
        
        data = []
        for unidad in pagos_pendientes:
            # Calcular días REALES de mora
            dias_mora = (hoy - fecha_vencimiento).days
            
            data.append({
                "unidad_id": unidad.id,
                "unidad_str": str(unidad),
                "propietario": str(unidad.propietario) if unidad.propietario else "No asignado",
                "valor_mensual": float(unidad.valor_mensual),
                "estado": unidad.estado,
                "dias_mora": max(0, dias_mora),  # No permitir valores negativos
                "fecha_vencimiento": fecha_vencimiento.isoformat()
            })
        
        return Response(data)