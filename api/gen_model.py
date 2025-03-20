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
    "response_mime_type": "application/json",
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

def generate_lesson(user_data):

    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-lite",
      generation_config=generation_config,
    )

    response = model.generate_content([
      """{\n  \"prompt\": {\n    \"task\": \"Generate personalized lessons for users learning to read and recite the Quran.\",\n
              \"instructions\": [\n
              \"Each lesson must include a title, content in markdown format optimized for display in a Flutter app, an estimated time to complete, and a lesson number.\",\n      
              \"Keep lesson titles short and concise to fit mobile app interfaces while remaining descriptive.\",\n      
              \"Structure the content for effective learning, incorporating key Tajweed concepts (e.g., pronunciation rules, articulation points, and recitation techniques).\",\n      
              \"Adapt lessons to the user's proficiency level (beginner, intermediate, advanced), preferred learning style (e.g., visual, auditory, kinesthetic), and specific focus areas (e.g., mastering specific rules, improving fluency).\",\n      
              \"Consider the user's Arabic language proficiency (`arabic_level`), general academic background (`academic_level`), and Sharia studies knowledge (`sharia_study_level`) to adjust lesson complexity, language support, and Islamic context.\",\n      
              \"Generate all lesson content, including titles, in the language specified by `lessons_language` (e.g., English, Arabic), ensuring accessibility and comprehension for the user.\",\n      
              \"When `lessons_language` is Arabic, use only Arabic throughout the lesson (titles, content, examples), avoiding English terms, transliteration, or translation unless explicitly required by the user's input.\",\n      
              \"If the user already understands a subject or Tajweed concept, include only a brief reminder or summary instead of a full lesson, ensuring efficiency and relevance.\",\n      
              \"Order the lessons sequentially from the most basic to the most advanced for progressive learning.\",\n      
              \"Include clear and relevant examples in each lesson to illustrate concepts, tailored to the user's learning style and proficiency level.\",\n      
              \"For lessons involving Tajweed concepts, provide specific examples from the Quran (e.g., verses or words) to demonstrate the application of rules, including Arabic text and, if applicable, transliteration or translation in the `lessons_language` only when it is not Arabic, add all nessey lessens for the user to reach the desired proficiency level even if it is not in the focus_areas and it nessery for the user to learn the Quran\",\n      
              \"Output the lessons in the following JSON format: [{'lesson_number': 1, 'title': 'title of Lesson', 'content': 'markdown content for a Flutter app', 'estimated_time': 'n min'}, ...]\"\n    ],\n    
              \"context\": {\n      \"app_name\": \"tajweed-ai\",\n      \"subject\": \"Learning how to read and recite the Quran\"\n    },\n    
              \"output_format\": \"JSON\"\n  }\n}""",
      "input: user_data: \{user_data\}",
      "output: [{'lesson_number': int , 'title': 'title of Lesson', 'content': 'markdown content for a Flutter app', 'estimated_time': 'n min'}]",
      "input: user_data: {user_data}",
      "output: ",
    ])
    return json.loads(response.to_dict()['candidates'][0]['content']['parts'][0]['text'])




def choise_verse(tajweed_focus_rule='all'):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config=generation_config,
    )

    prompt = f"""
    {{
        "prompt": {{
            "task": "Provide a Quranic verse that exemplifies the Tajweed rule: '{tajweed_focus_rule}'.",
            "instructions": [
                "Identify a verse from the Quran that demonstrates the specified Tajweed rule.",
                "Return the sura number, aya number, and the verse text in Quranic Arabic script.",
                "Output all text in Arabic.",
                "Format the output as a JSON object containing the sura, aya, and verse."
            ],
            "context": {{
                "app_name": "tajweed-example-finder",
                "subject": "Finding Quranic verses for Tajweed rules"
            }},
            "output_format": "JSON"
        }}
    }}
    """

    response = model.generate_content(prompt)

    try:
        json_response = json.loads(response.text)
        result = json_response[0] # load the list then get the first item.
        print(result)
        return result
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}") # Print the response for debugging
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



def recitationCorrection(sura: int, aya: int, verse: str, user_audio_base64: str, tajweed_rule='all'):
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )

    
    response = model.generate_content([
    f""" task: Analyze a user's Quran recitation based on a provided verse and Tajweed rules.,\n        instructions:\n            You will receive the following information:\n            - Sura Number: {sura},\n            - Aya Number: {aya},\n            - Verse Text (Arabic): {verse},\n            - User's Recitation (Base64 Encoded Audio): {user_audio_base64}'.\n            - Tajweed Focus Rule: {tajweed_rule} (or 'all' for general analysis),\n            Your task is to analyze the user's recitation based on this information.\n            Specifically, you should:\n            1. Attempt to identify any deviations in pronunciation, articulation, or application of Tajweed rules based on the base64 audio and the provided verse,\n            2. Focus on the specified Tajweed rule ({tajweed_rule}) if provided, or analyze all relevant rules if 'all' is given,\n            3. If possible, identify specific words where errors occur,\n\n            4. Classify each identified mistake (if any) as 'خطأ في النطق', 'قصر الممد بدلاً من المد', 'تجاوز قاعدة التجويد', etc., and assign a severity: 'صغير' (minor), 'متوسط' (medium), or 'كبير' (major),                                                         \n            5. give the user a score on int/100.                         \n           6. be strict in your evaluation.                         \n            7. Return the analysis as a JSON object with the following structure:\n        "sura\": {sura}, \"aya\": {aya}, \"verse\": \"{verse}\", \"errors\": ["mistake_word\": \"word with mistake in the verse\", \"mistake_type\": \"نوع الخطأ بالعربية\", \"severity\": \"\",...], \"score\": int \n            8. If no mistakes are detected, return an empty 'errors' list and a confirmation message in Arabic: 'القراءة صحيحة',\n            8. All text in the response must be in Arabic\n        context :\n            app_name : quran-recitation-corrector,\n            subject: Analyzing Quran recitation with Tajweed rules,\n        output_format: JSON """,
    "input: sura: int , aya:int, verse : the verse in Arabic , Base64 Encoded : Audiouser_audio_base64 , Tajweed Focus Rule: tajweed_rule",
    "output: {\"sura\": int , \"aya\":int, \"verse\":\"the verse in Arabic\", \"errors\": [{\"word\": \"word \nwith mistake\", \"mistake_type\": \"نوع الخطأ بالعربية\", \"severity\": \"\"}], \n\"score\": score}",
    f"input: sura : {sura}, aya : {aya}, verse : {verse}, Base64 Encoded : {user_audio_base64} , Tajweed Focus Rule: {tajweed_rule}",
    "output: ",
    ])

    return json.loads(response.to_dict()['candidates'][0]['content']['parts'][0]['text'])