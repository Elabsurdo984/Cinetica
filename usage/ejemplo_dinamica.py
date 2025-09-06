# -*- coding: utf-8 -*-
"""
Ejemplo de uso del modulo de dinamica de Cinetica.

Este ejemplo demuestra las capacidades del modulo de dinamica incluyendo:
- Leyes de Newton
- Analisis de fuerzas
- Trabajo y energia
"""

import sys
import os
import math
import numpy as np

# Agregar el directorio actual al path para importar la version local
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cinetica.dinamica import LeyesNewton, AnalisisFuerzas, TrabajoEnergia

def ejemplo_leyes_newton():
    """Ejemplo de uso de las leyes de Newton."""
    print("=== LEYES DE NEWTON ===")
    
    newton = LeyesNewton()
    
    # Segunda ley: calcular fuerza
    fuerza = newton.segunda_ley(masa=10, aceleracion=5)
    print(f"Fuerza necesaria para acelerar 10 kg a 5 m/s²: {fuerza}")
    
    # Fuerza neta de múltiples fuerzas
    fuerzas = [50, -20, 15, -10]
    fuerza_neta = newton.fuerza_neta(fuerzas)
    print(f"Fuerza neta de {fuerzas}: {fuerza_neta}")
    
    # Verificar equilibrio
    fuerzas_equilibrio = [100, -50, -50]
    en_equilibrio = newton.equilibrio(fuerzas_equilibrio)
    print(f"¿Fuerzas {fuerzas_equilibrio} en equilibrio? {en_equilibrio}")
    
    # Peso en la Tierra
    peso = newton.peso(masa=75)
    print(f"Peso de una persona de 75 kg: {peso}")
    
    # Fuerza centrípeta
    f_centripeta = newton.fuerza_centripeta(masa=2, velocidad=10, radio=5)
    print(f"Fuerza centrípeta (m=2kg, v=10m/s, r=5m): {f_centripeta}")
    
    print()

def ejemplo_analisis_fuerzas():
    """Ejemplo de analisis de fuerzas."""
    print("=== ANALISIS DE FUERZAS ===")
    
    fuerzas = AnalisisFuerzas()
    
    # Friccion estatica
    f_estatica = fuerzas.friccion_estatica(normal=200, coeficiente=0.3)
    print(f"Friccion estatica maxima (N=200N, mu=0.3): {f_estatica}")
    
    # Friccion cinetica
    f_cinetica = fuerzas.friccion_cinetica(normal=200, coeficiente=0.25)
    print(f"Friccion cinetica (N=200N, mu=0.25): {f_cinetica}")
    
    # Fuerza elastica
    f_elastica = fuerzas.fuerza_elastica(constante=500, deformacion=0.1)
    print(f"Fuerza elastica (k=500N/m, x=0.1m): {f_elastica}")
    
    # Descomposicion de fuerza
    Fx, Fy = fuerzas.descomponer_fuerza(magnitud=100, angulo=math.pi/4)
    print(f"Fuerza de 100N a 45 grados: Fx={Fx:.2f}, Fy={Fy:.2f}")
    
    # Plano inclinado
    F_par, F_perp = fuerzas.plano_inclinado(peso=500, angulo=math.pi/6)
    print(f"Peso 500N en plano 30 grados: Paralela={F_par:.2f}, Perpendicular={F_perp:.2f}")
    
    # Tension en cuerda
    tension = fuerzas.tension_cuerda(masa=20, aceleracion=2)
    print(f"Tension con masa 20kg y aceleracion 2m/s2: {tension}")
    
    print()

