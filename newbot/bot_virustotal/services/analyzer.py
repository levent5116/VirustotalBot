import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import GigaChat
from newbot.bot_virustotal.config import *

llm = ChatOpenAI(
        api_key=DEEPSEEK_API_KEY,  # Ваш API ключ DeepSeek
        base_url="https://api.deepseek.com/v1",  # DeepSeek API endpoint
        model="deepseek-chat",  # Модель DeepSeek
        temperature=0.6
    )

def analyze_virustotal_report(report_data: dict):
    llm = GigaChat(
        credentials=GIGACHAT_TOKEN,
        model="GigaChat:latest",
        verify_ssl_certs=False,
        temperature=0.6
    )

    # Первый промпт - глубокий анализ с рассуждениями
    analysis_prompt = ChatPromptTemplate.from_template("""  
    Ты — эксперт по кибербезопасности. Проанализируй JSON отчет от VirusTotal, следуя этим шагам:

    ШАГ 1: Сбор данных
    - Изучи статистику: total, malicious, suspicious, undetected
    - Проанализируй результаты антивирусов (results)

    ШАГ 2: Критическое мышление
    - Какие антивирусы имеют высокую репутацию и их детекты наиболее значимы?

    ШАГ 3: Формирование вывода
    На основе анализа предоставь структурированный ответ на русском:

    1. Уровень опасности (🔴Высокий/🟡Средний/🟢Низкий) + обоснование:
    2. Статистика детектов (malicious/suspicious/undetected):
    3. Ключевые находки (топ-3 наиболее значимых антивирусных детекта):
    4. Рекомендации по действиям:

    Данные для анализа: {input}
    """)

    # Второй промпт - рефлексия и фильтрация
    reflection_prompt = ChatPromptTemplate.from_template("""  
    Ты — старший аналитик безопасности. Проверь и доработай анализ угроз:

    ЗАДАЧА: 
    - Проанализируй предоставленный первичный анализ
    - Игнорируй undetected результаты как незначимые
    - Сфокусируйся только на malicious и suspicious детектах
    - Удали упоминания о необнаруженных угрозах
    - Усиль акцент на подтвержденных рисках

    КРИТЕРИИ КАЧЕСТВА:
    Только значимые детекты (malicious/suspicious)
    Конкретные названия антивирусов с высоким доверием
    Практические рекомендации без воды

    **Первичный анализ для проверки:** {previous_analysis}

    **Верни улучшенную версию на русском без упоминания undetected:**
    """)

    # Первый этап - глубокий анализ
    analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt)
    initial_analysis = analysis_chain.invoke({"input": json.dumps(report_data)})

    # Второй этап - рефлексия и фильтрация
    reflection_chain = LLMChain(llm=llm, prompt=reflection_prompt)
    final_result = reflection_chain.invoke({"previous_analysis": initial_analysis["text"]})

    return final_result["text"]