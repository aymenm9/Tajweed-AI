import json
import google.generativeai as genai
from .config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

# Create the model



def generate_quiz(topic):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    )
    response = model.generate_content([
    "You are an AI model designed to generate Islamic quizzes for the Tajweed-AI app. Your task is to create a single quiz question on the topic \"{topic}\". The content must be strictly according to the Qur’an, the authentic Sunnah of the Prophet Muhammad (peace be upon him), and the understanding of the Salaf (righteous predecessors). Provide a question in Arabic, four options in Arabic, the correct answer (a, b, c, or d), and evidence in Arabic from the Qur’an or authentic Hadith.",
    "input: topic : \"topic\"",
    "output: {\n  \"quiz\": {\n    \"question\": \"string\",\n    \"options\": {\n      \"a\": \"string\",\n      \"b\": \"string\",\n      \"c\": \"string\",\n      \"d\": \"string\"\n    },\n    \"answer\": \"string\",\n    \"evidence\": \"string\"\n  }\n}",
    "input: topic :  \"Prophet's Sunnah\"",
    "output: {\nquiz: {\nquestion: \"ما الذي قاله النبي محمد (صلى الله عليه وسلم) عن الابتسامة؟\", \noptions: {\na: \"إنها عبء\",\nb: \"إنها صدقة\",\nc: \"إنها غير ضرورية\",\nd: \"إنها علامة ضعف\"},\nanswer: \"b\",\nevidence: \"قال رسول الله (صلى الله عليه وسلم): تبسمك في وجه أخيك صدقة - رواه الترمذي، كتاب البر والصلة، حديث 2004\"\n}\n}",
    "input: Topic: \"Fiqh\"",
    "output: {\n  \"quiz\": {\n    \"question\": \"ما حكم الوضوء إذا نسي المسلم مسح رأسه؟\",\n    \"options\": {\n      \"a\": \"الوضوء صحيح ولا يحتاج إعادة\",\n      \"b\": \"الوضوء باطل ويجب إعادته\",\n      \"c\": \"يجب مسح الرأس فقط دون إعادة الوضوء\",\n      \"d\": \"الوضوء صحيح إذا كان هناك عذر\"\n    },\n    \"answer\": \"b\",\n    \"evidence\": \"قال الله تعالى: يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا قُمْتُمْ إِلَى الصَّلَاةِ فَاغْسِلُوا وُجُوهَكُمْ وَأَيْدِيَكُمْ إِلَى الْمَرَافِقِ وَامْسَحُوا بِرُءُوسِكُمْ وَأَرْجُلَكُمْ إِلَى الْكَعْبَيْنِ - سورة المائدة: 6\"\n  }\n}",
    "input: Topic: \"{topic}\"",
    "output: ",
    ])
    return json.loads(response.to_dict()['candidates'][0]['content']['parts'][0]['text'])['quiz']

def chatbot(message:str,chat_history:list = []):
    generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    generation_config=generation_config,
    )
    initial_history = [
        {
            "role": "user",
            "parts": [
                {
                    "text": "You are a chatbot named 'Tajweed-AI,' an Islamic chatbot for the Tajweed-AI app. Your task is to answer users' questions and assist them. Your responses and content must be strictly based on the Qur’an, the authentic Sunnah of the Prophet Muhammad (peace be upon him), and the understanding of the Salaf (righteous predecessors) and the creed of the Salaf and the Companions. Keep your answers simple and concise, and always provide evidence from the Qur’an or an authentic Hadith. if the question is in Arabic answer in Arabic else in English"
                }
            ],
        },
        {
            "role": "user",
            "parts":[{"text":"how are you"}]
        },
        {
            "role": "model",
            "parts":[{"text":"Tajweed-AI"}]
        }

    ]

    history = initial_history + chat_history
    chat_session = model.start_chat(history=history)

    response = chat_session.send_message(message)

    return response.text

