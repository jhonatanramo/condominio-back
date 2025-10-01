import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
#-----------------------------
# colegio/views.py
import json
import cv2
import numpy as np
from django.core.files.base import ContentFile
from .models import Placa  # Asumiendo que tienes este modelo
from django.http import HttpResponse
#------------------------
# colegio/logica/agendavisita.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from .models import Visita, Reserva, Pagos
from django.utils import timezone



# Eliminamos la variable global reader y get_reader() para evitar cargas innecesarias
stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
def create_payment(request):
    data = request.data
    try:
        intent = stripe.PaymentIntent.create(
            amount=data.get("amount"),   # en centavos (ej: 1000 = $10.00)
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return Response({"clientSecret": intent["client_secret"]})
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = "sk_test_51RRklm4Zqdn7RVeShGNEhW7wo7nVUDZRenO3u5gRLtuygmV2iCzWB0OdPB6YxF8pYwqVSww887vkhE6GXgHfJw2Z00yWO4QYsY"  # desde dashboard de Stripe
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        print("💰 Pago recibido:", intent["id"])

    return HttpResponse(status=200)


@api_view(["POST"])
@csrf_exempt
def crear(request):
    try:
        usuario = request.session.get('usuario')
        if not usuario:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener datos
        inicio = request.data.get("inicio")
        fin = request.data.get("fin")
        monto = request.data.get("monto")
        idareasocial = request.data.get("idareasocial")
        cant_gente = request.data.get("cant_gente")
        fecha = request.data.get("fecha")

        if not inicio or not fin or not idareasocial or not monto:
            return Response({"error": "Faltan datos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        if not fecha:
            fecha = timezone.now().date()

        idpersona = usuario.get('id')

        # Crear reserva
        reserva = Reserva.objects.create(
            horario_inicio=inicio,
            horario_fin=fin,
            fecha=fecha,
            estado=None,
            cantidad_gente=cant_gente,
            area_social_id=idareasocial,
            persona_id=idpersona,
        )

        # Crear pago
        pago = Pagos.objects.create(
            monto=monto,
            fecha=timezone.now().date(),
            duracion_meses=0,
            url_foto=None,
            persona_id=idpersona,
            unidad_id=None,
            reserva_id=reserva.id,
        )
        return HttpResponse("Reserva creada")
        

    except Exception as e:
        print("❌ ERROR:", str(e))
        print(traceback.format_exc())
        return Response({"error": "Ocurrió un error al crear la reserva"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def analizar_placa(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        # Verificar que se envió una imagen
        if 'imagen' not in request.FILES:
            return JsonResponse({'error': 'No se proporcionó imagen'}, status=400)
        
        imagen = request.FILES['imagen']
        
        # Leer y procesar la imagen
        imagen_bytes = imagen.read()
        imagen_np = np.frombuffer(imagen_bytes, np.uint8)
        imagen_cv = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
        
        if imagen_cv is None:
            return JsonResponse({'error': 'Imagen no válida'}, status=400)
        
        # ✅ IMPORTACIÓN DIFERIDA: EasyOCR solo se carga cuando se necesita
        import easyocr
        
        # ✅ Configuración optimizada para ahorrar memoria
        reader = easyocr.Reader(
            ['en'], 
            gpu=False,  # Forzar uso de CPU
            download_enabled=False,  # Evitar descargas automáticas
            model_storage_directory='/tmp/easyocr'  # Directorio temporal
        )
        
        # Realizar OCR en la imagen
        resultados = reader.readtext(imagen_cv)
        
        # ✅ Limpiar recursos explícitamente
        del reader
        import gc
        gc.collect()
        
        if not resultados:
            return JsonResponse({
                'exito': False,
                'error': 'No se detectó texto en la imagen'
            })
        
        # Filtrar y procesar resultados (buscar patrones de placa)
        texto_placa = None
        confianza = 0
        
        for (bbox, texto, conf) in resultados:
            # Limpiar texto y verificar si coincide con formato de placa
            texto_limpio = texto.upper().replace(' ', '').replace('-', '')
            if es_formato_placa_valido(texto_limpio):  # Función personalizada
                if conf > confianza:
                    texto_placa = texto_limpio
                    confianza = conf
        
        if not texto_placa:
            return JsonResponse({
                'exito': False,
                'error': 'No se encontró una placa válida en la imagen'
            })
        
        # Guardar en la base de datos
        registro = Placa(
            placa=texto_placa,
            confianza=confianza,
            # imagen_original=imagen  # Opcional: guardar la imagen
        )
        registro.save()
        
        return JsonResponse({
            'exito': True,
            'placa': texto_placa,
            'confianza': round(confianza * 100, 2),
            'mensaje': 'Placa guardada exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'error': f'Error en el procesamiento: {str(e)}'
        })


@api_view(["GET"])
def usuario(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return Response({"error": "No hay usuario autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"usuario": usuario}, status=status.HTTP_200_OK)


def es_formato_placa_valido(texto):
    """
    Función personalizada para validar formatos de placa.
    Adapta según el formato de tu país.
    """
    # Ejemplo para formato: ABC123 o ABC1234
    if len(texto) in [6, 7]:
        # Verificar combinación de letras y números
        letras = texto[:3]
        numeros = texto[3:]
        return letras.isalpha() and numeros.isdigit()
    return False