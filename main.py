from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
import random
from scipy.stats import norm
import pandas as pd
import json
import logging
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
PROMEDIO_GLOBAL = 0
DESVIACION_ESTANDAR = 1

# Load top 100 brands CSV
def load_top_brands():
    try:
        # In a real application, you would have a CSV file here
        # For this demo, we'll create a sample dataframe
        data = {
            'marca': ['Falabella', 'Ripley', 'Paris', 'Sodimac', 'Easy', 'Lider', 'Jumbo', 
                    'Movistar', 'Entel', 'WOM', 'Claro', 'Banco de Chile', 'Santander', 'BCI',
                    'Copec', 'Shell', 'Petrobras', 'CCU', 'Cristal', 'Escudo', 'Corona'],
            'score': [87, 82, 78, 85, 76, 71, 75, 68, 72, 81, 65, 88, 84, 79, 77, 75, 72, 83, 79, 75, 81]
        }
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error loading brands: {e}")
        return pd.DataFrame(columns=['marca', 'score'])

# Simple sentiment classifier (Spanish)
def classify_sentiment(text):
    text = text.lower()
    positive_words = [
        'excelente', 'bueno', 'increíble', 'maravilloso', 'genial', 'perfecto', 'recomendado',
        'satisfecho', 'calidad', 'mejor', 'innovador', 'recomiendo', 'positivo', 'éxito', 'amar',
        'gustar', 'eficiente', 'rápido', 'fácil', 'confiable', 'amable', 'servicial', 'satisfacción',
        'premium', 'destacado', 'excepcional', 'fantástico', 'impresionante', 'extraordinario', 'efectivo'
    ]
    
    negative_words = [
        'malo', 'terrible', 'horrible', 'pésimo', 'defectuoso', 'lento', 'caro', 'difícil',
        'complicado', 'problema', 'queja', 'reclamo', 'decepción', 'decepcionado', 'estafa',
        'fraude', 'inútil', 'desagradable', 'pobre', 'mala calidad', 'basura', 'error', 'falla',
        'deficiente', 'dañado', 'incumplimiento', 'incómodo', 'insatisfecho', 'molesto', 'frustración'
    ]
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return "positivo"
    elif negative_count > positive_count:
        return "negativo"
    else:
        return "neutro"

# Calculate score based on mentions
def calculate_score(mentions):
    if not mentions:
        return 50  # Default score if no mentions
    
    score = 0
    for m in mentions:
        peso = m['peso']
        if m['sentimiento'] == "positivo":
            score += 1 * peso
        elif m['sentimiento'] == "neutro":
            score += 0.5 * peso
        elif m['sentimiento'] == "negativo":
            score -= 1 * peso
    
    # Normalize with normal distribution
    z = (score - PROMEDIO_GLOBAL) / DESVIACION_ESTANDAR
    return int(norm.cdf(z) * 100)

