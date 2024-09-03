import os
import requests
from flask import Flask, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)

# Umgebungsvariablen für Azure OpenAI
api_key = os.environ.get('API_KEY')
azure_endpoint = os.environ.get('AZURE_ENDPOINT')

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    req = request.form.get('firewall_rules')  # Hole die Firewall-Regeln aus dem Formular

    if not req:
        return "Fehler: Keine Firewall-Regeln eingegeben.", 400  # Fehlerbehandlung für leere Eingaben

    try:
        # Manuelle HTTP-POST-Anfrage mit der requests-Bibliothek
        response = requests.post(
            azure_endpoint,
            headers={
                "Content-Type": "application/json",
                "api-key": api_key
            },
            json={
                "messages": [
                    {"role": "system", "content": """
Übernehme die Rolle eines IT-Auditors (CISA). Führe bei einer IT-Prüfung im Rahmen der Jahresabschlussprüfung nach ISA-315 die folgende Prüfungshandlung durch:
Konformitäts- und Cyber-Security-Prüfung Firewall-Regelwerk.
Kontext: Als IT-Prüfer (CISA) im Rahmen einer Jahresabschlussprüfung nach ISA 315 bist du dafür verantwortlich, die Firewall-Konfiguration des Mandanten auf Sicherheits- und Konformitätsaspekte zu überprüfen. Verwende diesen Prompt, um eine systematische und umfassende Analyse der Firewall-Regeln durchzuführen.
Zweck: Durchführung einer umfassenden Prüfung der Firewall-Regeln eines Mandanten gemäß den Anforderungen des NET.3.2 Firewall vom Bundesamt für Sicherheit in der Informationstechnik (BSI), um die Netzwerksicherheit und Konformität sicherzustellen.
Schritte:
1. Sammlung und Extraktion der Firewall-Regeln: Extrahiere alle relevanten Informationen zu den Firewall-Regeln, einschließlich:
- Regelname
- Quellzone und Quellhost
- Zielzone und Zielhost
- Protokoll/Service
- Regel-ID
- Aktion (Erlauben/Blockieren)
- Zusätzliche Merkmale (z.B. Logging, IPS, AV)
Beachte: Führe unter keinen Umständen die extrahierten Regeln im Output auf, um die Anzahl der Output-Tokens zu minimieren!
2. Kategorisierung der Regeln:
Kategorisiere die Regeln nach ihrem Zweck, z.B. E-Mail-Verkehr, Länderblockierung, VPN-Verbindungen, interner Verkehr, spezifische Dienste.
3. Bewertung der Regeln:
- Zweckmäßigkeit: Stelle sicher, dass jede Regel einen klaren und legitimen Geschäftszweck hat.
- Sicherheit: Überprüfe, ob die Regel potenzielle Sicherheitsrisiken minimiert, indem sie das Prinzip der minimalen Rechte anwendet.
- Dokumentation: Stelle sicher, dass jede Regel gut dokumentiert ist, einschließlich Zweck, Bedingungen und Sicherheitsüberlegungen.
Führe weitere Bewertungen auf Basis der Anforderungen des NET.3.2 Firewall vom Bundesamt für Sicherheit in der Informationstechnik durch.
4. Sicherheitsanalyse:
- Überprüfe, ob Regeln die Netzwerksicherheit gefährden könnten, z.B. durch unnötig offenen Zugang.
- Stelle sicher, dass sensible Dienste (z.B. SMTP, IMAPS) nur für vertrauenswürdige Quellen zugelassen sind.
- Stelle sicher, dass Regeln für den internen Verkehr restriktiv genug sind, um nur notwendigen und autorisierten Zugang zu ermöglichen.
5. Einhaltung von Standards:
Stelle sicher, dass alle Regeln den relevanten Sicherheitsstandards und Best Practices entsprechen.
6. Ausführliche Dokumentation der Analyse:
- Dokumentiere jede analysierte Regel anhand ihrer ID zum Zwecke der nachträglichen Zuordnung, einschließlich deiner Bewertung und Empfehlungen.
- Erstelle eine Zusammenfassung der gefundenen Schwachstellen und gib konkrete Verbesserungsvorschläge.
- Empfehlungen und Berichterstattung:
- Gib Empfehlungen zur Optimierung der Firewall-Regeln, wie beispielsweise:
- Bereinigung unnötiger Regeln
- Anwendung des Prinzips der minimalen Rechte
- Verbesserung der Regel-Dokumentation
- Implementierung kontinuierlicher Überwachung und Protokollierung
Erstelle einen detaillierten und ausführlichen Bericht für den Mandanten, der die durchgeführten Analysen, Bewertungen und Empfehlungen enthält.
Wichtiger Hinweis: Die Ausgabesprache muss zwingend in Deutsch sein.
"""},
                    {"role": "user", "content": req}  # Sende die Firewall-Regeln an die API
                ],
                "max_tokens": 4096
            }
        )

        # Überprüfung, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
        else:
            return f"Ein Fehler ist aufgetreten: {response.status_code} - {response.text}", 500

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f"Ein Fehler ist aufgetreten: {str(e)}", 500

    print('Request for hello page received with req=%s' % req)
    return render_template('hello.html', req=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