def ejemplo_trabajo_energia():
    """Ejemplo de trabajo y energía."""
    print("=== TRABAJO Y ENERGÍA ===")
    
    te = TrabajoEnergia()
    
    # Trabajo con fuerza constante
    trabajo = te.trabajo_fuerza_constante(fuerza=50, desplazamiento=10)
    print(f"Trabajo (F=50N, d=10m): {trabajo}")
    
    # Trabajo con angulo
    trabajo_angulo = te.trabajo_fuerza_constante(fuerza=100, desplazamiento=5, angulo=math.pi/3)
    print(f"Trabajo con angulo 60 grados (F=100N, d=5m): {trabajo_angulo}")
    
    # Energia cinetica
    Ec = te.energia_cinetica(masa=10, velocidad=15)
    print(f"Energia cinetica (m=10kg, v=15m/s): {Ec}")
    
    # Energia potencial gravitacional
    Ep_grav = te.energia_potencial_gravitacional(masa=5, altura=20)
    print(f"Energia potencial gravitacional (m=5kg, h=20m): {Ep_grav}")
    
    # Energia potencial elastica
    Ep_elastica = te.energia_potencial_elastica(constante=200, deformacion=0.15)
    print(f"Energia potencial elastica (k=200N/m, x=0.15m): {Ep_elastica}")
    
    # Energia mecanica total
    Em = te.energia_mecanica_total(energia_cinetica=1000, energia_potencial=500)
    print(f"Energia mecanica total (Ec=1000J, Ep=500J): {Em}")
    
    # Teorema trabajo-energia
    W_neto = te.teorema_trabajo_energia(masa=8, velocidad_inicial=0, velocidad_final=12)
    print(f"Trabajo neto por teorema trabajo-energia (m=8kg, v0=0, v=12m/s): {W_neto}")
    
    # Potencia
    potencia = te.potencia(trabajo=2000, tiempo=10)
    print(f"Potencia (W=2000J, t=10s): {potencia}")
    
    # Potencia instantanea
    P_inst = te.potencia_instantanea(fuerza=75, velocidad=8)
    print(f"Potencia instantanea (F=75N, v=8m/s): {P_inst}")
    
    print()

def ejemplo_problema_completo():
    """Ejemplo de problema completo combinando todos los módulos."""
    print("=== PROBLEMA COMPLETO ===")
    print("Un bloque de 10 kg se desliza por un plano inclinado de 30 grados con friccion.")
    print("Coeficiente de friccion cinetica: 0.2")
    print()
    
    # Datos del problema
    masa = 10  # kg
    angulo = math.pi/6  # 30 grados en radianes
    mu_k = 0.2  # coeficiente de friccion cinetica
    distancia = 5  # metros
    
    # Instanciar clases
    newton = LeyesNewton()
    fuerzas = AnalisisFuerzas()
    te = TrabajoEnergia()
    
    # 1. Calcular peso y sus componentes
    peso = newton.peso(masa=masa)
    F_paralela, F_perpendicular = fuerzas.plano_inclinado(peso=peso, angulo=angulo)
    
    print(f"Peso del bloque: {peso}")
    print(f"Componente paralela al plano: {F_paralela:.2f}")
    print(f"Componente perpendicular al plano: {F_perpendicular:.2f}")
    
    # 2. Calcular friccion cinetica
    f_friccion = fuerzas.friccion_cinetica(normal=F_perpendicular, coeficiente=mu_k)
    print(f"Fuerza de friccion cinetica: {f_friccion:.2f}")
    
    # 3. Calcular fuerza neta y aceleracion
    fuerza_neta = newton.fuerza_neta([F_paralela.magnitude, -f_friccion.magnitude])
    aceleracion = newton.segunda_ley(masa=masa, fuerza=fuerza_neta)
    
    print(f"Fuerza neta: {fuerza_neta:.2f}")
    print(f"Aceleracion del bloque: {aceleracion:.2f}")
    
    # 4. Calcular trabajo realizado por cada fuerza
    W_peso = te.trabajo_fuerza_constante(fuerza=F_paralela, desplazamiento=distancia)
    W_friccion = te.trabajo_fuerza_constante(fuerza=f_friccion, desplazamiento=distancia, angulo=math.pi)
    W_neto = W_peso + W_friccion
    
    print(f"Trabajo realizado por el peso: {W_peso:.2f}")
    print(f"Trabajo realizado por la friccion: {W_friccion:.2f}")
    print(f"Trabajo neto: {W_neto:.2f}")
    
    # 5. Calcular velocidad final usando cinematica
    # v^2 = v0^2 + 2as, con v0 = 0
    velocidad_final = math.sqrt(2 * aceleracion.magnitude * distancia)
    
    print(f"Velocidad final: {velocidad_final:.2f} m/s")
    
    # 6. Verificar con teorema trabajo-energia
    W_teorema = te.teorema_trabajo_energia(masa=masa, velocidad_inicial=0, velocidad_final=velocidad_final)
    print(f"Trabajo segun teorema trabajo-energia: {W_teorema:.2f}")
    print(f"Diferencia: {abs(W_neto.magnitude - W_teorema.magnitude):.6f} J")

if __name__ == "__main__":
    print("EJEMPLOS DEL MODULO DE DINAMICA DE CINETICA")
    print("=" * 50)
    print()
    
    ejemplo_leyes_newton()
    ejemplo_analisis_fuerzas()
    ejemplo_trabajo_energia()
    ejemplo_problema_completo()
    
    print("\nEjemplos completados exitosamente!")