# Function to scrape Google News
def scrape_google_news(brand):
    try:
        # In a real application, you would implement actual scraping here
        # For this demo, we'll simulate results
        mentions = []
        
        # Simulate various mentions with different sentiments and sources
        sources = [
            {"domain": "emol.cl", "peso": 1.0},
            {"domain": "latercera.com", "peso": 1.0},
            {"domain": "biobiochile.cl", "peso": 0.8},
            {"domain": "diariofinanciero.cl", "peso": 0.9},
            {"domain": "reclamos.cl", "peso": 0.6},
            {"domain": "blogspot.cl", "peso": 0.6},
            {"domain": "twitter.com", "peso": 0.4},
            {"domain": "linkedin.com", "peso": 0.5},
            {"domain": "instagram.com", "peso": 0.4},
            {"domain": "tiktok.com", "peso": 0.4}
        ]
        
        # Simulate 15-25 random mentions
        num_mentions = random.randint(15, 25)
        
        for i in range(num_mentions):
            source = random.choice(sources)
            domain = source["domain"]
            peso = source["peso"]
            
            # Generate sentiment with some bias (more likely to be neutral)
            sentiment_roll = random.random()
            if sentiment_roll < 0.3:
                sentiment = "positivo"
                title_template = f"{brand}: {random.choice(['nueva innovación sorprende al mercado', 'excelente rendimiento financiero', 'reconocida por su calidad', 'implementa mejoras significativas', 'recibe premio por innovación'])}"
            elif sentiment_roll < 0.7:
                sentiment = "neutro"
                title_template = f"{brand} {random.choice(['anuncia cambios en su directorio', 'presenta nuevo producto', 'participa en evento', 'abre nueva sucursal en Santiago', 'actualiza su catálogo'])}"
            else:
                sentiment = "negativo"
                title_template = f"{random.choice(['Clientes insatisfechos con', 'Problemas de servicio en', 'Reclamos contra', 'Controversia rodea a', 'Críticas por gestión de'])} {brand}"
            
            # Generate a snippet based on sentiment
            if sentiment == "positivo":
                snippet = f"La empresa {brand} ha {random.choice(['mostrado excelentes resultados', 'innovado en el mercado chileno', 'mejorado significativamente su servicio al cliente', 'recibido reconocimiento por su calidad', 'aumentado su satisfacción de clientes'])}"
            elif sentiment == "neutro":
                snippet = f"{brand} {random.choice(['ha informado sobre', 'comunicó acerca de', 'anunció que', 'presentó su', 'publicó información sobre'])} {random.choice(['sus planes futuros', 'cambios en su estructura', 'nuevos productos', 'actualización de servicios', 'participación en el mercado'])}"
            else:
                snippet = f"{random.choice(['Usuarios reportan problemas con', 'Clientes expresan molestia por', 'Aumentan quejas relacionadas con', 'Críticas en redes sociales sobre', 'Reclamos formales contra'])} {brand} por {random.choice(['deficiencias en el servicio', 'problemas de calidad', 'atención al cliente', 'incumplimiento de promesas', 'fallos técnicos'])}"
            
            # Generate a date within the last 30 days
            days_ago = random.randint(1, 30)
            date = (datetime.now().date() - pd.Timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            # Create mention object
            mention = {
                "title": title_template,
                "snippet": snippet,
                "url": f"https://{domain}/noticias/{brand.lower().replace(' ', '-')}-{random.randint(1000, 9999)}",
                "source": domain,
                "date": date,
                "sentimiento": sentiment,
                "peso": peso
            }
            
            mentions.append(mention)
        
        return mentions
    
    except Exception as e:
        logger.error(f"Error scraping Google News: {e}")
        return []

# Generate common phrases from mentions
def extract_common_phrases(mentions):
    if not mentions:
        return []
    
    # In a real application, you would implement NLP here
    # For this demo, we'll return some of the snippets
    positive_snippets = [m['snippet'] for m in mentions if m['sentimiento'] == 'positivo']
    negative_snippets = [m['snippet'] for m in mentions if m['sentimiento'] == 'negativo']
    
    common_phrases = []
    
    if positive_snippets:
        common_phrases.append(random.choice(positive_snippets))
    
    if negative_snippets:
        common_phrases.append(random.choice(negative_snippets))
    
    return common_phrases[:3]  # Return up to 3 phrases

# Generate attribute radar data
def generate_attribute_radar(mentions, brand):
    # Simulate attribute scores based on mentions
    num_positive = sum(1 for m in mentions if m['sentimiento'] == 'positivo')
    num_negative = sum(1 for m in mentions if m['sentimiento'] == 'negativo')
    num_total = len(mentions)
    
    positive_ratio = num_positive / num_total if num_total > 0 else 0.5
    negative_ratio = num_negative / num_total if num_total > 0 else 0.5
    
    # Add some randomness but keep it reasonable
    innovation = min(100, max(0, int(70 + (positive_ratio - 0.5) * 40 + random.randint(-10, 10))))
    service = min(100, max(0, int(60 - (negative_ratio * 50) + random.randint(-15, 15))))
    reputation = min(100, max(0, int(65 + (positive_ratio - negative_ratio) * 30 + random.randint(-10, 10))))
    digital_presence = min(100, max(0, int(50 + num_total + random.randint(-5, 15))))
    
    return {
        "innovation": innovation,
        "service": service,
        "reputation": reputation, 
        "digital_presence": digital_presence
    }

# Generate recommendations based on analysis
def generate_recommendations(score, mentions, attributes):
    recommendations = []
    
    # Count mentions by source and sentiment
    sources = {}
    for m in mentions:
        source = m['source']
        sentiment = m['sentimiento']
        
        if source not in sources:
            sources[source] = {"positivo": 0, "neutro": 0, "negativo": 0}
        
        sources[source][sentiment] += 1
    
    # Generate recommendations based on score
    if score < 40:
        recommendations.append("Tu marca está en una situación crítica. Es necesaria una intervención inmediata en tu estrategia de comunicación.")
    elif score < 60:
        recommendations.append("Tu marca está en la media, pero con riesgo de caer. Enfócate en mejorar tus puntos débiles.")
    elif score < 80:
        recommendations.append(f"Estás en el percentil {score} de percepción. Buen trabajo, pero aún hay margen para mejorar.")
    else:
        recommendations.append(f"Tu marca está en el percentil {score}: estás en la élite digital chilena.")
    
    # Recommendations based on attributes
    weak_attributes = []
    if attributes["service"] < 50:
        weak_attributes.append("servicio al cliente")
    if attributes["innovation"] < 50:
        weak_attributes.append("innovación")
    if attributes["reputation"] < 50:
        weak_attributes.append("reputación")
    if attributes["digital_presence"] < 50:
        weak_attributes.append("presencia digital")
    
    if weak_attributes:
        recommendations.append(f"Tus áreas de mejora principales son: {', '.join(weak_attributes)}.")
    
    # Check for negative mentions in important sources
    important_sources = ["emol.cl", "latercera.com", "diariofinanciero.cl"]
    for source in important_sources:
        if source in sources and sources[source]["negativo"] > 0:
            recommendations.append(f"Tus menciones negativas en {source} podrían estar afectando significativamente tu percepción. Atiende estos issues prioritariamente.")
    
    # Add an analogy or statistical insight
    if score > 80:
        recommendations.append("Tus menciones son mayoritariamente positivas: estás en el extremo favorable de la curva de Gauss, donde solo el 10% de las marcas chilenas logran posicionarse.")
    elif score < 40:
        recommendations.append("Estás en el 30% inferior de la distribución. Las marcas que logran salir de este segmento suelen hacerlo con campañas de reposicionamiento enfocadas.")
    else:
        negative_source = None
        max_negative = 0
        
        for source, counts in sources.items():
            if counts["negativo"] > max_negative:
                max_negative = counts["negativo"]
                negative_source = source
        
        if negative_source:
            recommendations.append(f"Tus menciones negativas provienen principalmente de {negative_source}. Trabajar en este frente podría elevarte hasta un 15% en la percepción total.")
    
    return recommendations[:3]  # Return top 3 recommendations

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get form data
        form_data = request.form
        brand = form_data.get('brand')
        name = form_data.get('name')
        company = form_data.get('company')
        email = form_data.get('email')
        phone = form_data.get('phone')
        employees = form_data.get('employees')
        
        # Validate required fields
        if not all([brand, name, company, email, phone, employees]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400
        
        # Store in session for result page
        session['user_data'] = {
            'brand': brand,
            'name': name,
            'company': company,
            'email': email,
            'phone': phone,
            'employees': employees
        }
        
        # Perform analysis
        mentions = scrape_google_news(brand)
        score = calculate_score(mentions)
        
        # Count sentiment distribution
        positive_count = sum(1 for m in mentions if m['sentimiento'] == 'positivo')
        neutral_count = sum(1 for m in mentions if m['sentimiento'] == 'neutro')
        negative_count = sum(1 for m in mentions if m['sentimiento'] == 'negativo')
        
        # Generate insights
        common_phrases = extract_common_phrases(mentions)
        attribute_radar = generate_attribute_radar(mentions, brand)
        recommendations = generate_recommendations(score, mentions, attribute_radar)
        
        # Compare with similar brands
        top_brands = load_top_brands()
        similar_brands = top_brands.sample(min(5, len(top_brands))).to_dict('records')
        
        # Add the analyzed brand to the comparison
        comparison = similar_brands + [{'marca': brand, 'score': score}]
        
        # Store results in session
        session['results'] = {
            'brand': brand,
            'score': score,
            'sentiment_distribution': {
                'positive': positive_count,
                'neutral': neutral_count,
                'negative': negative_count
            },
            'common_phrases': common_phrases,
            'attribute_radar': attribute_radar,
            'recommendations': recommendations,
            'comparison': comparison,
            'mentions': mentions
        }
        
        return redirect(url_for('results'))
    
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return jsonify({"error": "Ha ocurrido un error al analizar la marca"}), 500

@app.route('/results')
def results():
    # Check if results are in session
    if 'results' not in session:
        return redirect(url_for('index'))
    
    results = session['results']
    user_data = session.get('user_data', {})
    
    return render_template('result.html', results=results, user_data=user_data)

@app.route('/download_pdf')
def download_pdf():
    # This would generate a PDF in a real application
    # For this demo, we'll return a placeholder message
    return "Función para descargar PDF en desarrollo..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
