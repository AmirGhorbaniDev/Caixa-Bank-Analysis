!streamlit run app.py &
from pyngrok import ngrok
public_url = ngrok.connect(port="8501")
print(f"Streamlit app is live at: {public_url}")
